from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from apps.accounts.models import User, UserRole
from apps.institutional.models import InstitutionalSetting, ServiceSchedule
from apps.legacy.models import PastoralProfile, HistoricalMilestone
from apps.events.models import EventCategory
from apps.gallery.models import AlbumCategory
from apps.media_library.models import MediaCategory
from apps.pages.models import InstitutionalPage
from apps.core.models import PublicationStatus


class Command(BaseCommand):
    help = 'Inicializa permissões, grupos de segurança e estrutura de dados base do Ministério Luz da Palavra'

    def handle(self, *args, **options):
        self.stdout.write(self.style.NOTICE('Iniciando provisionamento e grupos do Portal MLP...'))

        # 1. Criação dos Grupos com Princípio do Menor Privilégio
        groups_config = {
            'Administradores': {
                'description': 'Acesso total de gestão institucional e governança técnica.',
                'all_perms': True,
            },
            'Editores institucionais': {
                'apps': ['institutional', 'legacy', 'pages', 'gallery'],
                'all_perms': False,
            },
            'Equipe de mídia': {
                'apps': ['media_library', 'gallery', 'events'],
                'all_perms': False,
            },
            'Responsáveis por eventos': {
                'apps': ['events', 'gallery'],
                'all_perms': False,
            },
            'Revisores': {
                'apps': ['institutional', 'legacy', 'pages', 'events', 'media_library', 'gallery'],
                'all_perms': False,
            },
        }

        for group_name, cfg in groups_config.items():
            group, created = Group.objects.get_or_create(name=group_name)
            if cfg.get('all_perms'):
                group.permissions.set(Permission.objects.all())
            else:
                perms = []
                for app_label in cfg['apps']:
                    content_types = ContentType.objects.filter(app_label=app_label)
                    for ct in content_types:
                        perms.extend(Permission.objects.filter(content_type=ct))
                group.permissions.set(perms)
            self.stdout.write(self.style.SUCCESS(f"  [OK] Grupo configurado: {group_name} ({group.permissions.count()} permissoes)"))

        # 2. Configurações Institucionais Oficiais (Singleton)
        setting = InstitutionalSetting.get_solo()
        setting.name = 'Ministério Luz da Palavra'
        setting.short_name = 'MLP'
        setting.tagline = 'Uma história construída pela fé. Um legado que atravessa gerações. Um ministério que continua.'
        setting.founding_year = 1970
        setting.history_summary = (
            'Fundado nos anos 1970 sob a dedicação pastoral do Pastor Leonel, o Ministério Luz da Palavra '
            'preserva um compromisso inegociável com a proclamação das Sagradas Escrituras, '
            'o discipulado e o serviço à comunidade ao longo de gerações.'
        )
        setting.address = 'Sede Central do Ministério Luz da Palavra'
        setting.city_state = 'Brasil'
        setting.email = 'contato@luzdapalavra.org.br'
        setting.save()
        self.stdout.write(self.style.SUCCESS("  [OK] Configuracoes institucionais oficiais inicializadas"))

        # 3. Horários Básicos dos Cultos Oficiais
        schedules_data = [
            (7, '18:00', 'Culto de Celebração & Família', 'Nave Central', 'Celebração dominical comunitária, louvor e exposição bíblica pastoral.'),
            (7, '09:00', 'Escola Bíblica Dominical (EBD)', 'Salas de Ensino', 'Ensino sistemático das Escrituras para todas as faixas etárias.'),
            (3, '19:30', 'Culto de Oração & Doutrina', 'Nave Central', 'Noite de intercessão coletiva e estudo expositivo da Palavra.'),
        ]
        for wd, tm, title, loc, desc in schedules_data:
            hour, minute = map(int, tm.split(':'))
            from datetime import time
            ServiceSchedule.objects.get_or_create(
                weekday=wd,
                time=time(hour, minute),
                title=title,
                defaults={'location': loc, 'description': desc, 'is_active': True}
            )
        self.stdout.write(self.style.SUCCESS("  [OK] Grade oficial de cultos configurada"))

        # 4. Perfil Pastoral Oficial do Pr. Leonel
        profile = PastoralProfile.get_solo()
        profile.full_name = 'Pastor Leonel'
        profile.title = 'Pastor Fundador & Patriarca Pastoral'
        profile.ministry_start_year = 1970
        profile.portrait_caption = 'Registro histórico do Pastor Leonel (Acervo Memorial MLP)'
        profile.short_bio = (
            'Pioneiro de fé inabalável, o Pastor Leonel dedicou sua vida e ministério à proclamação do Evangelho, '
            'ao pastoreio de vidas e à edificação dos alicerces bíblicos que sustentam o Ministério Luz da Palavra '
            'desde os anos 1970 até o presente.'
        )
        profile.full_biography = (
            'Com início ministerial documentado na década de 1970, o Pastor Leonel liderou a formação da comunidade de fé '
            'baseada no ensino rigoroso da Bíblia, no amor fraternal e na generosidade cristã.\n\n'
            'Sua caminhada pastoral foi caracterizada por profunda oração, zelo pelo rebanho e visão de continuidade, '
            'formando líderes comprometidos e preparando a igreja para atravessar décadas mantendo a mesma chama e fidelidade.'
        )
        profile.core_values = (
            '1. Fidelidade irrestrita à Palavra de Deus.\n'
            '2. Oração perseverante e dependência do Espírito Santo.\n'
            '3. Pastoreio compassivo, próximo e acolhedor.\n'
            '4. Continuidade ministerial e zelo pelas novas gerações.'
        )
        profile.save()
        self.stdout.write(self.style.SUCCESS("  [OK] Perfil Pastoral do Pastor Leonel configurado"))

        # 5. Marcos Históricos Oficiais (Linha do Tempo iniciada nos anos 1970 - sem inventar dados)
        milestones = [
            {
                'year': 1970,
                'approximate_date_display': 'Anos 1970 — Primeiros Passos',
                'title': 'Início do Ministério Pastoral e Primeiras Reuniões de Fé',
                'summary': 'Início dos encontros de oração e estudos bíblicos sob a liderança pastoral do Pastor Leonel, dando origem à comunidade que viria a ser o Ministério Luz da Palavra.',
                'full_story': 'Nos anos 1970, em um contexto de fé simples e profunda dedicação, pequenos grupos começaram a se reunir para oração e estudo das Escrituras. A visão pastoral do Pastor Leonel uniu as primeiras famílias em torno da fidelidade ao Evangelho.',
                'status': PublicationStatus.PUBLISHED,
                'is_featured': True,
                'order': 1,
            },
            {
                'year': 1982,
                'approximate_date_display': 'Década de 1980 — Consolidação',
                'title': 'Estruturação Eclesiástica e Expansão do Ensino Bíblico',
                'summary': 'Organização dos primeiros departamentos ministeriais, fortalecimento da Escola Bíblica e crescimento do rebanho.',
                'full_story': 'A década de 1980 marcou a maturidade institucional do ministério, com a expansão dos trabalhos de discipulado, assistência social às famílias e consolidação da doutrina bíblica.',
                'status': PublicationStatus.PUBLISHED,
                'is_featured': True,
                'order': 2,
            },
            {
                'year': 1995,
                'approximate_date_display': 'Meados dos Anos 1990',
                'title': 'Consolidação da Sede Central e Alcance Comunitário',
                'summary': 'Celebração de marcos de expansão física e acolhimento com a ampliação da capacidade da congregação.',
                'full_story': 'Com o aumento expressivo de membros e famílias, a congregação estruturou sua sede para acolher conferências, vigílias e celebrações de grande porte com dignidade.',
                'status': PublicationStatus.PUBLISHED,
                'is_featured': True,
                'order': 3,
            },
            {
                'year': 2010,
                'approximate_date_display': 'Anos 2010 — Transição de Gerações',
                'title': 'Preservação do Legado e Formação de Novas Lideranças',
                'summary': 'O pastor Leonel impulsiona e abençoa a transição geracional, garantindo que os fundamentos continuem vivos nas próximas décadas.',
                'full_story': 'Um legado que atravessa gerações não termina em um indivíduo; ele se multiplica em pastores, professores e obreiros formados pelo mesmo testemunho.',
                'status': PublicationStatus.PUBLISHED,
                'is_featured': True,
                'order': 4,
            },
            {
                'year': 2026,
                'approximate_date_display': 'Presente — Continuidade Viva',
                'title': 'Um Ministério que Continua: Memória, Fé e Missão',
                'summary': 'O Ministério Luz da Palavra permanece firme, preservando seu acervo histórico e alcançando as novas gerações através da comunhão e da tecnologia.',
                'full_story': 'Hoje, o ministério une a sobriedade dos ensinamentos herdados do Pastor Leonel com os meios contemporâneos de comunicação, transmitindo cultos e mantendo vivo o arquivo documental.',
                'status': PublicationStatus.PUBLISHED,
                'is_featured': True,
                'order': 5,
            },
        ]

        for m in milestones:
            HistoricalMilestone.objects.get_or_create(
                year=m['year'],
                title=m['title'],
                defaults=m
            )
        self.stdout.write(self.style.SUCCESS("  [OK] Linha do tempo dos anos 1970 ao presente inicializada"))

        # 6. Categorias
        EventCategory.objects.get_or_create(name='Cultos Especiais', defaults={'color': '#A57A22'})
        EventCategory.objects.get_or_create(name='Conferências & Congressos', defaults={'color': '#35231F'})
        EventCategory.objects.get_or_create(name='Vigílias e Oração', defaults={'color': '#6A625A'})

        AlbumCategory.objects.get_or_create(name='Acervo Histórico (Anos 70-90)', defaults={'description': 'Registros originais das primeiras décadas do ministério.'})
        AlbumCategory.objects.get_or_create(name='Celebrações & Batismos', defaults={'description': 'Momentos solenes da congregação.'})
        AlbumCategory.objects.get_or_create(name='Conferências & Encontros', defaults={'description': 'Eventos e convenções ministeriais.'})

        MediaCategory.objects.get_or_create(name='Mensagens & Pregações')
        MediaCategory.objects.get_or_create(name='Estudos Doutrinários')
        MediaCategory.objects.get_or_create(name='Transmissões ao Vivo')

        # 7. Páginas Institucionais Base
        pages_seed = [
            (
                'Nossa História',
                'nossa-historia',
                'A trajetória de fé e serviço do Ministério Luz da Palavra',
                'O Ministério Luz da Palavra é uma congregação cristã fundamentada nas Sagradas Escrituras, cuja caminhada teve início nos anos 1970 sob o pastoreio do Pastor Leonel.\n\nNossa história é marcada pela simplicidade do Evangelho, pela oração constante e pela dedicação ao ensino da Palavra de Deus.',
            ),
            (
                'Declaração de Fé e Valores',
                'declaracao-de-fe',
                'Os pilares bíblicos que orientam nossa doutrina e prática cristã',
                'Cremos na inspiração divina e autoridade suprema das Sagradas Escrituras. Cremos no Deus trino — Pai, Filho e Espírito Santo — e na salvação unicamente pela graça mediante a fé em Jesus Cristo.',
            ),
            (
                'Liderança & Pastores',
                'lideranca',
                'Quem são os servos dedicados ao cuidado da igreja local',
                'A liderança do Ministério Luz da Palavra atua com senso de mordomia, transparência e respeito ao rebanho, honrando o testemunho deixado pelo pastor Leonel.',
            ),
        ]
        for title, slug, subtitle, body in pages_seed:
            InstitutionalPage.objects.get_or_create(
                slug=slug,
                defaults={
                    'title': title,
                    'subtitle': subtitle,
                    'body': body,
                    'status': PublicationStatus.PUBLISHED,
                }
            )
        self.stdout.write(self.style.SUCCESS("  [OK] Páginas institucionais base cadastradas"))

        # 8. Administrador Padrão do Sistema (se não existir nenhum superusuário)
        if not User.objects.filter(is_superuser=True).exists():
            admin_user = User.objects.create_superuser(
                username='admin',
                email='admin@luzdapalavra.org.br',
                password='admin_mlp_password_2026',
                role=UserRole.ADMIN,
                first_name='Administrador',
                last_name='Institucional'
            )
            admin_group = Group.objects.get(name='Administradores')
            admin_user.groups.add(admin_group)
            self.stdout.write(self.style.SUCCESS("  [OK] Usuário administrador inicial criado: admin / admin_mlp_password_2026"))
        else:
            self.stdout.write("  - Superusuário já existente no banco de dados.")

        self.stdout.write(self.style.SUCCESS("Provisionamento inicial concluído com sucesso!"))
