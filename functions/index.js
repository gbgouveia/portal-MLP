/**
 * Cloud Functions — Ministério Luz da Palavra (MLP)
 * 
 * 1. Monitoramento automático de Live no YouTube (baixo custo de cota: uploads playlist + videos.list)
 * 2. Atualização idempotente de live/atual, avisos e notificações em broadcast
 * 3. Notificações Push via Firebase Cloud Messaging (FCM)
 * 4. Disparo oficial de WhatsApp Business Cloud API (Meta) em lote com controle LGPD e webhook de unsubscribe ("SAIR"/"PARAR")
 * 5. Atribuição de Custom Claims (admin / membro)
 */

const { onRequest, onCall, HttpsError } = require("firebase-functions/v2/https");
const { onSchedule } = require("firebase-functions/v2/scheduler");
const admin = require("firebase-admin");

if (!admin.apps.length) {
  admin.initializeApp();
}

const db = admin.firestore();
const messaging = admin.messaging();

// Constantes do Canal Oficial
const CHANNEL_ID = "UCkvN5Uqsjhj6lSpIX5JhBpA";
const UPLOADS_PLAYLIST_ID = "UUkvN5Uqsjhj6lSpIX5JhBpA"; // 'UU' substitui 'UC'

/**
 * 1. Cloud Function Agendada: Verificar Live no YouTube a cada 3 minutos
 * Cota mínima: 1 unidade (playlistItems.list) + 1 unidade (videos.list) = 2 unidades por execução!
 */
exports.checkYouTubeLive = onSchedule(
  {
    schedule: "every 3 minutes",
    secrets: ["YOUTUBE_API_KEY", "META_WHATSAPP_TOKEN", "META_PHONE_NUMBER_ID"],
    timeZone: "America/Sao_Paulo",
    retryCount: 1,
  },
  async (event) => {
    const apiKey = process.env.YOUTUBE_API_KEY;
    if (!apiKey) {
      console.warn("[YouTube Live] Chave YOUTUBE_API_KEY não configurada em secrets. Ignorando checagem.");
      return;
    }

    try {
      // 1. Consulta últimos itens da playlist de uploads (custa 1 unidade de cota)
      const playlistUrl = `https://www.googleapis.com/youtube/v3/playlistItems?part=snippet&playlistId=${UPLOADS_PLAYLIST_ID}&maxResults=3&key=${apiKey}`;
      const playlistRes = await fetch(playlistUrl);
      if (!playlistRes.ok) {
        throw new Error(`Falha na API do YouTube (playlistItems): HTTP ${playlistRes.status}`);
      }
      const playlistData = await playlistRes.json();
      const videoIds = (playlistData.items || []).map((item) => item.snippet?.resourceId?.videoId).filter(Boolean);

      if (videoIds.length === 0) {
        console.log("[YouTube Live] Nenhum vídeo recente encontrado na playlist.");
        return;
      }

      // 2. Consulta videos.list com snippet e liveStreamingDetails (custa 1 unidade)
      const videosUrl = `https://www.googleapis.com/youtube/v3/videos?part=snippet,liveStreamingDetails&id=${videoIds.join(",")}&key=${apiKey}`;
      const videosRes = await fetch(videosUrl);
      if (!videosRes.ok) {
        throw new Error(`Falha na API do YouTube (videos): HTTP ${videosRes.status}`);
      }
      const videosData = await videosRes.json();

      let activeLive = null;
      for (const v of videosData.items || []) {
        if (v.snippet?.liveBroadcastContent === "live") {
          activeLive = {
            videoId: v.id,
            titulo: v.snippet.title,
            url: `https://www.youtube.com/watch?v=${v.id}`,
          };
          break;
        }
      }

      const liveRef = db.doc("live/atual");
      const currentLiveSnap = await liveRef.get();
      const currentLive = currentLiveSnap.exists ? currentLiveSnap.data() : { ativo: false };

      if (activeLive) {
        // Live ativa encontrada
        if (!currentLive.ativo || currentLive.videoId !== activeLive.videoId) {
          console.log(`[YouTube Live] Nova transmissão detectada: ${activeLive.videoId} - "${activeLive.titulo}"`);
          
          await liveRef.set({
            ativo: true,
            videoId: activeLive.videoId,
            titulo: activeLive.titulo,
            url: activeLive.url,
            iniciadaEm: admin.firestore.FieldValue.serverTimestamp(),
          });

          // Dispara broadcast de notificações e avisos de forma idempotente
          await triggerLiveBroadcast(activeLive);
        }
      } else {
        // Nenhuma transmissão ao vivo no momento
        if (currentLive.ativo) {
          console.log(`[YouTube Live] Transmissão anterior encerrada.`);
          await liveRef.update({
            ativo: false,
            encerradaEm: admin.firestore.FieldValue.serverTimestamp(),
          });
        }
      }
    } catch (err) {
      console.error("[YouTube Live] Erro na verificação agendada:", err);
    }
  }
);

