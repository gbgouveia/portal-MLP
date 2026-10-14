# Product

<!-- impeccable:product-schema 1 -->

## Platform

web

## Stack

Django + Firebase (Authentication, Firestore, Storage, Cloud Functions, Firebase Cloud Messaging / FCM).
Sem Three.js ou outras bibliotecas 3D/gráficas pesadas sem necessidade real.

## Users

- **Membros e Famílias da Igreja:** Acompanham cultos ao vivo, avisos e notificações (com sininho), galerias de fotos, participam do cadastro e gestão de irmãos e recebem comunicações oficiais por WhatsApp.
- **Visitantes e Novos Convertidos:** Conhecem o ministério, localização, horários e assistem às pregações e transmissões.
- **Liderança Pastoral e Equipe Administrativa:** Gerenciam o cadastro dos irmãos, publicações, avisos, notificações por sininho, disparos via API oficial do WhatsApp e mídias no Firebase.
- **Público Geral e Admiradores:** Conhecem a história real e o legado do Pastor Leonel através do memorial documental.

## Product Purpose

Portal oficial e sistema comunitário do **Ministério Luz da Palavra (MLP)**. Unifica o portal público institucional e o memorial do Pastor Leonel com os serviços de gestão e comunicação da igreja: cadastro e gestão dos irmãos, avisos e notificações com sininho, galeria de fotos integrada ao Firebase, transmissão automática de lives do YouTube e avisos por WhatsApp via API oficial.

## Positioning

Portal ministerial solene, autêntico e funcional: combina a honra e preservação fidedigna do legado pastoral do Pastor Leonel (sem invenções) com ferramentas práticas de comunhão, acolhimento e comunicação ativa para os membros no dia a dia.

## Operating Context

- Acesso diário e durante os cultos tanto em dispositivos móveis (notificações push, avisos de sininho, mensagens no WhatsApp, visualização de fotos) quanto em desktop.
- Transmissões ao vivo sincronizadas automaticamente com o canal oficial do YouTube (`@MLPBRASILIA-DF`).
- Gestão de membros e mídias centralizada com autenticação e banco em nuvem via Firebase.

## Capabilities and Constraints

- **Capacidades Oficiais:**
  - **Hero Aprovada (Inalterável):** Galeria 3D curva (`TiltedGridHero`), retrato do Pastor Leonel e o título *"MINISTÉRIO / Luz da Palavra / Pastor Leonel"*. Componente `src/components/ui/tilted-grid-hero.tsx` preservado integralmente. Não redesenhar, não trocar de técnica e não reescrever a lógica.
  - **Portal Público:** Apresentação institucional, memorial pastoral, horários de cultos e eventos reais.
  - **Cadastro e Gestão de Irmãos:** Registro estruturado de membros e famílias.
  - **Avisos com Sininho:** Sistema de notificações de comunicados importantes.
  - **Galeria no Firebase:** Armazenamento e exibição de fotos e álbuns no Firebase Storage / Firestore.
  - **Live do YouTube Automática:** Integração direta com o canal oficial do YouTube (`Channel ID: UCkvN5Uqsjhj6lSpIX5JhBpA`, `@MLPBRASILIA-DF`).
  - **Avisos por WhatsApp:** Integração oficial via API do WhatsApp para comunicados ministeriais.
- **Restrições Rígidas de Conteúdo:**
  - **Conteúdo 100% Real (Nada Inventado):** Proibido criar ou inventar datas, nomes, fatos históricos, depoimentos, endereços ou telefones. Onde a informação real não estiver disponível, manter espaço reservado claramente demarcado.
  - **Restrições Técnicas:** Não adicionar Three.js nem bibliotecas pesadas de animação/3D além do CSS 3D nativo já implementado no componente aprovado da hero.

## Brand Commitments

- **Nome Oficial:** Ministério Luz da Palavra (MLP) / Pastor Leonel.
- **Paleta Oficial (Insubstituível):**
  - Marrom: `#8C4303`
  - Ouro: `#BF871F`
  - Dourado Claro: `#F2D16D`
  - Terra: `#A6754B`
  - Claro: `#F2F1F0`
  - Preto da Hero: `#080605`
- **Tipografia Oficial (Insubstituível):**
  - Títulos: *Playfair Display*
  - Corpo e Menu: *Montserrat*
  - Assinatura "Pastor Leonel": *Great Vibes*
- **Canal Oficial do YouTube:**
  - URL: [https://www.youtube.com/@MLPBRASILIA-DF](https://www.youtube.com/@MLPBRASILIA-DF)
  - Channel ID: `UCkvN5Uqsjhj6lSpIX5JhBpA`

## Evidence on Hand

- Componente de Hero Aprovado: `src/components/ui/tilted-grid-hero.tsx` (CSS 3D puro com slices/cilindro curvo, sem Three.js).
- Configurações e regras do Firebase no projeto (`firebase.json`, `firestore.rules`, `storage.rules`, `.firebaserc`).
- Backend Django configurado em `apps/` e `mlp_portal/`.
- Canal do YouTube e identificadores oficiais validados.

## Product Principles

1. **Veracidade e Integridade Histórica:** Nenhum dado biográfico, data ou testemunho é inventado. A verdade dos fatos rege todo o conteúdo; dados ausentes são indicados com espaços reservados.
2. **Preservação Visual da Hero:** A Hero com galeria curva 3D, retrato do Pastor Leonel e tipografia oficial é consagrada e mantida sem alterações estruturais ou substituições técnicas.
3. **Comunicação Direta e Acolhimento:** Os irmãos são alcançados onde estão (sininho na plataforma, WhatsApp oficial e lives instantâneas).
4. **Desempenho Sem Peso Desnecessário:** Arquitetura leve (Django + Firebase), sem inclusão de engines 3D pesadas como Three.js.

## Accessibility & Inclusion

- Conformidade com padrões de contraste entre os tons dourados/claros e o fundo escuro/marrom.
- Tipografia legível com Montserrat para corpo de texto em tamanhos adequados para todas as faixas etárias.
- Degradação funcional limpa e navegação por teclado.
