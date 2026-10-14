"""
Exportador estático para o portal do Ministério Luz da Palavra (MLP).
Gera arquivos HTML/CSS/JS/Mídia prontos para hospedar no GitHub Pages.
"""

import os
import sys
import shutil
import argparse
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

def export_site(base_path='portal-MLP', output_dir='dist'):
    print(f"=== Iniciando exportação estática do Portal MLP para GitHub Pages ===")
    print(f"Subcaminho base: /{base_path}/" if base_path else "Subcaminho base: / (raiz)")
    print(f"Diretório de saída: {output_dir}")

    # Define variável de ambiente antes de inicializar o Django
    os.environ['DJANGO_BASE_PATH'] = base_path
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mlp_portal.settings')
    os.environ['DJANGO_DEBUG'] = 'False'

    import django
    django.setup()

    from django.test import Client
    from django.urls import reverse
    from apps.events.models import Event
    from apps.gallery.models import Album
    from apps.media_library.models import MediaItem
    from apps.pages.models import InstitutionalPage

    out = BASE_DIR / output_dir
    if out.exists():
        shutil.rmtree(out)
    out.mkdir(parents=True, exist_ok=True)

    # 1. Coleta e cópia de arquivos estáticos
    print("\n1. Copiando arquivos estáticos...")
    if (BASE_DIR / 'package.json').exists():
        try:
            import subprocess
            print("   Compilando assets Vite/React (Hero 3D)...")
            subprocess.run('npm run build', check=True, cwd=str(BASE_DIR), shell=True)
            print("   [OK] Bundle Vite/React compilado com sucesso")
        except Exception as e:
            print(f"   [AVISO] Nao foi possivel compilar bundle Vite: {e}")

    from django.core.management import call_command
    call_command('collectstatic', interactive=False, verbosity=0)

    static_src = BASE_DIR / 'staticfiles'
    static_dest = out / 'static'
    if static_src.exists():
        shutil.copytree(static_src, static_dest, dirs_exist_ok=True)
        print(f"   [OK] Arquivos estaticos copiados para {static_dest}")

    # 2. Cópia de arquivos de mídia (se existirem)
    media_src = BASE_DIR / 'media'
    media_dest = out / 'media'
    if media_src.exists() and any(media_src.iterdir()):
        shutil.copytree(media_src, media_dest, dirs_exist_ok=True)
        print(f"   [OK] Arquivos de midia copiados para {media_dest}")
    else:
        media_dest.mkdir(parents=True, exist_ok=True)

    # 3. Criação de arquivo .nojekyll (obrigatório para GitHub Pages)
    (out / '.nojekyll').touch()
    print("   [OK] Arquivo .nojekyll criado")

    # 4. Mapeamento de rotas canônicas
    client = Client()
    routes = [
        (reverse('public:home'), 'index.html'),
        (reverse('public:legacy'), 'legado-pastor-leonel/index.html'),
        (reverse('public:history'), 'nossa-historia/index.html'),
        (reverse('public:events'), 'agenda-cultos/index.html'),
        (reverse('public:gallery'), 'acervo-fotografico/index.html'),
        (reverse('public:media'), 'mensagens-e-ao-vivo/index.html'),
        (reverse('public:contact'), 'contato-e-horarios/index.html'),
        (reverse('public:entrar'), 'entrar/index.html'),
        (reverse('public:cadastro'), 'cadastro/index.html'),
        (reverse('public:perfil'), 'perfil/index.html'),
    ]

    # Rotas dinâmicas do banco
    for ev in Event.published.all():
        routes.append((reverse('public:event_detail', kwargs={'slug': ev.slug}), f'agenda-cultos/{ev.slug}/index.html'))

    for alb in Album.published.all():
        routes.append((reverse('public:album_detail', kwargs={'slug': alb.slug}), f'acervo-fotografico/{alb.slug}/index.html'))

    for med in MediaItem.published.all():
        routes.append((reverse('public:media_detail', kwargs={'slug': med.slug}), f'mensagens-e-ao-vivo/{med.slug}/index.html'))

    for pg in InstitutionalPage.published.all():
        routes.append((reverse('public:page_detail', kwargs={'slug': pg.slug}), f'pagina/{pg.slug}/index.html'))

    print(f"\n2. Gerando paginas HTML ({len(routes)} rotas)...")
    visited_files = set()

    for url, file_rel in routes:
        if file_rel in visited_files:
            continue
        visited_files.add(file_rel)

        file_path = out / file_rel
        file_path.parent.mkdir(parents=True, exist_ok=True)

        # Com FORCE_SCRIPT_NAME ativo, reverse() já retorna URLs prefixadas.
        # O test client espera a URL completa com o prefixo.
        resp = client.get(url)
        if resp.status_code == 200:
            content = resp.content.decode('utf-8')
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"   [OK] [200 OK] {url} -> {file_rel}")
        else:
            print(f"   [AVISO] [ERRO {resp.status_code}] Falha ao exportar {url}")

    # Criação de 404.html amigável para o GitHub Pages
    home_file = out / 'index.html'
    if home_file.exists():
        shutil.copy(home_file, out / '404.html')
        print("   [OK] 404.html gerado a partir da pagina principal")

    print(f"\n=== Exportação concluída com sucesso em: {out} ===")
    return out

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Exportar Portal MLP para GitHub Pages')
    parser.add_argument('--repo', default='portal-MLP', help='Nome do repositório no GitHub para o subcaminho base (default: portal-MLP)')
    parser.add_argument('--out', default='dist', help='Diretório de saída (default: dist)')
    args = parser.parse_args()

    export_site(base_path=args.repo, output_dir=args.out)
