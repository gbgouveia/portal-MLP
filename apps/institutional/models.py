from django.db import models
from django.utils.translation import gettext_lazy as _
from apps.core.models import PublishableModel


class InstitutionalSetting(models.Model):
    """
    Configurações institucionais oficiais (Singleton).
    Centraliza endereço, telefones, redes oficiais e identidade verbal.
    """
    name = models.CharField(_('Nome Institucional'), max_length=150, default='Ministério Luz da Palavra')
    short_name = models.CharField(_('Sigla / Nome Curto'), max_length=20, default='MLP')
    tagline = models.CharField(
        _('Direção Conceitual / Frase Síntese'),
        max_length=255,
        default='Uma história construída pela fé. Um legado que atravessa gerações. Um ministério que continua.'
    )
    founding_year = models.PositiveIntegerField(_('Ano de Fundação'), default=1970)
    history_summary = models.TextField(
        _('Resumo Histórico Institucional'),
        blank=True,
        default='O Ministério Luz da Palavra nasceu nos anos 1970, consolidando uma trajetória de fé genuína, ensino das Escrituras e relevância comunitária contínua.'
    )
    address = models.CharField(_('Endereço Oficial'), max_length=255, default='Sede Central — Ministério Luz da Palavra')
    city_state = models.CharField(_('Cidade / UF'), max_length=100, default='Brasil')
    phone = models.CharField(_('Telefone Principal'), max_length=50, blank=True)
    whatsapp = models.CharField(_('WhatsApp Oficial'), max_length=50, blank=True)
    email = models.EmailField(_('E-mail de Contato'), max_length=150, default='contato@luzdapalavra.org.br')
    
    youtube_url = models.URLField(_('Canal Oficial no YouTube'), blank=True, default='https://www.youtube.com')
    youtube_channel_id = models.CharField(_('ID do Canal YouTube'), max_length=100, blank=True)
    instagram_url = models.URLField(_('Instagram Oficial'), blank=True)
    facebook_url = models.URLField(_('Facebook Oficial'), blank=True)
    
    official_logo = models.ImageField(_('Logotipo Oficial'), upload_to='branding/', blank=True, null=True)
    hero_background_image = models.ImageField(_('Imagem de Abertura Oficial'), upload_to='branding/', blank=True, null=True)

    class Meta:
        verbose_name = _('Configuração Institucional')
        verbose_name_plural = _('Configurações Institucionais')

    def __str__(self):
        return f"{self.name} (Configurações Gerais)"

    @classmethod
    def get_solo(cls):
        obj, _ = cls.objects.get_or_create(id=1)
        return obj


class ServiceSchedule(models.Model):
    """
    Horários e cultos da comunidade de fé.
    """
    WEEKDAY_CHOICES = [
        (1, _('Segunda-feira')),
        (2, _('Terça-feira')),
        (3, _('Quarta-feira')),
        (4, _('Quinta-feira')),
        (5, _('Sexta-feira')),
        (6, _('Sábado')),
        (7, _('Domingo')),
    ]

    title = models.CharField(_('Nome do Culto / Reunião'), max_length=120)
    weekday = models.IntegerField(_('Dia da Semana'), choices=WEEKDAY_CHOICES, default=7)
    time = models.TimeField(_('Horário de Início'))
    end_time = models.TimeField(_('Horário de Término'), blank=True, null=True)
    location = models.CharField(_('Local'), max_length=150, default='Nave Central / Templo')
    description = models.TextField(_('Descrição / Público'), blank=True)
    order = models.PositiveIntegerField(_('Ordem de Exibição'), default=0)
    is_active = models.BooleanField(_('Ativo'), default=True)

    class Meta:
        verbose_name = _('Horário de Culto')
        verbose_name_plural = _('Horários de Cultos')
        ordering = ['weekday', 'time', 'order']

    def __str__(self):
        return f"{self.get_weekday_display()} - {self.time.strftime('%H:%M')} — {self.title}"


class MinistryLeader(models.Model):
    """
    Liderança pastoral e conselho ministerial contemporâneo.
    """
    name = models.CharField(_('Nome'), max_length=150)
    role = models.CharField(_('Função / Ministério'), max_length=120)
    biography = models.TextField(_('Biografia / Trajetória'), blank=True)
    photo = models.ImageField(_('Foto'), upload_to='leaders/', blank=True, null=True)
    order = models.PositiveIntegerField(_('Ordem'), default=0)
    is_active = models.BooleanField(_('Ativo na Liderança'), default=True)

    class Meta:
        verbose_name = _('Líder Institucional')
        verbose_name_plural = _('Liderança Institucional')
        ordering = ['order', 'name']

    def __str__(self):
        return f"{self.name} ({self.role})"


class MinistryDepartment(models.Model):
    """
    Frentes de ministério, departamentos e iniciativas comunitárias.
    """
    name = models.CharField(_('Nome do Departamento'), max_length=150)
    leader_name = models.CharField(_('Responsável / Liderança'), max_length=150, blank=True)
    description = models.TextField(_('Propósito e Atuação'))
    meeting_info = models.CharField(_('Encontros / Periodicidade'), max_length=200, blank=True)
    icon_name = models.CharField(_('Ícone de Referência'), max_length=50, blank=True, help_text=_('Nome semântico do ícone SVG'))
    order = models.PositiveIntegerField(_('Ordem'), default=0)
    is_active = models.BooleanField(_('Ativo'), default=True)

    class Meta:
        verbose_name = _('Ministério / Departamento')
        verbose_name_plural = _('Ministérios e Departamentos')
        ordering = ['order', 'name']

    def __str__(self):
        return self.name
