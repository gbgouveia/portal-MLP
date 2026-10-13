# Ministério Luz da Palavra (MLP) — Portal Institucional & Legado Pastoral

> *“Uma história construída pela fé. Um legado que atravessa gerações. Um ministério que continua.”*

Portal institucional histórico, experiência digital autoral e acervo memorial do **Ministério Luz da Palavra**, tendo o legado pastoral do **Pastor Leonel** como protagonista da experiência.

---

## 1. Visão Geral da Arquitetura

O sistema foi concebido sob uma arquitetura limpa, modular e sustentável em **Python 3.14 + Django 6.1**, priorizando renderização rápida, acessibilidade semântica, governança de dados e preservação histórica de acervos.

### Aplicações Modulares por Domínio (`apps/`):
- `accounts`: Modelo de usuário customizado (`User`) com papéis institucionais baseados no princípio do menor privilégio (`ADMIN`, `INSTITUTIONAL_EDITOR`, `MEDIA_TEAM`, `EVENT_MANAGER`, `REVIEWER`).
- `core`: Modelo base abstrato de publicação editorial (`PublishableModel`), querysets de rascunho/publicado/arquivado e comando `setup_mlp`.
- `institutional`: Configurações oficiais (Singleton), liderança ministerial, frentes de ministério e grade oficial de cultos.
- `legacy`: Eixo narrativo central — Perfil biográfico do Pastor Leonel, Linha do Tempo Histórica interativa (anos 1970 ao presente com suporte a datas aproximadas), documentos digitalizados e testemunhos autorizados.
- `events`: Agenda de celebrações e congressos com categorização e integração com álbuns e vídeos.
- `gallery`: Acervo fotográfico documental, álbuns com distinção histórica e contemporânea, upload em lote de fotos e visualizador Lightbox acessível por teclado.
- `media_library`: Catálogo de pregações gravadas, estudos e player oficial de transmissão ao vivo do YouTube com ativação em 1 clique.
- `pages`: Páginas institucionais dinâmicas, editáveis e com histórico de revisões.
- `dashboard`: Painel administrativo próprio, visualmente integrado à paleta institucional, com indicadores calculados de dados reais.
- `audit`: Trilha de auditoria imutável (`AuditLog`) para conformidade e rastreabilidade.

---

## 2. Identidade Visual & Design System Editorial

- **Paleta Canônica:**
  - Vinho Histórico: `#35231F`
  - Marfim Documental: `#F7F2E9`
  - Dourado Discreto: `#A57A22`
  - Cinza Documental: `#6A625A`
  - Branco Puro: `#FFFFFF`
- **Tipografia:** *Cinzel* (display monumental), *Libre Baskerville* (títulos e citações editoriais), *Inter* (interface, navegação e leitura fluida).
- **Movimento e Animações com Propósito:**
  - **GSAP & ScrollTrigger:** Coreografia suave na entrada do Hero e revelação progressiva da Linha do Tempo.
  - **Three.js:** Experiência espacial memorial abstrata com partículas sutis de luz e poeira do tempo, com pausa automática via `IntersectionObserver` e suporte estrito a `prefers-reduced-motion`.
  - **Anime.js:** Micro-interações vetoriais nos nós da timeline sem conflito com o GSAP.
  - **Acessibilidade:** Nenhum conteúdo essencial depende de JavaScript para ser lido; total navegação por teclado e conformidade com WCAG 2.1 AA.

---

## 3. Instruções de Instalação e Execução

### Pré-requisitos:
- Python 3.12+ (testado e validado em Python 3.14)
- Pip

### 1. Clonar e Acessar o Diretório:
```bash
git clone <url-do-repositorio>
cd "Portal Igreja"
```

### 2. Instalar Dependências:
```bash
pip install django pillow python-dotenv
```

### 3. Configurar Variáveis de Ambiente (`.env`):
Crie um arquivo `.env` na raiz do projeto (opcional, já há fallbacks seguros para desenvolvimento local):
```env
DJANGO_SECRET_KEY=sua-chave-secreta-de-producao
DJANGO_DEBUG=True
DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1
# Para produção com PostgreSQL:
# DATABASE_URL=postgresql://usuario:senha@localhost:5432/mlp_db
```

### 4. Executar Migrações e Inicializar Dados do Ministério:
```bash
python manage.py migrate
python manage.py setup_mlp
```
O comando `setup_mlp` cria automaticamente:
- Grupos de permissão institucionais.
- Configurações do Ministério Luz da Palavra (fundação em 1970).
- Perfil do Pastor Leonel e marcos iniciais da Linha do Tempo (1970–2026).
- Usuário administrador padrão:
  - **Usuário:** `admin`
  - **Senha:** `admin_mlp_password_2026` *(Altere imediatamente no primeiro login em ambiente de produção)*

### 5. Iniciar o Servidor de Desenvolvimento:
```bash
python manage.py runserver
```
- **Portal Público:** [http://127.0.0.1:8000/](http://127.0.0.1:8000/)
- **Painel MLP:** [http://127.0.0.1:8000/painel/](http://127.0.0.1:8000/painel/)
- **Admin Técnico:** [http://127.0.0.1:8000/admin-tecnico/](http://127.0.0.1:8000/admin-tecnico/)

---

## 4. Execução dos Testes Automatizados

Para rodar a suíte completa de testes de integridade, modelos, segurança e rotas públicas:
```bash
python manage.py test
```
Resultados esperados: 14 testes executados com 100% de aprovação (OK).

---

## 5. Diretrizes de Curadoria e Governança
1. **Veracidade Histórica:** Não invente fotografias, citações ou datas do Pastor Leonel. Quando dados de dia ou mês forem aproximados, utilize o campo de datação apropriada.
2. **Proteção de Mídia:** Armazenamento seguro de uploads em diretório `media/` fora do versionamento de código.
3. **Auditoria:** Todas as alterações relevantes são registradas no modelo `AuditLog`.
