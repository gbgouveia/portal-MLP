from django.db import models
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
from apps.core.models import PublishableModel


class PastoralProfile(models.Model):
    """
    Perfil e biografia oficial do Pastor Leonel — eixo narrativo do portal.
    """
    full_name = models.CharField(_('Nome Completo'), max_length=150, default='Pastor Leonel')
    title = models.CharField(_('Título Pastoral'), max_length=150, default='Pastor Fundador & Patriarca Pastoral')
    birth_date = models.DateField(_('Data de Nascimento'), blank=True, null=True)
    passing_date = models.DateField(_('Data de Falecimento / Transição'), blank=True, null=True)
    ministry_start_year = models.PositiveIntegerField(_('Ano de Início do Ministério'), default=1970)
    
    portrait = models.ImageField(_('Retrato Oficial'), upload_to='pastoral/portraits/', blank=True, null=True)
    portrait_caption = models.CharField(_('Legenda do Retrato Oficial'), max_length=255, blank=True, default='Registro histórico do Pastor Leonel')
    
    short_bio = models.TextField(
        _('Biografia Sintética / Introdução'),
        default='Pioneiro de fé inabalável, o Pastor Leonel dedicou mais de cinco décadas à proclamação da Palavra, edificação de famílias e fundamentação sólida do Ministério Luz da Palavra.'
    )
    full_biography = models.TextField(
        _('Biografia Completa'),
        help_text=_('Texto detalhado da trajetória pessoal, vocação, primeiros anos ministeriais e legado.')
    )
    core_values = models.TextField(
        _('Pilares Doutrinários e Valores Pastorais'),
        blank=True,
        help_text=_('Ex: Fidelidade Bíblica, Simplicidade no Viver, Amor ao Próximo e Zelo Pastoral.')
    )
    is_active = models.BooleanField(_('Perfil Ativo'), default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('Perfil Pastoral do Pastor Leonel')
        verbose_name_plural = _('Perfis Pastorais')

    def __str__(self):
        return f"{self.full_name} — {self.title}"

    @classmethod
    def get_solo(cls):
        obj, _ = cls.objects.get_or_create(id=1)
        return obj


class HistoricalMilestone(PublishableModel):
    """
    Marcos históricos da linha do tempo iniciada nos anos 1970.
    Suporta datas confirmadas e aproximações históricas sem forçar dia/mês inventados.
    """
    year = models.IntegerField(_('Ano do Marco'), db_index=True)
    month = models.PositiveSmallIntegerField(_('Mês (Opcional)'), blank=True, null=True)
    day = models.PositiveSmallIntegerField(_('Dia (Opcional)'), blank=True, null=True)
    approximate_date_display = models.CharField(
        _('Exibição de Data Apropriada'),
        max_length=100,
        blank=True,
        help_text=_('Ex: "Início dos anos 1970", "Março de 1984" ou "Década de 1990"')
    )
    decade = models.CharField(_('Década'), max_length=10, blank=True, db_index=True, help_text=_('Ex: 1970s, 1980s'))

    title = models.CharField(_('Título do Acontecimento'), max_length=200)
    slug = models.SlugField(_('Identificador (Slug)'), max_length=220, unique=True, blank=True)
    summary = models.TextField(_('Resumo Curto do Acontecimento'))
    full_story = models.TextField(_('Relato Histórico e Contextualização'), blank=True)
    
    primary_image = models.ImageField(_('Fotografia Histórica Principal'), upload_to='legacy/milestones/', blank=True, null=True)
    image_caption = models.CharField(_('Legenda da Imagem'), max_length=255, blank=True)
    image_source = models.CharField(_('Fonte / Acervo da Imagem'), max_length=150, blank=True, default='Acervo Histórico MLP')
    
    related_album = models.ForeignKey(
        'gallery.Album',
        verbose_name=_('Álbum de Fotos Relacionado'),
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='milestones'
    )
    order = models.PositiveIntegerField(_('Ordem Dentro do Ano'), default=0)
    is_featured = models.BooleanField(_('Destaque na Página Inicial'), default=False)

    class Meta:
        verbose_name = _('Marco Histórico')
        verbose_name_plural = _('Marcos Históricos (Linha do Tempo)')
        ordering = ['year', 'month', 'order', 'title']

    def __str__(self):
        display_date = self.approximate_date_display or str(self.year)
        return f"[{display_date}] {self.title}"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f"{self.year}-{self.title}")
        if self.year:
            decade_start = (self.year // 10) * 10
            self.decade = f"{decade_start}s"
        super().save(*args, **kwargs)

    @property
    def formatted_date(self):
        if self.approximate_date_display:
            return self.approximate_date_display
        if self.day and self.month:
            return f"{self.day:02d}/{self.month:02d}/{self.year}"
        if self.month:
            return f"{self.month:02d}/{self.year}"
        return str(self.year)


class HistoricalDocument(PublishableModel):
    """
    Documentos históricos digitalizados (cartas, certidões, boletins antigos, registros pastorais).
    """
    DOC_TYPES = [
        ('letter', _('Carta Pastoral / Correspondência')),
        ('certificate', _('Certidão / Ata / Registro Oficial')),
        ('note', _('Anotações Manuscritas do Pr. Leonel')),
        ('bulletin', _('Boletim Informativo Histórico')),
        ('photo_doc', _('Registro Documental Fotográfico')),
        ('other', _('Outro Documento de Acervo')),
    ]

    title = models.CharField(_('Título do Documento'), max_length=200)
    slug = models.SlugField(_('Slug'), max_length=220, unique=True, blank=True)
    doc_type = models.CharField(_('Tipo de Documento'), max_length=30, choices=DOC_TYPES, default='official')
    document_file = models.FileField(_('Arquivo Digitalizado (PDF/Imagem)'), upload_to='legacy/documents/', blank=True, null=True)
    thumbnail = models.ImageField(_('Pré-visualização do Documento'), upload_to='legacy/documents/thumbs/', blank=True, null=True)
    
    year = models.IntegerField(_('Ano Estimado / Registrado'), blank=True, null=True)
    approximate_date = models.CharField(_('Datação Documental'), max_length=100, blank=True)
    description = models.TextField(_('Descrição e Transcrição Histórica'))
    author_or_source = models.CharField(_('Autoria / Proveniência'), max_length=150, default='Arquivo Central MLP')
    
    milestone = models.ForeignKey(
        HistoricalMilestone,
        verbose_name=_('Marco Histórico Associado'),
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='documents'
    )

    class Meta:
        verbose_name = _('Documento Histórico')
        verbose_name_plural = _('Documentos Históricos')
        ordering = ['-year', 'title']

    def __str__(self):
        return f"{self.title} ({self.approximate_date or self.year or 'S/D'})"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)


class Testimonial(PublishableModel):
    """
    Testemunhos autorizados que atestam o legado do Pastor Leonel e a continuidade do ministério.
    """
    author_name = models.CharField(_('Nome do Autor do Depoimento'), max_length=150)
    author_role = models.CharField(_('Vínculo com o Ministério'), max_length=150, help_text=_('Ex: "Membro desde 1978", "Presbítero", "Comunidade"'))
    author_photo = models.ImageField(_('Foto do Autor'), upload_to='legacy/testimonials/', blank=True, null=True)
    testimony_text = models.TextField(_('Relato / Depoimento Autorizado'))
    year_context = models.IntegerField(_('Ano / Época do Relato'), blank=True, null=True)
    
    milestone = models.ForeignKey(
        HistoricalMilestone,
        verbose_name=_('Marco Associado'),
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='testimonials'
    )
    is_featured = models.BooleanField(_('Destaque na Página Inicial'), default=False)
    order = models.PositiveIntegerField(_('Ordem'), default=0)

    class Meta:
        verbose_name = _('Testemunho Autorizado')
        verbose_name_plural = _('Testemunhos Autorizados')
        ordering = ['order', '-created_at']

    def __str__(self):
        return f"{self.author_name} — {self.author_role}"
