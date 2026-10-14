---
target_identity: "file:C:\\Users\\HOME\\OneDrive\\Área de Trabalho\\convite 15 anos ester\\Portal Igreja\\templates\\public\\home.html"
target_fingerprint: "sha256:ad384ba213ff60231cf00fc2de51e2b66f638a4d075efd3b1c1f6061b155fced"
target_path: "C:\\Users\\HOME\\OneDrive\\Área de Trabalho\\convite 15 anos ester\\Portal Igreja\\templates\\public\\home.html"
timestamp: 2026-10-14T15-08-53Z
slug: templates-public-home-html
closed: true
---
### Design Health Score

| # | Heuristic | Score | Key Issue |
|---|-----------|-------|-----------|
| 1 | Visibility of System Status | 3 | Estado ativo na navegação e feedback de carregamento em formulários claro; transmissão ao vivo poderia indicar status offline mais explicitamente |
| 2 | Match System / Real World | 3 | Linguagem e tom eclesiásticos adequados e respeitosos; convenções de cultos e horários bem organizadas |
| 3 | User Control and Freedom | 3 | Navegação direta e menus de fácil retorno; formulários possuem cancelamento simples |
| 4 | Consistency and Standards | 3 | Fontes (*Playfair Display*, *Montserrat*, *Great Vibes*) e paleta oficial agora uniformizadas; anti-padrão de borda superior grossa em cards arredondados eliminado |
| 5 | Error Prevention | 3 | Validação nos inputs de contato e formulários; confirmação antes de deslogar no perfil |
| 6 | Recognition Rather Than Recall | 3 | Acesso imediato aos cultos, transmissão do YouTube e avisos principais sem exigir memorização |
| 7 | Flexibility and Efficiency | n/a | Surface pública/experiencial (landing page institucional sem fluxos complexos para power users) |
| 8 | Aesthetic and Minimalist Design | 3 | Estética sóbria e digna alinhada ao Ministério Luz da Palavra; remoção dos badges/eyebrows reduziu ruído visual |
| 9 | Error Recovery | 2 | Mensagens de erro de autenticação e formulário podem ser mais específicas sobre como prosseguir |
| 10 | Help and Documentation | n/a | Surface institucional/conversão; não requer manual de documentação |
| **Total** | | **23/32** | **Bom (B)** |

---

### Design Specificity Verdict

**LLM assessment**: A página inicial e as seções públicas possuem uma identidade visual única e digna, fortemente alinhada ao propósito do Ministério Luz da Palavra. A combinação de *Playfair Display* nos títulos com o preto sóbrio (`#080605`) da Hero e os tons de marrom (`#8C4303`) e ouro (`#BF871F`) cria uma atmosfera de reverência e autoridade eclesiástica. A assinatura em *Great Vibes* do Pastor Leonel traz calor e autenticidade pessoal. As correções recentes removeram elementos genéricos de SaaS (como badges em formato de pílula usados como subtítulos e bordas coloridas de 4px sobre cards arredondados), reforçando o caráter editorial do portal.

