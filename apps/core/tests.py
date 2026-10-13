from django.test import TestCase, Client
from django.urls import reverse
from django.utils import timezone
from apps.accounts.models import User, UserRole
from apps.legacy.models import PastoralProfile, HistoricalMilestone
from apps.events.models import Event, EventCategory
from apps.gallery.models import Album, Photo
from apps.media_library.models import MediaItem
from apps.audit.models import AuditLog
from apps.core.models import PublicationStatus


class MLPModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='editor_test',
            password='secure_password_123',
            role=UserRole.INSTITUTIONAL_EDITOR
        )

    def test_milestone_decade_and_format(self):
        milestone = HistoricalMilestone.objects.create(
            year=1975,
            title='Primeiros Estudos Bíblicos',
            summary='Início dos estudos nas casas.',
            status=PublicationStatus.PUBLISHED
        )
        self.assertEqual(milestone.decade, '1970s')
        self.assertEqual(milestone.formatted_date, '1975')

    def test_milestone_approximate_date_display(self):
        milestone = HistoricalMilestone.objects.create(
            year=1980,
            approximate_date_display='Início dos anos 1980',
            title='Consolidação Departamental',
            summary='Resumo histórico.',
            status=PublicationStatus.PUBLISHED
        )
        self.assertEqual(milestone.formatted_date, 'Início dos anos 1980')

    def test_youtube_video_id_extraction(self):
        item = MediaItem.objects.create(
            title='Mensagem de Fé e Esperança',
            youtube_video_id='https://www.youtube.com/watch?v=dQw4w9WgXcQ',
            description='Estudo bíblico dominical.',
            status=PublicationStatus.PUBLISHED
        )
        self.assertEqual(item.youtube_video_id, 'dQw4w9WgXcQ')
        self.assertIn('https://www.youtube-nocookie.com/embed/dQw4w9WgXcQ', item.embed_url)

    def test_unauthorized_content_hidden_from_public(self):
        draft_milestone = HistoricalMilestone.objects.create(
            year=1999,
            title='Rascunho de Marco Não Confirmado',
            summary='Em apuração com a família.',
            status=PublicationStatus.DRAFT
        )
        published_milestone = HistoricalMilestone.objects.create(
            year=1995,
            title='Marco Confirmado e Autorizado',
            summary='Documento arquivado.',
            status=PublicationStatus.PUBLISHED
        )
        published_qs = HistoricalMilestone.published.all()
        self.assertIn(published_milestone, published_qs)
        self.assertNotIn(draft_milestone, published_qs)


class MLPPublicRouteTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.pastoral = PastoralProfile.get_solo()
        self.milestone = HistoricalMilestone.objects.create(
            year=1970,
            title='Fundação das Primeiras Reuniões',
            summary='Cultos iniciais.',
            status=PublicationStatus.PUBLISHED
        )

    def test_home_page_status_200(self):
        response = self.client.get(reverse('public:home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Ministério Luz da Palavra')
        self.assertContains(response, 'Pastor Leonel')

    def test_legacy_page_status_200(self):
        response = self.client.get(reverse('public:legacy'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'O Legado Pastoral do')
        self.assertContains(response, 'Linha do Tempo Histórica')

    def test_history_page_status_200(self):
        response = self.client.get(reverse('public:history'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Nossa História')

    def test_events_page_status_200(self):
        response = self.client.get(reverse('public:events'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Agenda de Eventos')

    def test_gallery_page_status_200(self):
        response = self.client.get(reverse('public:gallery'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Acervo Fotográfico')

    def test_media_page_status_200(self):
        response = self.client.get(reverse('public:media'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Mensagens & Gravações')

    def test_contact_page_status_200(self):
        response = self.client.get(reverse('public:contact'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Contato & Localização')

    def test_mac_os_dock_renders_canonical_routes(self):
        response = self.client.get(reverse('public:home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'mlp-dock')
        self.assertContains(response, reverse('public:home'))
        self.assertContains(response, reverse('public:history'))
        self.assertContains(response, reverse('public:legacy'))
        self.assertContains(response, reverse('public:events'))
        self.assertContains(response, reverse('public:gallery'))
        self.assertContains(response, reverse('public:media'))
        self.assertContains(response, reverse('public:contact'))

    def test_hero_section_2_split_screen_renders(self):
        response = self.client.get(reverse('public:home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'hero-section-2')
        self.assertContains(response, 'hero-reveal-mask')
        self.assertContains(response, 'hero-stats-strip')
        self.assertContains(response, '+50')



class MLPDashboardSecurityTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.admin_user = User.objects.create_superuser(
            username='admin_test',
            email='admin@test.org',
            password='test_secure_password',
            role=UserRole.ADMIN
        )

    def test_unauthenticated_dashboard_redirects_to_login(self):
        response = self.client.get(reverse('dashboard:index'))
        self.assertEqual(response.status_code, 302)
        self.assertIn('/painel/login/', response.url)

    def test_authenticated_admin_accesses_dashboard(self):
        self.client.login(username='admin_test', password='test_secure_password')
        response = self.client.get(reverse('dashboard:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Painel de Gestão & Memória')

    def test_dashboard_milestone_creation_logs_audit(self):
        self.client.login(username='admin_test', password='test_secure_password')
        response = self.client.post(reverse('dashboard:milestone_create'), {
            'year': 1988,
            'title': 'Marco de Teste de Auditoria',
            'summary': 'Resumo do teste.',
            'status': 'published',
        })
        self.assertEqual(response.status_code, 302)
        
        milestone = HistoricalMilestone.objects.get(year=1988)
        self.assertEqual(milestone.title, 'Marco de Teste de Auditoria')
        
        log_entry = AuditLog.objects.filter(object_id=str(milestone.pk)).first()
        self.assertIsNotNone(log_entry)
        self.assertEqual(log_entry.user, self.admin_user)
