#!/usr/bin/env node
/**
 * Script de Atribuição de Permissão de Administrador (Custom Claims no Firebase Auth)
 * 
 * Uso:
 *   node scripts/set-admin.mjs email@exemplo.com
 *   node scripts/set-admin.mjs email@exemplo.com --remove
 * 
 * Requisitos:
 *   Defina a variável GOOGLE_APPLICATION_CREDENTIALS apontando para a chave JSON:
 *   PowerShell: $env:GOOGLE_APPLICATION_CREDENTIALS="C:\caminho\para\serviceAccountKey.json"
 */

import { initializeApp, cert } from "firebase-admin/app";
import { getAuth } from "firebase-admin/auth";
import fs from "fs";

const args = process.argv.slice(2);
const listFlag = args.includes("--list");
const removeFlag = args.includes("--remove");
const email = args.find((a) => !a.startsWith("--"));

if (!listFlag && !email) {
  console.error("\x1b[31m[ERRO]\x1b[0m Informe o e-mail do usuário ou use --list para listar.");
  console.log("Uso:");
  console.log("  node scripts/set-admin.mjs email@exemplo.com");
  console.log("  node scripts/set-admin.mjs email@exemplo.com --remove");
  console.log("  node scripts/set-admin.mjs --list");
  process.exit(1);
}

// Inicializa Firebase Admin SDK com credenciais da variável de ambiente
const credentialsPath = process.env.GOOGLE_APPLICATION_CREDENTIALS;

if (!credentialsPath) {
  console.error("\x1b[31m[ERRO]\x1b[0m Nenhuma credencial encontrada!");
  console.error("Defina a variável de ambiente GOOGLE_APPLICATION_CREDENTIALS apontando para o arquivo JSON da conta de serviço:");
  console.error('  PowerShell: $env:GOOGLE_APPLICATION_CREDENTIALS="service-account.json"');
  process.exit(1);
}

if (!fs.existsSync(credentialsPath)) {
  console.error(`\x1b[31m[ERRO]\x1b[0m Arquivo de credenciais não encontrado em: ${credentialsPath}`);
  process.exit(1);
}

let auth;
try {
  const serviceAccount = JSON.parse(fs.readFileSync(credentialsPath, "utf-8"));
  const app = initializeApp({
    credential: cert(serviceAccount),
  });
  auth = getAuth(app);
  console.log(`[INFO] Conectado ao projeto Firebase: ${serviceAccount.project_id}`);
} catch (initErr) {
  console.error(`\x1b[31m[ERRO]\x1b[0m Falha ao inicializar Firebase Admin:`, initErr.message);
  process.exit(1);
}

async function run() {
  if (listFlag) {
    try {
      const list = await auth.listUsers(50);
      console.log(`\n=== Usuários Cadastrados no Firebase Auth (${list.users.length}) ===`);
      if (list.users.length === 0) {
        console.log("Nenhum usuário cadastrado ainda.");
      } else {
        list.users.forEach((u) => {
          const isAdmin = u.customClaims && u.customClaims.admin === true;
          console.log(`- ${u.email || "(sem email)"} | UID: ${u.uid} | Admin: ${isAdmin ? "\x1b[32mSIM\x1b[0m" : "NÃO"}`);
        });
      }
      return;
    } catch (listErr) {
      console.error(`\x1b[31m[ERRO]\x1b[0m Falha ao listar usuários:`, listErr.message);
      process.exit(1);
    }
  }
  try {
    const user = await auth.getUserByEmail(email);
    console.log(`[INFO] Usuário encontrado: ${user.email} (UID: ${user.uid})`);

    const currentClaims = user.customClaims || {};

    if (removeFlag) {
      const { admin: _, ...remainingClaims } = currentClaims;
      await auth.setCustomUserClaims(user.uid, remainingClaims);
      console.log(`\x1b[32m[SUCESSO]\x1b[0m Custom claim { admin: true } REMOVIDO para ${user.email}.`);
      console.log(`Claims atuais preservadas:`, remainingClaims);
    } else {
      const updatedClaims = {
        ...currentClaims,
        admin: true,
      };
      await auth.setCustomUserClaims(user.uid, updatedClaims);
      console.log(`\x1b[32m[SUCESSO]\x1b[0m Usuário ${user.email} recebeu o claim { admin: true }!`);
      console.log(`Claims preservadas e atualizadas:`, updatedClaims);
      console.log(`\x1b[33m[AVISO]\x1b[0m Para os novos privilégios entrarem em vigor no navegador, o token precisa ser renovado (o usuário deve sair e entrar novamente na conta, ou forçar user.getIdToken(true)).`);
    }
  } catch (err) {
    if (err.code === "auth/user-not-found") {
      console.error(`\x1b[31m[ERRO]\x1b[0m Nenhum usuário encontrado com o e-mail: ${email}`);
    } else {
      console.error(`\x1b[31m[ERRO]\x1b[0m Falha ao processar claims:`, err.message);
    }
    process.exit(1);
  }
}

run();
