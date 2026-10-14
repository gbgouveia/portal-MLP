/**
 * Firebase Auth Service — Ministério Luz da Palavra
 * Cadastro, login, LGPD, perfil com resize no browser e gestão de claims.
 */

// Helper para resolver paths em GitHub Pages (/portal-MLP/) vs local (/)
function getBasePath() {
  const base = document.querySelector('base');
  if (base && base.href) {
    try { return new URL(base.href).pathname.replace(/\/$/, ''); } catch(e) {}
  }
  // Detecta sub-path pelo location
  const match = window.location.pathname.match(/^\/([^/]+)/);
  if (match && ['portal-MLP'].includes(match[1])) return '/' + match[1];
  return '';
}
function resolvePath(path) {
  return getBasePath() + path;
}

import { auth, db, storage, isConfigured } from "./config.js";
import {
  createUserWithEmailAndPassword,
  signInWithEmailAndPassword,
  signOut,
  onAuthStateChanged,
  sendEmailVerification,
  updateProfile,
  deleteUser,
  setPersistence,
  browserLocalPersistence
} from "https://www.gstatic.com/firebasejs/10.12.2/firebase-auth.js";
import {
  doc,
  setDoc,
  getDoc,
  updateDoc,
  deleteDoc,
  serverTimestamp
} from "https://www.gstatic.com/firebasejs/10.12.2/firebase-firestore.js";
import {
  ref,
  uploadBytes,
  getDownloadURL,
  deleteObject
} from "https://www.gstatic.com/firebasejs/10.12.2/firebase-storage.js";

// Configuração explícita de persistência local (browserLocalPersistence)
if (auth) {
  setPersistence(auth, browserLocalPersistence).catch((err) => {
    console.warn("[Auth] Não foi possível forçar browserLocalPersistence:", err.message);
  });
}

// Promessa única global authReady que resolve na primeira emissão do onAuthStateChanged
let _resolveAuthReady;
export const authReady = new Promise((resolve) => {
  _resolveAuthReady = resolve;
});

let _initialAuthEmitted = false;
onAuthStateChanged(auth, (user) => {
  if (!_initialAuthEmitted) {
    _initialAuthEmitted = true;
    _resolveAuthReady(user);
  }
});

export async function waitForAuth() {
  await authReady;
  return auth.currentUser;
}

// Trava Anti-Loop em sessionStorage: detecta mais de 2 redirecionamentos entre /entrar e /perfil em 10s
export function checkAntiLoop(currentPage) {
  const KEY = "mlp_auth_loop_log";
  const now = Date.now();
  let entries = [];
  try {
    entries = JSON.parse(sessionStorage.getItem(KEY) || "[]");
  } catch (e) {
    entries = [];
  }
  // Mantém apenas saltos nos últimos 10 segundos
  entries = entries.filter((e) => now - e.t < 10000);
  entries.push({ p: currentPage, t: now });
  sessionStorage.setItem(KEY, JSON.stringify(entries));

  const authBounces = entries.filter((e) => e.p.includes("entrar") || e.p.includes("perfil"));
  if (authBounces.length >= 3) {
    console.error("[Anti-Loop] Trava ativada! Mais de 2 redirecionamentos detectados em 10s:", entries);
    return true;
  }
  return false;
}

export function resetAntiLoop() {
  sessionStorage.removeItem("mlp_auth_loop_log");
}

// Sanitização de parâmetro ?next= (apenas caminhos internos seguros que começam com "/")
export function getSafeNextUrl(defaultUrl = "/perfil/") {
  const params = new URLSearchParams(window.location.search);
  const next = params.get("next");
  if (next && next.startsWith("/") && !next.startsWith("//") && !next.startsWith("/\\")) {
    return next;
  }
  return defaultUrl;
}

// Garante existência de documento membros/{uid} sem falhar ou deslogar
export async function ensureMembroDoc(user) {
  if (!user) return null;
  try {
    const userRef = doc(db, "membros", user.uid);
    const snap = await getDoc(userRef);
    if (!snap.exists()) {
      const initialDoc = {
        nome: user.displayName || (user.email ? user.email.split("@")[0] : "Membro"),
        email: (user.email || "").toLowerCase(),
        telefone: "",
        fotoUrl: user.photoURL || null,
        status: "ativo",
        consentimentoWhatsapp: false,
        consentimentoEmail: false,
        criadoEm: serverTimestamp(),
      };
      await setDoc(userRef, initialDoc, { merge: true });
      return initialDoc;
    }
    return snap.data();
  } catch (err) {
    console.warn("[Auth] Não foi possível verificar/criar membros/{uid}:", err.message);
    return null;
  }
}

