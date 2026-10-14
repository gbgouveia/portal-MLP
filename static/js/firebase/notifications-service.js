/**
 * Notifications & Quadro de Avisos Service — Ministério Luz da Palavra
 * Sininho no cabeçalho em tempo real, push FCM com consentimento pós-clique,
 * histórico individual de lidas e renderização do quadro de avisos.
 */

import { auth, db, app, isConfigured } from "./config.js";
import {
  collection,
  query,
  where,
  orderBy,
  limit,
  onSnapshot,
  doc,
  setDoc,
  getDocs,
  updateDoc,
  arrayUnion,
  serverTimestamp
} from "https://www.gstatic.com/firebasejs/10.12.2/firebase-firestore.js";
import {
  getMessaging,
  getToken
} from "https://www.gstatic.com/firebasejs/10.12.2/firebase-messaging.js";

// Inicializa observador de notificações para o Sininho
export function initNotificationsWatcher() {
  const bellContainer = document.getElementById("header-bell-container");
  const unreadCountBadge = document.getElementById("header-unread-count");
  const notifListEl = document.getElementById("header-notifications-list");
  const markAllBtn = document.getElementById("btn-mark-all-read");

  if (!isConfigured) return;

  auth.onAuthStateChanged((user) => {
    if (!user) {
      if (bellContainer) bellContainer.style.display = "none";
      return;
    }

    if (bellContainer) bellContainer.style.display = "block";

    // 1. Escuta notificações broadcast (últimas 20)
    const notifQuery = query(
      collection(db, "notificacoes"),
      orderBy("criadoEm", "desc"),
      limit(20)
    );

    // 2. Escuta itens já lidos por este usuário
    const readDocsRef = collection(db, "lidas", user.uid, "itens");

    let allNotifs = [];
    let readNotifIds = new Set();

    const renderNotifications = () => {
      const unreadList = allNotifs.filter(n => !readNotifIds.has(n.id));
      const unreadCount = unreadList.length;

      if (unreadCountBadge) {
        if (unreadCount > 0) {
          unreadCountBadge.textContent = unreadCount > 99 ? "99+" : unreadCount;
          unreadCountBadge.style.display = "block";
        } else {
          unreadCountBadge.style.display = "none";
        }
      }

      if (notifListEl) {
        if (allNotifs.length === 0) {
          notifListEl.innerHTML = `<p class="site-header__empty-notif">Nenhuma notificação no momento.</p>`;
          return;
        }

        notifListEl.innerHTML = allNotifs.map(n => {
          const isUnread = !readNotifIds.has(n.id);
          return `
            <a href="${n.link || '#'}" class="site-header__notif-item ${isUnread ? 'unread' : ''}" data-id="${n.id}">
              <span class="site-header__notif-title">${n.titulo || 'Aviso'}</span>
              <span class="site-header__notif-text">${n.texto || ''}</span>
            </a>
          `;
        }).join("");

        // Clique para marcar individual como lida
        notifListEl.querySelectorAll(".site-header__notif-item").forEach(item => {
          item.addEventListener("click", async () => {
            const id = item.getAttribute("data-id");
            if (id && user) {
              await setDoc(doc(db, "lidas", user.uid, "itens", id), {
                lidoEm: serverTimestamp()
              });
            }
          });
        });
      }
    };

    onSnapshot(readDocsRef, (snap) => {
      readNotifIds = new Set(snap.docs.map(d => d.id));
      renderNotifications();
    });

    onSnapshot(notifQuery, (snap) => {
      allNotifs = snap.docs.map(d => ({ id: d.id, ...d.data() }));
      renderNotifications();
    });

    if (markAllBtn) {
      markAllBtn.addEventListener("click", async () => {
        for (const n of allNotifs) {
          if (!readNotifIds.has(n.id)) {
            await setDoc(doc(db, "lidas", user.uid, "itens", n.id), {
              lidoEm: serverTimestamp()
            });
          }
        }
      });
    }
  });
}

