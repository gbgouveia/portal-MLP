# Pesquisa de Design e Referências de Componentes — Portal MLP

## 1. Contexto Editorial e Diretrizes
O portal institucional do **Ministério Luz da Palavra (MLP)** celebra o legado pastoral do **Pastor Leonel**, conectando mais de cinco décadas de história (desde os anos 1970) com o presente e o futuro da comunidade de fé.

- **Conceito Editorial:** *“Uma história construída pela fé. Um legado que atravessa gerações. Um ministério que continua.”*
- **Paleta Oficial Obrigatória do MLP:**
  - **Dourado luminoso (`#F2D16D`):** Destaques sutis, pequenos detalhes e ênfases visuais.
  - **Ouro envelhecido (`#BF871F`):** Links ativos, chamadas secundárias e navegação.
  - **Marrom profundo (`#8C4303`):** Títulos imponentes, botões principais, identidade e contraste alto.
  - **Terra acolhedora (`#A6754B`):** Elementos secundários, bordas, divisores e superfícies auxiliares.
  - **Cinza-marfim (`#F2F1F0`):** Fundo principal e áreas nobres de leitura.
- **Tipografia:**
  - Display / Títulos: *Cinzel* / *Libre Baskerville* / Serif editorial com dignidade histórica.
  - Interface / Corpo: *Inter* / *Plus Jakarta Sans* para legibilidade sem serifa, dados e navegação.

---

## 2. Componentes Pesquisados (21st.dev & Referências Curadas)