// Formatação e conversão de telefone para padrão E.164 (+5561...)
export function formatToE164(rawPhone) {
  const digits = rawPhone.replace(/\D/g, "");
  if (digits.length === 11) {
    return `+55${digits}`;
  } else if (digits.length === 13 && digits.startsWith("55")) {
    return `+${digits}`;
  }
  return `+55${digits}`;
}

export function maskPhoneInput(inputEl) {
  inputEl.addEventListener("input", (e) => {
    let v = e.target.value.replace(/\D/g, "");
    if (v.length > 11) v = v.slice(0, 11);

    if (v.length > 6) {
      e.target.value = `(${v.slice(0, 2)}) ${v.slice(2, 7)}-${v.slice(7)}`;
    } else if (v.length > 2) {
      e.target.value = `(${v.slice(0, 2)}) ${v.slice(2)}`;
    } else if (v.length > 0) {
      e.target.value = `(${v}`;
    } else {
      e.target.value = "";
    }
  });
}

// Mensagens de erro em português para autenticação
export function getFriendlyErrorMessage(error) {
  const code = error.code || "";
  switch (code) {
    case "auth/email-already-in-use":
      return "Este endereço de e-mail já está cadastrado em nosso portal.";
    case "auth/invalid-email":
      return "Por favor, informe um endereço de e-mail válido.";
    case "auth/weak-password":
      return "A senha deve conter no mínimo 8 caracteres para sua segurança.";
    case "auth/user-not-found":
    case "auth/wrong-password":
    case "auth/invalid-credential":
      return "E-mail ou senha incorretos. Por favor, verifique os dados digitados.";
    case "auth/too-many-requests":
      return "Muitas tentativas sem sucesso. Aguarde alguns instantes antes de tentar novamente.";
    case "auth/requires-recent-login":
      return "Para esta operação sensível, é necessário fazer login novamente.";
    default:
      return error.message || "Ocorreu um erro no processamento. Tente novamente.";
  }
}

// 1. Cadastro de Membro (com Consentimento LGPD explícito)
export async function cadastrarMembro({ nome, email, telefone, senha, consentimentoWhatsapp, consentimentoEmail }) {
  if (!isConfigured) {
    console.warn("[Auth] Operando em modo de demonstração.");
  }

  // 1. Cria usuário no Firebase Auth
  const userCredential = await createUserWithEmailAndPassword(auth, email, senha);
  const user = userCredential.user;

  // 2. Atualiza nome de exibição no Auth
  await updateProfile(user, { displayName: nome });

  // 3. Envia e-mail de verificação
  try {
    await sendEmailVerification(user);
  } catch (e) {
    console.warn("[Auth] Não foi possível disparar email de confirmação imediato:", e);
  }

  // 4. Grava na coleção membros/{uid} com auditoria LGPD
  const phoneE164 = formatToE164(telefone);
  const membroData = {
    nome: nome.trim(),
    email: email.trim().toLowerCase(),
    telefone: phoneE164,
    fotoUrl: null,
    status: "ativo",
    consentimentoWhatsapp: !!consentimentoWhatsapp,
    consentimentoEmail: !!consentimentoEmail,
    consentimentoData: serverTimestamp(),
    fcmTokens: [],
    criadoEm: serverTimestamp(),
  };

  await setDoc(doc(db, "membros", user.uid), membroData);
  return { user, membroData };
}

// 2. Login com E-mail e Senha
export async function loginMembro(email, senha) {
  const userCredential = await signInWithEmailAndPassword(auth, email, senha);
  return userCredential.user;
}

// 3. Logout
export async function logoutMembro() {
  await signOut(auth);
}