/**
 * Disparo idempotente de notificações de Live (Avisos, Notificação para o Sininho, Push e WhatsApp)
 */
async function triggerLiveBroadcast(liveData) {
  const { videoId, titulo, url } = liveData;

  // Idempotência: verifica se este videoId já foi notificado
  const notifId = `live_${videoId}`;
  const notifRef = db.doc(`notificacoes/${notifId}`);
  const notifSnap = await notifRef.get();

  if (notifSnap.exists) {
    console.log(`[Broadcast Live] Notificação para ${videoId} já foi disparada anteriormente. Ignorando.`);
    return;
  }

  // 1. Cria notificação para o sininho
  await notifRef.set({
    titulo: "Estamos Ao Vivo!",
    texto: `Transmissão: ${titulo}`,
    link: url,
    tipo: "live",
    videoId: videoId,
    criadoEm: admin.firestore.FieldValue.serverTimestamp(),
  });

  // 2. Cria aviso no Quadro de Avisos
  await db.collection("avisos").add({
    titulo: `Transmissão ao Vivo: ${titulo}`,
    texto: `A celebração do Ministério Luz da Palavra está sendo transmitida agora no canal oficial do YouTube. Acesse e participe conosco.`,
    tipo: "live",
    fixado: true,
    publicado: true,
    criadoPor: "sistema",
    criadoEm: admin.firestore.FieldValue.serverTimestamp(),
    expiraEm: new Date(Date.now() + 6 * 3600 * 1000), // expira em 6 horas
    link: url,
  });

  // 3. Dispara Push Notification via FCM para tokens válidos
  try {
    const membrosSnap = await db.collection("membros").where("status", "==", "ativo").get();
    const tokens = [];

    membrosSnap.forEach((doc) => {
      const data = doc.data();
      if (Array.isArray(data.fcmTokens)) {
        tokens.push(...data.fcmTokens);
      }
    });

    if (tokens.length > 0) {
      const uniqueTokens = [...new Set(tokens)];
      await messaging.sendEachForMulticast({
        tokens: uniqueTokens,
        notification: {
          title: "Ministério Luz da Palavra — Ao Vivo!",
          body: titulo,
        },
        webpush: {
          fcmOptions: {
            link: url,
          },
        },
      });
      console.log(`[FCM] Push disparado para ${uniqueTokens.length} dispositivos.`);
    }
  } catch (pushErr) {
    console.error("[FCM] Erro ao enviar push:", pushErr);
  }

  // 4. Dispara WhatsApp Business oficial em modo de teste ou produção
  await sendWhatsAppBatch("aviso_live", {
    param1: "Irmão(ã)",
    param2: url,
    resumo: titulo,
  });
}

/**
 * 2. Envio de Mensagens de WhatsApp Oficial (Meta Business Cloud API)
 */
async function sendWhatsAppBatch(templateName, params) {
  const token = process.env.META_WHATSAPP_TOKEN;
  const phoneNumberId = process.env.META_PHONE_NUMBER_ID;

  // Busca membros ativos com consentimento explícito
  const membrosSnap = await db.collection("membros")
    .where("status", "==", "ativo")
    .where("consentimentoWhatsapp", "==", true)
    .get();

  if (membrosSnap.empty) {
    console.log("[WhatsApp] Nenhum membro ativo com consentimento de WhatsApp cadastrado.");
    return;
  }

  const isTestMode = !token || !phoneNumberId;
  console.log(`[WhatsApp] Iniciando envio (${isTestMode ? "MODO TESTE" : "MODO PRODUÇÃO"}) para ${membrosSnap.size} contatos.`);

  for (const doc of membrosSnap.docs) {
    const membro = doc.data();
    const telefone = membro.telefone; // E.164 (+5561...)

    if (!telefone) continue;

    const envioId = `envio_${doc.id}_${Date.now()}`;
    const envioRef = db.collection("envios").doc(envioId);

    if (isTestMode) {
      // Modo de teste: apenas registra no Firestore sem gastar créditos da Meta
      await envioRef.set({
        membroUid: doc.id,
        nome: membro.nome || "Irmão",
        telefone: telefone,
        template: templateName,
        status: "simulado_sucesso",
        mensagem: `[SIMULAÇÃO] Modelo ${templateName} registrado com sucesso para ${telefone}. Chaves da Meta não configuradas.`,
        criadoEm: admin.firestore.FieldValue.serverTimestamp(),
      });
    } else {
      // Modo de produção: chamada real à WhatsApp Cloud API da Meta
      try {
        const payload = {
          messaging_product: "whatsapp",
          to: telefone.replace("+", ""),
          type: "template",
          template: {
            name: templateName,
            language: { code: "pt_BR" },
            components: [
              {
                type: "body",
                parameters: [
                  { type: "text", text: membro.nome || "Irmão(ã)" },
                  { type: "text", text: params.param2 || "" },
                ],
              },
            ],
          },
        };

        const res = await fetch(`https://graph.facebook.com/v19.0/${phoneNumberId}/messages`, {
          method: "POST",
          headers: {
            Authorization: `Bearer ${token}`,
            "Content-Type": "application/json",
          },
          body: JSON.stringify(payload),
        });

        const data = await res.json();
        if (res.ok) {
          await envioRef.set({
            membroUid: doc.id,
            nome: membro.nome || "Irmão",
            telefone: telefone,
            template: templateName,
            status: "sucesso",
            metaMessageId: data.messages?.[0]?.id || null,
            criadoEm: admin.firestore.FieldValue.serverTimestamp(),
          });
        } else {
          await envioRef.set({
            membroUid: doc.id,
            nome: membro.nome || "Irmão",
            telefone: telefone,
            template: templateName,
            status: "erro",
            erroDetalhe: data.error || data,
            criadoEm: admin.firestore.FieldValue.serverTimestamp(),
          });
        }
      } catch (sendErr) {
        await envioRef.set({
          membroUid: doc.id,
          nome: membro.nome || "Irmão",
          telefone: telefone,
          template: templateName,
          status: "falha_conexao",
          erroDetalhe: sendErr.message,
          criadoEm: admin.firestore.FieldValue.serverTimestamp(),
        });
      }
    }
  }
}

