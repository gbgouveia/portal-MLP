from django.db import models
from django.utils import timezone
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
from apps.core.models import PublishableModel


class EventCategory(models.Model):
    name = models.CharField(_('Nome da Categoria'), max_length=100)
    slug = models.SlugField(_('Slug'), max_length=120, unique=True, blank=True)
    color = models.CharField(_('Cor de Destaque (Hex)'), max_length=10, default='#A57A22')

    class Meta:
        verbose_name = _('Categoria de Evento')
        verbose_name_plural = _('Categorias de Eventos')
        ordering = ['name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Event(PublishableModel):
    """
    Agenda e histórico de celebrações, conferências e eventos da comunidade.
    """
    title = models.CharField(_('Título do Evento'), max_length=200)
    slug = models.SlugField(_('Identificador (Slug)'), max_length=220, unique=True, blank=True)
    category = models.ForeignKey(
        EventCategory,
        verbose_name=_('Categoria'),
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='events'
    )
    start_datetime = models.DateTimeField(_('Início do Evento'), db_index=True)
    end_datetime = models.DateTimeField(_('Término do Evento'), blank=True, null=True)
    
    location_name = models.CharField(_('Nome do Local'), max_length=150, default='Templo Sede MLP')
    address = models.CharField(_('Endereço Completo'), max_length=255, blank=True)
    
    summary = models.TextField(_('Resumo do Evento'))
    description = models.TextField(_('Descrição Detalhada e Informações'))
    cover_image = models.ImageField(_('Imagem de Divulgação'), upload_to='events/covers/', blank=True, null=True)
    
    is_featured = models.BooleanField(_('Destaque na Página Inicial'), default=False)
    
    related_album = models.ForeignKey(
        'gallery.Album',
        verbose_name=_('Álbum Fotográfico Relacionado'),
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='events'
    )
    related_video = models.ForeignKey(
        'media_library.MediaItem',
        verbose_name=_('Vídeo / Transmissão Relacionada'),
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='events'
    )

    class Meta:
        verbose_name = _('Evento / Celebração')
        verbose_name_plural = _('Eventos e Agenda')
        ordering = ['start_datetime']

    def __str__(self):
        return f"{self.title} ({self.start_datetime.strftime('%d/%m/%Y %H:%M')})"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    @property
    def is_upcoming(self):
        return self.start_datetime >= timezone.now()