// 4. Redimensionar imagem em Canvas no navegador (< 512px) e converter para WebP
export function resizeImageToBlob(file, maxDimension = 512) {
  return new Promise((resolve, reject) => {
    const reader = new FileReader();
    reader.onload = (e) => {
      const img = new Image();
      img.onload = () => {
        let width = img.width;
        let height = img.height;

        if (width > height) {
          if (width > maxDimension) {
            height = Math.round((height * maxDimension) / width);
            width = maxDimension;
          }
        } else {
          if (height > maxDimension) {
            width = Math.round((width * maxDimension) / height);
            height = maxDimension;
          }
        }

        const canvas = document.createElement("canvas");
        canvas.width = width;
        canvas.height = height;
        const ctx = canvas.getContext("2d");
        ctx.drawImage(img, 0, 0, width, height);

        canvas.toBlob(
          (blob) => {
            if (blob) {
              resolve(blob);
            } else {
              reject(new Error("Falha ao compactar imagem."));
            }
          },
          "image/webp",
          0.85
        );
      };
      img.onerror = reject;
      img.src = e.target.result;
    };
    reader.onerror = reject;
    reader.readAsDataURL(file);
  });
}

// 5. Upload de Foto de Perfil
export async function uploadFotoPerfil(uid, file) {
  const optimizedBlob = await resizeImageToBlob(file, 512);
  const storageRef = ref(storage, `perfis/${uid}/avatar.webp`);

  await uploadBytes(storageRef, optimizedBlob, {
    contentType: "image/webp",
  });

  const downloadUrl = await getDownloadURL(storageRef);

  // Atualiza no Auth e no Firestore
  if (auth.currentUser) {
    await updateProfile(auth.currentUser, { photoURL: downloadUrl });
  }
  await updateDoc(doc(db, "membros", uid), {
    fotoUrl: downloadUrl,
    fotoAtualizadaEm: serverTimestamp(),
  });

  return downloadUrl;
}

// 6. Atualização de Dados e Consentimentos LGPD
export async function atualizarPerfilMembro(uid, { nome, telefone, consentimentoWhatsapp, consentimentoEmail }) {
  const updatePayload = {
    nome: nome.trim(),
    telefone: formatToE164(telefone),
    consentimentoWhatsapp: !!consentimentoWhatsapp,
    consentimentoEmail: !!consentimentoEmail,
    atualizadoEm: serverTimestamp(),
  };

  await updateDoc(doc(db, "membros", uid), updatePayload);

  if (auth.currentUser && auth.currentUser.displayName !== nome) {
    await updateProfile(auth.currentUser, { displayName: nome });
  }

  return updatePayload;
}

// 7. Exclusão da Conta e dos Dados (Direito ao Esquecimento LGPD)
export async function excluirContaMembro(uid) {
  // 1. Exclui foto no Storage se houver
  try {
    const storageRef = ref(storage, `perfis/${uid}/avatar.webp`);
    await deleteObject(storageRef);
  } catch (e) {
    // Foto pode não existir
  }

  // 2. Exclui documento no Firestore
  await deleteDoc(doc(db, "membros", uid));

  // 3. Exclui usuário no Firebase Auth
  if (auth.currentUser) {
    await deleteUser(auth.currentUser);
  }
}