**Deterministic scan**: O scan determinístico (`impeccable detect`) reportou 0 violações críticas residuais após a limpeza dos anti-padrões `badge-editorial section-badge` e `border-accent-on-rounded` nos templates [home.html](file:///c:/Users/HOME/OneDrive/%C3%81rea%20de%20Trabalho/convite%2015%20anos%20ester/Portal%20Igreja/templates/public/home.html), [avisos.html](file:///c:/Users/HOME/OneDrive/%C3%81rea%20de%20Trabalho/convite%2015%20anos%20ester/Portal%20Igreja/templates/public/avisos.html), [cadastro.html](file:///c:/Users/HOME/OneDrive/%C3%81rea%20de%20Trabalho/convite%2015%20anos%20ester/Portal%20Igreja/templates/public/cadastro.html), [entrar.html](file:///c:/Users/HOME/OneDrive/%C3%81rea%20de%20Trabalho/convite%2015%20anos%20ester/Portal%20Igreja/templates/public/entrar.html) e [perfil.html](file:///c:/Users/HOME/OneDrive/%C3%81rea%20de%20Trabalho/convite%2015%20anos%20ester/Portal%20Igreja/templates/public/perfil.html).

**Visual overlays**: A inspeção via navegador confirmou que os blocos de conteúdo e tipografia estão alinhados aos tokens oficiais do design system, sem quebras de layout ou sobreposições.

---

### Overall Impression
O portal apresenta excelente presença visual com a hero imersiva e a identidade do Pastor Leonel. As seções inferiores agora respiram melhor sem o ruído dos badges repetitivos. O maior ponto de oportunidade reside na cadência rítmica entre as seções secundárias e no contraste fino dos botões secundários dourados contra fundos claros.

---

### What's Working
1. **Hero Aprovada e Imersiva**: A composição escura (`#080605`) com a galeria 3D curva e o retrato do Pastor Leonel estabelece um impacto solene imediato.
2. **Tipografia Nobre e Equilibrada**: A hierarquia com *Playfair Display* em títulos, *Montserrat* para leitura e *Great Vibes* para a assinatura pessoal do pastor dá o tom exato do ministério.
3. **Eliminação do Ruído de Badges**: A remoção dos "kickers/eyebrows" e o refinamento das bordas dos cards trouxeram sobriedade editorial às seções de cultos, transmissões e avisos.

---

### Priority Issues

- **[P1] Hierarquia e Contraste em Botões Secundários**
  - **Why it matters**: Botões com fundo dourado claro ou texto em ouro (`#BF871F`) sobre fundo claro podem apresentar contraste limítrofe para usuários com baixa acuidade visual.
  - **Fix**: Padronizar o token `--color-mlp-gold-text: #8A5F12` em todos os elementos de texto e bordas interativas sobre superfícies brancas/claras.
  - **Suggested command**: `/impeccable colorize`

- **[P1] Ritmo Vertical e Espaçamento de Seções no Mobile**
  - **Why it matters**: Em viewports estreitos (360px–390px), as margens entre as seções de Transmissões e Programação de Cultos estavam gerando saltos de respiro desiguais.
  - **Fix**: Padronizar `padding: var(--space-12) 0` ou `var(--space-16) 0` consistente em todas as seções públicas via `.section-container`.
  - **Suggested command**: `/impeccable layout`

- **[P2] Densidade de Informação e Cards de Avisos**
  - **Why it matters**: Na página de avisos e na listagem resumida, a data e a categoria competiam em peso visual com o título da mensagem.
  - **Fix**: Reduzir a espessura da metainformação para `font-size: 0.8125rem` em tom neutro médio (`#666`), deixando o título em *Playfair Display* guiar a leitura.
  - **Suggested command**: `/impeccable typeset`

- **[P2] Alinhamento e Espaçamento do Rodapé**
  - **Why it matters**: As colunas de links institucionais e informações de endereço no rodapé perdem simetria visual quando visualizadas em telas médias (768px a 1024px).
  - **Fix**: Ajustar o grid do rodapé para manter colunas balanceadas com `align-items: flex-start` e `gap: var(--space-8)`.
  - **Suggested command**: `/impeccable layout`

---

### Persona Red Flags

- **Alex (Membro Frequente / Busca Rápida)**: Ao procurar o horário do próximo culto pelo celular, a transição entre a hero e a grade de horários exige rolar por cards de transmissão antes de chegar na agenda semanal completa.
- **Jordan (Primeira Vez / Visitante)**: Visitante que quer conhecer a igreja precisa de um acesso imediato ao endereço e como chegar logo abaixo da mensagem de boas-vindas do pastor.

---

### Minor Observations
- O botão de "Voltar ao Topo" pode ter uma transição de fade-in mais sutil conforme o usuário rola a página.
- O favicon e as metatags OpenGraph devem refletir o logo e identidade oficiais do MLP.

---

### Questions to Consider
- O link direto para "Como Chegar / Endereço" deveria ter destaque fixo na seção de boas-vindas para novos visitantes?
- A seção de transmissão ao vivo do YouTube deveria exibir automaticamente o status do canal quando não houver culto em andamento?
