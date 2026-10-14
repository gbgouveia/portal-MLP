/**
 * Firebase Client-Side Configuration & Initializer
 * Versão: Firebase Modular SDK v10 (ESM)
 */

import { initializeApp, getApps, getApp } from "https://www.gstatic.com/firebasejs/10.12.2/firebase-app.js";
import { getAuth } from "https://www.gstatic.com/firebasejs/10.12.2/firebase-auth.js";
import { getFirestore } from "https://www.gstatic.com/firebasejs/10.12.2/firebase-firestore.js";
import { getStorage } from "https://www.gstatic.com/firebasejs/10.12.2/firebase-storage.js";

// Configuração Oficial do Firebase para o Portal MLP
const defaultFirebaseConfig = {
  apiKey: "AIzaSyDyTc2EZztDP72Ssuzt_DHFjUDYzZmegas",
  authDomain: "portal-igreja-e6a66.firebaseapp.com",
  projectId: "portal-igreja-e6a66",
  storageBucket: "portal-igreja-e6a66.firebasestorage.app",
  messagingSenderId: "1013927945766",
  appId: "1:1013927945766:web:76879218b1e6ac3e2fa8e7"
};

const hasValidInjectedConfig = (
  typeof window !== "undefined" &&
  window.MLP_FIREBASE_CONFIG &&
  typeof window.MLP_FIREBASE_CONFIG === "object" &&
  typeof window.MLP_FIREBASE_CONFIG.apiKey === "string" &&
  window.MLP_FIREBASE_CONFIG.apiKey.startsWith("AIzaSy") &&
  !window.MLP_FIREBASE_CONFIG.apiKey.includes("PLACEHOLDER")
);

const firebaseConfig = hasValidInjectedConfig
  ? window.MLP_FIREBASE_CONFIG
  : defaultFirebaseConfig;

// Inicialização segura
let app;
let auth;
let db;
let storage;
let isConfigured = true;

try {
  app = !getApps().length ? initializeApp(firebaseConfig) : getApp();
  auth = getAuth(app);
  db = getFirestore(app);
  try {
    storage = getStorage(app);
  } catch (stErr) {
    console.warn("[Firebase Storage] Storage não configurado ou em pausa:", stErr.message);
  }
} catch (err) {
  console.error("[Firebase MLP] Erro ao inicializar Firebase:", err);
}

export { app, auth, db, storage, isConfigured, firebaseConfig };