// 8. Sincronização do Cabeçalho com Estado de Autenticação
export function initHeaderAuthSync() {
  const accountSlot = document.getElementById("site-header-account");
  const bellContainer = document.getElementById("header-bell-container");
  const authSlot = document.getElementById("header-auth-slot");
  const mobileAccountSlot = document.getElementById("site-mobile-account-slot") || document.getElementById("mobile-menu-account") || document.querySelector(".mobile-menu__account");
  const targetDesktopSlot = authSlot || accountSlot;

  onAuthStateChanged(auth, async (user) => {
    if (user) {
      // Usuário autenticado
      if (bellContainer) bellContainer.style.display = "block";

      // Busca dados adicionais do membro no Firestore (foto, role)
      let photoUrl = user.photoURL;
      let isAdmin = false;
      let nome = user.displayName || (user.email ? user.email.split("@")[0] : "Membro");

      try {
        const idTokenResult = await user.getIdTokenResult();
        isAdmin = idTokenResult.claims.admin === true || idTokenResult.claims.role === "admin";

        const membroSnap = await getDoc(doc(db, "membros", user.uid));
        if (membroSnap.exists()) {
          const mData = membroSnap.data();
          if (mData.fotoUrl) photoUrl = mData.fotoUrl;
          if (mData.nome) nome = mData.nome;
        }
      } catch (err) {
        console.warn("[Auth Sync] Leitura de membro secundária:", err.message);
      }

      const initialLetter = nome.charAt(0).toUpperCase();

      if (targetDesktopSlot) {
        targetDesktopSlot.innerHTML = `
          <div class="site-header__user-menu" style="position: relative;">
            <button type="button" class="site-header__avatar-btn" id="header-avatar-btn" aria-expanded="false" aria-controls="header-user-dropdown" aria-label="Menu do usuário">
              ${photoUrl ? `<img src="${photoUrl}" alt="${nome}" class="site-header__avatar-img">` : `<span class="site-header__avatar-fallback">${initialLetter}</span>`}
            </button>
            <div class="site-header__dropdown site-header__dropdown--user" id="header-user-dropdown" aria-hidden="true">
              <div class="site-header__user-info">
                <strong>${nome}</strong>
                <span class="site-header__user-role">${isAdmin ? "Administrador" : "Membro"}</span>
              </div>
              <hr class="site-header__divider">
              <a href="${resolvePath('/perfil/')}" class="site-header__dropdown-item">Meu Perfil</a>
              ${isAdmin ? `<a href="${resolvePath('/painel/')}" class="site-header__dropdown-item">Painel de Gestão</a>` : ""}
              <hr class="site-header__divider">
              <button type="button" class="site-header__dropdown-item site-header__dropdown-item--danger" id="btn-logout-firebase" style="background:none; border:none; width:100%; text-align:left; cursor:pointer;">Sair</button>
            </div>
          </div>
        `;

        // Toggle do dropdown do avatar
        const avatarBtn = targetDesktopSlot.querySelector("#header-avatar-btn");
        const dropdown = targetDesktopSlot.querySelector("#header-user-dropdown");
        if (avatarBtn && dropdown) {
          avatarBtn.addEventListener("click", (e) => {
            e.stopPropagation();
            const isOpen = dropdown.classList.toggle("show");
            avatarBtn.setAttribute("aria-expanded", isOpen ? "true" : "false");
            dropdown.setAttribute("aria-hidden", isOpen ? "false" : "true");
          });
          document.addEventListener("click", () => {
            dropdown.classList.remove("show");
            avatarBtn.setAttribute("aria-expanded", "false");
            dropdown.setAttribute("aria-hidden", "true");
          });
        }

        // Event listener do logout desktop
        const logoutBtn = document.getElementById("btn-logout-firebase");
        if (logoutBtn) {
          logoutBtn.addEventListener("click", async () => {
            await logoutMembro();
            window.location.href = resolvePath("/");
          });
        }
      }

      if (mobileAccountSlot) {
        mobileAccountSlot.innerHTML = `
          <div class="mobile-menu__user-box">
            <span>Olá, <strong>${nome}</strong></span>
            <div class="mobile-menu__user-links">
              <a href="${resolvePath('/perfil/')}">Meu Perfil</a>
              ${isAdmin ? `<a href="${resolvePath('/painel/')}">Painel Admin</a>` : ""}
              <a href="#" id="btn-mobile-logout" style="color: #FF5252;">Sair</a>
            </div>
          </div>
        `;
        const mobileLogout = document.getElementById("btn-mobile-logout");
        if (mobileLogout) {
          mobileLogout.addEventListener("click", async (e) => {
            e.preventDefault();
            await logoutMembro();
            window.location.href = resolvePath("/");
          });
        }
      }
    } else {
      // Usuário deslogado
      if (bellContainer) bellContainer.style.display = "none";

      if (targetDesktopSlot) {
        targetDesktopSlot.innerHTML = `
          <div class="site-header__guest-links">
            <a href="${resolvePath('/entrar/')}" class="site-header__btn-login">Entrar</a>
            <a href="${resolvePath('/cadastro/')}" class="site-header__btn-register">Cadastrar</a>
          </div>
        `;
      }

      if (mobileAccountSlot) {
        mobileAccountSlot.innerHTML = `
          <div class="mobile-menu__auth-grid">
            <a href="${resolvePath('/entrar/')}" class="btn btn-outline-gold" style="width: 100%; text-align: center;">Entrar</a>
            <a href="${resolvePath('/cadastro/')}" class="btn btn-gold" style="width: 100%; text-align: center;">Cadastrar</a>
          </div>
        `;
      }
    }
  });
}