/**
 * 3. Webhook da Meta para WhatsApp: Trata "SAIR" / "PARAR" (Opt-out LGPD)
 */
exports.whatsappWebhook = onRequest(
  { secrets: ["META_WEBHOOK_VERIFY_TOKEN"] },
  async (req, res) => {
    // Verificação do webhook pelo painel de desenvolvedores da Meta
    if (req.method === "GET") {
      const mode = req.query["hub.mode"];
      const token = req.query["hub.verify_token"];
      const challenge = req.query["hub.challenge"];
      const verifyToken = process.env.META_WEBHOOK_VERIFY_TOKEN || "mlp_whatsapp_verify_token_2026";

      if (mode === "subscribe" && token === verifyToken) {
        console.log("[WhatsApp Webhook] Verificação do Hub efetuada com sucesso!");
        res.status(200).send(challenge);
      } else {
        res.status(403).send("Token de verificação inválido.");
      }
      return;
    }

    // Recebimento de mensagens dos usuários
    if (req.method === "POST") {
      try {
        const body = req.body;
        const entry = body.entry?.[0];
        const changes = entry?.changes?.[0];
        const value = changes?.value;
        const messages = value?.messages;

        if (Array.isArray(messages) && messages.length > 0) {
          for (const msg of messages) {
            const from = msg.from; // Número do remetente (ex: "5561999999999")
            const text = (msg.text?.body || "").trim().toUpperCase();

            if (text === "SAIR" || text === "PARAR" || text === "CANCELAR") {
              console.log(`[WhatsApp LGPD] Solicitação de cancelamento de envio recebida do número ${from}`);
              
              // Busca membros associados a esse telefone e desativa consentimento
              const formattedPhone = from.startsWith("+") ? from : `+${from}`;
              const membrosSnap = await db.collection("membros")
                .where("telefone", "in", [formattedPhone, from])
                .get();

              for (const doc of membrosSnap.docs) {
                await doc.ref.update({
                  consentimentoWhatsapp: false,
                  optOutData: admin.firestore.FieldValue.serverTimestamp(),
                });
                console.log(`[WhatsApp LGPD] Consentimento revogado para o membro UID: ${doc.id}`);
              }
            }
          }
        }
        res.status(200).send("EVENT_RECEIVED");
      } catch (err) {
        console.error("[WhatsApp Webhook] Erro no processamento:", err);
        res.status(500).send("Internal Server Error");
      }
    }
  }
);

/**
 * 4. Atribuição de Funções de Administrador (Custom Claims)
 * Apenas usuários que já são admin podem promover outros membros.
 */
exports.setAdminRole = onCall(async (request) => {
  // Verifica se o solicitante é admin ou se é o primeiro usuário do sistema
  const callerAuth = request.auth;
  if (!callerAuth) {
    throw new HttpsError("unauthenticated", "Usuário não autenticado.");
  }

  const { targetUid, isAdmin } = request.data;
  if (!targetUid) {
    throw new HttpsError("invalid-argument", "UID de destino é obrigatório.");
  }

  const callerIsAdmin = callerAuth.token.admin === true || callerAuth.token.role === "admin";
  if (!callerIsAdmin) {
    throw new HttpsError("permission-denied", "Apenas administradores podem gerenciar papéis de usuários.");
  }

  await admin.auth().setCustomUserClaims(targetUid, {
    admin: !!isAdmin,
    role: isAdmin ? "admin" : "membro",
  });

  return { success: true, targetUid, isAdmin: !!isAdmin };
});