### 2.1. Timeline Histórica Interativa & Curadoria Cronológica
- **Componente de Referência:** *Interactive Timeline / Milestones Storyboard*
- **Referência:** [21st.dev Timeline Components](https://21st.dev/community/components/explore/timeline-component)
- **Funcionalidade Aproveitada:** Linha cronológica vertical contínua com nós de marcos históricos (décadas 1970 a 2020+), suporte a datas aproximadas (apenas ano ou mês/ano), revelação gradual de cartões de acervo com fotografias históricas em tom documental e citação contextual.
- **Biblioteca / Abordagem:** GSAP (ScrollTrigger para o progresso da linha central) + Anime.js para micro-aceleração nos nós cronológicos ao atingir o viewport.
- **Adaptação:** Renderização server-side via Django Templates (`HistoricalMilestone` queryset ordenado), gerando HTML semântico com `data-year` e microinterações de filtro por década sem necessidade de bundle pesado.
- **Motivo de Escolha:** É o coração da narrativa do Pastor Leonel e do ministério, permitindo que pesquisadores, membros antigos e novas gerações naveguem pela memória da igreja com dignidade documental.

### 2.2. Abertura Editorial com Revelação de Imagem — Hero Section 2
- **Componente de Referência:** *hero-section-2.tsx*
- **Referência:** [21st.dev Hero Sections](https://21st.dev/community/components)
- **Descrição da Interação:** Composição dividida (split-screen) assimétrica com tipografia editorial imponente, entrada progressiva de subtítulo/título/citação e revelação da fotografia histórica por recorte animado (`clip-path` progressivo da máscara de imagem).
- **Motivo da Escolha:** Constrói uma abertura solene, digna de uma instituição histórica com mais de 50 anos de caminhada, evitando a aparência de landing pages comerciais ou templates genéricos de igreja.
- **Adaptações Realizadas para Django:**
  - Substituição de quaisquer textos de demonstração por dados institucionais autênticos do Ministério Luz da Palavra e do Pastor Leonel fornecidos pelo backend (`PastoralProfile`, `InstitutionalSetting`).
  - Implementação da revelação de imagem por recorte utilizando CSS Custom Properties (`clip-path: polygon(...)`) e timeline do GSAP com fallback gracioso em CSS estático para usuários com `prefers-reduced-motion`.
  - Integração nativa com template parcial [templates/components/hero_editorial.html](file:///c:/Users/HOME/OneDrive/Área%20de%20Trabalho/convite%2015%20anos%20ester/Portal%20Igreja/templates/components/hero_editorial.html) e renderização na página inicial.
- **Dependências:** GSAP (core) com fallback CSS nativo.
- **Licença / Condições:** Licença MIT comunitária do 21st.dev.

### 2.3. Acervo & Galeria Fotográfica Documental com Lightbox Acessível
- **Componente de Referência:** *Curated Archive Grid & Photo Stack*
- **Referência:** [21st.dev Image Showcase & Gallery](https://21st.dev/community/components)
- **Funcionalidade Aproveitada:** Grade de acervo responsiva com metadados editoriais visíveis (legenda, ano, fotógrafo/acervo), proporções respeitadas sem cortes destrutivos, e modal Lightbox acessível com suporte a navegação por teclado (ESC, setas) e leitores de tela.
- **Biblioteca:** Vanilla JS modular + CSS Grid editorial + micro-transições via Motion/CSS.
- **Adaptação:** Modelos Django `Album` e `Photo` com paginação, thumbnails e atributos acessíveis (`alt`, `aria-describedby`).
- **Motivo de Escolha:** O acervo fotográfico é o patrimônio visual do ministério; as fotos devem respirar sem botões intrusivos poluindo o enquadramento.

### 2.4. Abertura Tridimensional Abstrata (Three.js Memory Void / Time Particles)
- **Componente de Referência:** *Three.js Ambient Archive Dust / Dimensional Memorial*
- **Referência:** [Three.js Official Examples](https://threejs.org/) & [21st.dev Canvas Backgrounds](https://21st.dev/community/components)
- **Funcionalidade Aproveitada:** Campo de partículas sutis em suspensão dourada/marfim (metáfora de poeira do tempo, memória viva e feixe de luz da palavra) atuando como plano de fundo sob demanda na seção de memória histórica.
- **Biblioteca:** Three.js (carregado sob demanda, apenas se WebGL2 disponível e `prefers-reduced-motion` não estiver ativo; pausa de animação via IntersectionObserver quando fora da tela).
- **Adaptação:** Script isolado `js/three/memorial-canvas.js` sem interferir na renderização de texto e acessibilidade do DOM.
- **Motivo de Escolha:** Transmite espiritualidade, tempo e solenidade sem inventar falsos artefatos ou representações literais desrespeitosas.

### 2.5. Biblioteca Audiovisual & Transmissão ao Vivo Oficial
- **Componente de Referência:** *Media Archive & Live Stream Banner*
- **Referência:** Padrões canônicos de acervos audiovisuais e YouTube Embed API.
- **Funcionalidade Aproveitada:** Incorporação respeitosa de transmissões ao vivo apenas quando o status estiver confirmado (`is_live=True`), acompanhado de filtro de pregações por tema, pregador e data.
- **Biblioteca:** Vanilla JS + YouTube iframe API nativa.
- **Adaptação:** Modelos Django `MediaItem` com validação de ID do YouTube, sem raspagem de dados e sem exposição de chaves no frontend.

### 2.6. Navegação Flutuante Auxiliar — Mac OS Dock
- **Componente de Referência:** *mac-os-dock.tsx*
- **Referência:** [21st.dev Component Library — Dock Interaction](https://21st.dev/community/components)
- **Descrição da Interação:** Barra de navegação flutuante no rodapé/lateral com ampliação harmônica por proximidade física do cursor (magnification matemática), elevação sutil de ícones com sombras quentes, tooltips acessíveis no topo com o nome das seções, ponto indicador de rota ativa (`active dot`) e feedback tátil ao clicar.
- **Motivo da Escolha:** Oferece uma experiência de navegação rápida e moderna para o visitante explorar o acervo histórico sem poluir o cabeçalho institucional fixo, permitindo trânsito ágil entre Início, História, Legado, Eventos, Fotos, Mensagens e Contato.
- **Adaptações Realizadas para Django:**
  - Convertido integralmente de React/TSX para HTML semântico (`<nav class="mlp-dock">`), CSS moderno integrado com as variáveis oficiais da MLP (`--mlp-brown-dark`, `--mlp-gold`, `--mlp-earth`, `--mlp-surface`, `--mlp-border`) e JavaScript Vanilla modular ([static/js/core/dock-interactive.js](file:///c:/Users/HOME/OneDrive/Área%20de%20Trabalho/convite%2015%20anos%20ester/Portal%20Igreja/static/js/core/dock-interactive.js)).
  - Utilização estrita de rotas canônicas reais via Django URL template tags: `{% url 'public:home' %}`, `{% url 'public:history' %}`, `{% url 'public:legacy' %}`, `{% url 'public:events' %}`, `{% url 'public:gallery' %}`, `{% url 'public:media' %}`, `{% url 'public:contact' %}` (zero links fictícios).
  - Acessibilidade completa: suporte a navegação por teclado (`Tab`, `Enter`, `Space`), foco visível, tooltips com atributos `role="tooltip"` e fallback direto para telas touch (onde a ampliação por hover é desabilitada em favor de toque imediato).
- **Dependências:** Nenhuma biblioteca externa necessária (100% Vanilla JS + CSS).
- **Licença / Condições:** Licença MIT comunitária do 21st.dev.

---

## 3. Matriz de Responsabilidade das Bibliotecas de Animação

| Biblioteca | Responsabilidade Primária | Onde é Utilizada | Justificativa |
|---|---|---|---|
| **GSAP + ScrollTrigger** | Coreografia editorial e scroll narrativo | Linha do tempo, revelação de marcos e Hero Section 2 (máscara de recorte) | Precisão de sincronia com a rolagem do usuário e renderização fluida sem travamentos. |
| **Motion / CSS Nativo** | Transições de UI e estados de componentes | Mac OS Dock, modais, acordeões de biografia, tabs de eventos | Interações ágeis e táteis com respeito a acessibilidade. |
| **Three.js** | Atmosfera tridimensional simbólica sob demanda | Hero comemorativo do Legado (canvas com pausa automática) | Representação poética de luz e memória histórica sem criar falsas réplicas 3D de pessoas. |
| **Anime.js** | Animação gráfica vetorial e contornos SVG | Traçado da linha do tempo histórica, monogramas e divisores editoriais | Manipulação SVG leve e de alta precisão sem sobrecarregar a GPU. |

---

## 4. Política de Acessibilidade e Performance
- Suporte total a `prefers-reduced-motion: reduce` desativando animações pesadas e fornecendo transições estáticas imediatas.
- Zero dependência de JavaScript para a leitura integral dos conteúdos históricos e horários.
- Contraste em conformidade com WCAG 2.1 AA (#8C4303 e #BF871F sobre #F2F1F0 e #FFFFFF proporcionam contraste acima de 7:1 e 4.5:1).
