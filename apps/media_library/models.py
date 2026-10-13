import re
from django.db import models
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
from apps.core.models import PublishableModel


class MediaCategory(models.Model):
    name = models.CharField(_('Categoria'), max_length=100)
    slug = models.SlugField(_('Slug'), max_length=120, unique=True, blank=True)

    class Meta:
        verbose_name = _('Categoria de Mídia')
        verbose_name_plural = _('Categorias de Mídias')
        ordering = ['name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class MediaItem(PublishableModel):
    """
    Biblioteca de pregações, estudos e transmissões em vídeo e áudio.
    """
    MEDIA_TYPES = [
        ('video', _('Vídeo / Pregação Gravada')),
        ('livestream', _('Transmissão Oficial ao Vivo')),
        ('audio', _('Áudio / Estudo Bíblico')),
    ]

    title = models.CharField(_('Título da Mensagem / Registro'), max_length=200)
    slug = models.SlugField(_('Identificador (Slug)'), max_length=220, unique=True, blank=True)
    media_type = models.CharField(_('Tipo de Conteúdo'), max_length=20, choices=MEDIA_TYPES, default='video')
    category = models.ForeignKey(
        MediaCategory,
        verbose_name=_('Categoria'),
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='media_items'
    )
    
    youtube_video_id = models.CharField(
        _('ID do Vídeo no YouTube ou Link Completo'),
        max_length=100,
        help_text=_('Ex: "dQw4w9WgXcQ" ou "https://www.youtube.com/watch?v=dQw4w9WgXcQ"')
    )
    preacher = models.CharField(_('Ministrante / Pregador'), max_length=150, default='Pr. Leonel', blank=True)
    biblical_reference = models.CharField(_('Referência Bíblica'), max_length=150, blank=True)
    event_date = models.DateField(_('Data da Gravação / Celebração'), blank=True, null=True)
    
    description = models.TextField(_('Sinopse / Conteúdo da Mensagem'))
    custom_thumbnail = models.ImageField(_('Miniatura Personalizada'), upload_to='media/thumbs/', blank=True, null=True)
    
    is_live = models.BooleanField(
        _('Transmissão ao Vivo Confirmada'),
        default=False,
        help_text=_('Marque apenas quando o culto estiver efetivamente em transmissão ao vivo.')
    )
    is_featured = models.BooleanField(_('Destaque na Página Inicial'), default=False)
    
    milestone = models.ForeignKey(
        'legacy.HistoricalMilestone',
        verbose_name=_('Marco Histórico Associado'),
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='media_items'
    )

    class Meta:
        verbose_name = _('Item Audiovisual')
        verbose_name_plural = _('Biblioteca Audiovisual')
        ordering = ['-event_date', '-created_at']

    def __str__(self):
        return f"{self.title} ({self.preacher})"

    def clean_youtube_id(self):
        """Extrai o ID puro de 11 caracteres mesmo se o operador colar a URL inteira."""
        val = self.youtube_video_id.strip()
        if 'youtube.com' in val or 'youtu.be' in val:
            match = re.search(r'(?:v=|\/)([0-9A-Za-z_-]{11}).*', val)
            if match:
                return match.group(1)
        return val

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        self.youtube_video_id = self.clean_youtube_id()
        super().save(*args, **kwargs)

    @property
    def embed_url(self):
        if self.youtube_video_id:
            return f"https://www.youtube-nocookie.com/embed/{self.youtube_video_id}"
        return ""

    @property
    def fallback_thumbnail_url(self):
        if self.custom_thumbnail:
            return self.custom_thumbnail.url
        if self.youtube_video_id:
            return f"https://img.youtube.com/vi/{self.youtube_video_id}/hqdefault.jpg"
        return ""
