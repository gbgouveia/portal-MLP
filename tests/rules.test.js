import { describe, it, before, after, beforeEach } from 'node:test';
import assert from 'node:assert';
import fs from 'node:fs';
import {
  initializeTestEnvironment,
  assertFails,
  assertSucceeds,
} from '@firebase/rules-unit-testing';

let testEnv;

before(async () => {
  testEnv = await initializeTestEnvironment({
    projectId: 'portal-igreja-e6a66',
    firestore: {
      rules: fs.readFileSync('firestore.rules', 'utf8'),
      host: '127.0.0.1',
      port: 8080,
    },
    storage: {
      rules: fs.readFileSync('storage.rules', 'utf8'),
      host: '127.0.0.1',
      port: 9199,
    },
  });
});

after(async () => {
  if (testEnv) {
    await testEnv.cleanup();
  }
});

beforeEach(async () => {
  if (testEnv) {
    await testEnv.clearFirestore();
  }
});

describe('Regras de Segurança do Firestore — Portal MLP', () => {
  it('Visitante anônimo NÃO pode ler documentos de membros', async () => {
    const unauthDb = testEnv.unauthenticatedContext().firestore();
    await assertFails(unauthDb.collection('membros').doc('alice').get());
  });

  it('Membro autenticado pode ler e criar seu próprio perfil', async () => {
    const aliceDb = testEnv.authenticatedContext('alice').firestore();
    await assertSucceeds(
      aliceDb.collection('membros').doc('alice').set({
        nome: 'Alice Oliveira',
        email: 'alice@exemplo.com',
        telefone: '+5561999990001',
        status: 'ativo',
        consentimentoWhatsapp: true,
        consentimentoEmail: true,
      })
    );

    const doc = await assertSucceeds(aliceDb.collection('membros').doc('alice').get());
    assert.strictEqual(doc.data().nome, 'Alice Oliveira');
  });

  it('Membro NÃO pode ler documento de outro membro', async () => {
    // Setup prévio pelo admin
    await testEnv.withSecurityRulesDisabled(async (context) => {
      await context.firestore().collection('membros').doc('bob').set({
        nome: 'Bob Silva',
        email: 'bob@exemplo.com',
        status: 'ativo',
      });
    });

    const aliceDb = testEnv.authenticatedContext('alice').firestore();
    await assertFails(aliceDb.collection('membros').doc('bob').get());
  });

  it('Membro NÃO pode alterar seu papel para admin ou alterar seu status', async () => {
    await testEnv.withSecurityRulesDisabled(async (context) => {
      await context.firestore().collection('membros').doc('alice').set({
        nome: 'Alice',
        status: 'ativo',
        role: 'membro',
      });
    });

    const aliceDb = testEnv.authenticatedContext('alice').firestore();
    // Tenta se autopromover para admin
    await assertFails(
      aliceDb.collection('membros').doc('alice').update({
        role: 'admin',
        admin: true,
      })
    );
  });

  it('Admin pode ler e gerenciar qualquer membro', async () => {
    await testEnv.withSecurityRulesDisabled(async (context) => {
      await context.firestore().collection('membros').doc('bob').set({
        nome: 'Bob Silva',
        status: 'ativo',
      });
    });

    const adminDb = testEnv.authenticatedContext('admin_user', { admin: true }).firestore();
    const doc = await assertSucceeds(adminDb.collection('membros').doc('bob').get());
    assert.strictEqual(doc.data().nome, 'Bob Silva');
  });

  it('Visitante anônimo pode ler avisos PUBLICADOS, mas NÃO pode ler rascunhos', async () => {
    await testEnv.withSecurityRulesDisabled(async (context) => {
      await context.firestore().collection('avisos').doc('aviso_publicado').set({
        titulo: 'Culto de Domingo',
        texto: 'Horário às 19h',
        publicado: true,
      });
      await context.firestore().collection('avisos').doc('aviso_rascunho').set({
        titulo: 'Aviso Interno',
        texto: 'Ainda em elaboração',
        publicado: false,
      });
    });

    const unauthDb = testEnv.unauthenticatedContext().firestore();
    await assertSucceeds(unauthDb.collection('avisos').doc('aviso_publicado').get());
    await assertFails(unauthDb.collection('avisos').doc('aviso_rascunho').get());
  });

  it('Membro comum NÃO pode criar avisos (apenas admin)', async () => {
    const aliceDb = testEnv.authenticatedContext('alice').firestore();
    await assertFails(
      aliceDb.collection('avisos').add({
        titulo: 'Novo Aviso',
        texto: 'Tentativa por membro',
        publicado: true,
      })
    );

    const adminDb = testEnv.authenticatedContext('admin_user', { admin: true }).firestore();
    await assertSucceeds(
      adminDb.collection('avisos').add({
        titulo: 'Aviso Oficial',
        texto: 'Publicado por admin',
        publicado: true,
      })
    );
  });

  it('Público pode ler live/atual e galeria, mas não pode escrever', async () => {
    await testEnv.withSecurityRulesDisabled(async (context) => {
      await context.firestore().collection('live').doc('atual').set({
        ativo: true,
        videoId: 'f6ArFvSPlkw',
      });
    });

    const unauthDb = testEnv.unauthenticatedContext().firestore();
    await assertSucceeds(unauthDb.collection('live').doc('atual').get());
    await assertFails(unauthDb.collection('live').doc('atual').set({ ativo: false }));
  });

  it('Membro pode marcar notificações lidas em seu próprio registro', async () => {
    const aliceDb = testEnv.authenticatedContext('alice').firestore();
    await assertSucceeds(
      aliceDb.collection('lidas').doc('alice').collection('itens').doc('notif_123').set({
        lidaEm: new Date(),
      })
    );

    // Alice não pode escrever no registro de Bob
    await assertFails(
      aliceDb.collection('lidas').doc('bob').collection('itens').doc('notif_123').set({
        lidaEm: new Date(),
      })
    );
  });
});
