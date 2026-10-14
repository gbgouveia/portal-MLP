/**
 * Firebase Client Entry Point — Ministério Luz da Palavra
 * Conecta autenticação, notificações, live do YouTube e avisos.
 */

import { initHeaderAuthSync } from "./auth-service.js";
import { initLiveStreamWatcher } from "./live-service.js";
import { initNotificationsWatcher, initAvisosBoard } from "./notifications-service.js";

document.addEventListener("DOMContentLoaded", () => {
  // Sincroniza sessão e estado do usuário no cabeçalho
  initHeaderAuthSync();

  // Escuta status da live do YouTube em tempo real
  initLiveStreamWatcher();

  // Escuta notificações e avisos para o sininho
  initNotificationsWatcher();

  // Renderiza quadro de avisos dinâmico
  initAvisosBoard();
});