// Push FCM (solicitado ESTRITAMENTE após clique do usuário)
export async function enableBrowserPushNotifications() {
  if (!("Notification" in window)) {
    throw new Error("Seu navegador não suporta notificações Push.");
  }

  const permission = await Notification.requestPermission();
  if (permission !== "granted") {
    throw new Error("Permissão de notificações não concedida.");
  }

  const user = auth.currentUser;
  if (!user) {
    throw new Error("Faça login para receber notificações push.");
  }

  try {
    const messaging = getMessaging(app);
    const vapidKey = window.MLP_FIREBASE_VAPID_KEY || undefined;

    const token = await getToken(messaging, { vapidKey });
    if (token) {
      await updateDoc(doc(db, "membros", user.uid), {
        fcmTokens: arrayUnion(token)
      });
      return { success: true, token };
    }
  } catch (err) {
    console.error("[FCM] Falha ao registrar token:", err);
    throw err;
  }
}

// Renderização do Quadro de Avisos Público (Home e /avisos/)
export function initAvisosBoard() {
  const container = document.getElementById("home-avisos-container") || document.getElementById("avisos-board-grid");
  if (!container || !isConfigured) return;

  const now = new Date();
  const avisosQuery = query(
    collection(db, "avisos"),
    where("publicado", "==", true),
    orderBy("fixado", "desc"),
    orderBy("criadoEm", "desc"),
    limit(12)
  );

  onSnapshot(avisosQuery, (snap) => {
    if (snap.empty) {
      // Mantém aviso padrão se não houver registros
      return;
    }

    const typeColors = {
      geral: { bg: "rgba(191, 135, 31, 0.15)", text: "#8C4303", border: "#BF871F" },
      live: { bg: "#FFEBEE", text: "#D32F2F", border: "#EF5350" },
      evento: { bg: "rgba(140, 67, 3, 0.12)", text: "#8C4303", border: "#8C4303" },
      urgente: { bg: "#FFCDD2", text: "#B71C1C", border: "#E53935" },
    };

    const validAvisos = snap.docs
      .map(d => ({ id: d.id, ...d.data() }))
      .filter(a => !a.expiraEm || (a.expiraEm.toDate ? a.expiraEm.toDate() : new Date(a.expiraEm)) > now);

    if (validAvisos.length === 0) return;

    container.innerHTML = validAvisos.map(aviso => {
      const colors = typeColors[aviso.tipo] || typeColors.geral;
      const typeLabel = (aviso.tipo || "geral").toUpperCase();
      const dateStr = aviso.criadoEm?.toDate ? aviso.criadoEm.toDate().toLocaleDateString("pt-BR") : "";

      return `
        <div class="aviso-card ${aviso.fixado ? 'aviso-card--destaque' : ''}" 
             style="background: #FFF; border: 1px solid rgba(191, 135, 31, 0.3); border-radius: 8px; padding: 1.5rem; box-shadow: 0 4px 15px rgba(0,0,0,0.05); border-top: 4px solid ${aviso.fixado ? '#BF871F' : 'rgba(191,135,31,0.4)'};">
          <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.75rem;">
            <span class="badge-editorial" style="background: ${colors.bg}; color: ${colors.text}; border-color: ${colors.border};">${typeLabel}</span>
            ${aviso.fixado ? '<span style="font-size: 0.78rem; color: #8C4303; font-weight: 700;">★ Fixado</span>' : ''}
          </div>
          <h3 class="font-display" style="font-size: 1.2rem; color: #100904; margin-bottom: 0.5rem;">${aviso.titulo}</h3>
          <p style="font-size: 0.92rem; color: #555; line-height: 1.6; margin-bottom: 1rem;">
            ${aviso.texto}
          </p>
          <div style="display: flex; justify-content: space-between; align-items: center; font-size: 0.8rem; color: #888;">
            <span>${dateStr}</span>
            ${aviso.link ? `<a href="${aviso.link}" target="_blank" rel="noopener noreferrer" style="color: #BF871F; text-decoration: none; font-weight: 600;">Acessar &rarr;</a>` : ''}
          </div>
        </div>
      `;
    }).join("");
  }, (err) => {
    console.warn("[Avisos Board] Erro ao carregar avisos:", err);
  });
}
