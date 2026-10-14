/**
 * Live Stream Real-Time Sync Service — Ministério Luz da Palavra
 * Sincroniza o bloco de transmissões com a coleção live/atual no Firestore em tempo real.
 */

import { db, isConfigured } from "./config.js";
import { doc, onSnapshot } from "https://www.gstatic.com/firebasejs/10.12.2/firebase-firestore.js";

const DEFAULT_CHANNEL_ID = "UCkvN5Uqsjhj6lSpIX5JhBpA";
const FALLBACK_VIDEO_ID = "f6ArFvSPlkw"; // Vídeo público verificado do canal

export function initLiveStreamWatcher() {
  const topLiveBanner = document.getElementById("top-live-banner");
  const topLiveTitle = document.getElementById("top-live-title");
  const liveIndicator = document.getElementById("live-status-indicator");
  const recordedIndicator = document.getElementById("recorded-status-indicator");
  const transmissionTitle = document.getElementById("transmission-title");
  const playerMount = document.getElementById("transmission-player-mount");

  if (!isConfigured) {
    // Se o Firebase ainda não tiver chaves reais no .env, garante o fallback perfeito
    return;
  }

  try {
    const liveDocRef = doc(db, "live", "atual");

    onSnapshot(liveDocRef, (snap) => {
      if (!snap.exists()) return;

      const data = snap.data();
      const isLive = data.ativo === true;

      // 1. Atualiza a barra de topo
      if (topLiveBanner) {
        if (isLive) {
          topLiveBanner.style.display = "block";
          if (topLiveTitle) topLiveTitle.textContent = data.titulo || "Culto Ao Vivo";
        } else {
          topLiveBanner.style.display = "none";
        }
      }

      // 2. Atualiza indicadores de status
      if (liveIndicator) {
        liveIndicator.style.display = isLive ? "flex" : "none";
      }
      if (recordedIndicator) {
        recordedIndicator.style.display = isLive ? "none" : "inline-block";
      }

      // 3. Atualiza título
      if (transmissionTitle && data.titulo) {
        transmissionTitle.textContent = data.titulo;
      }

      // 4. Atualiza o player de transmissão dinamicamente
      if (playerMount) {
        const videoId = isLive ? data.videoId : (data.lastVideoId || FALLBACK_VIDEO_ID);
        const title = data.titulo || "Transmissão Oficial — Ministério Luz da Palavra";

        // Cria o iframe seguro e responsivo com aspect-ratio 16:9
        playerMount.innerHTML = `
          <div class="stream-player-container" style="position: relative; width: 100%; aspect-ratio: 16/9; background-color: #0c0806; border-radius: 8px; overflow: hidden; box-shadow: 0 10px 30px rgba(0,0,0,0.45); border: 1px solid rgba(242, 209, 109, 0.2);">
            <iframe
              src="https://www.youtube-nocookie.com/embed/${videoId}${isLive ? '?autoplay=1&mute=0' : ''}"
              title="${title}"
              style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; border: none;"
              allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share"
              allowfullscreen
              loading="lazy"
              referrerpolicy="strict-origin-when-cross-origin">
            </iframe>
          </div>
        `;
      }
    }, (err) => {
      console.warn("[Live Watcher] Falha na sincronização em tempo real:", err);
      // Plano B: se a API falhar, monta o player com live_stream padrão do canal
      if (playerMount && !playerMount.querySelector("iframe")) {
        playerMount.innerHTML = `
          <div class="stream-player-container" style="position: relative; width: 100%; aspect-ratio: 16/9; background-color: #0c0806; border-radius: 8px; overflow: hidden;">
            <iframe
              src="https://www.youtube.com/embed/live_stream?channel=${DEFAULT_CHANNEL_ID}"
              title="Canal Oficial MLP"
              style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; border: none;"
              allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share"
              allowfullscreen
              loading="lazy"
              referrerpolicy="strict-origin-when-cross-origin">
            </iframe>
          </div>
        `;
      }
    });
  } catch (e) {
    console.error("[Live Watcher] Erro ao inicializar observador da live:", e);
  }
}
