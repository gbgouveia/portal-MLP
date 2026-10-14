from django.db import models
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
from apps.core.models import PublishableModel


class AlbumCategory(models.Model):
    name = models.CharField(_('Nome da Categoria'), max_length=100)
    slug = models.SlugField(_('Slug'), max_length=120, unique=True, blank=True)
    description = models.TextField(_('Descrição'), blank=True)

    class Meta:
        verbose_name = _('Categoria de Álbum')
        verbose_name_plural = _('Categorias de Álbuns')
        ordering = ['name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Album(PublishableModel):
    """
    Álbuns fotográficos do Ministério e do Acervo Histórico.
    """
    title = models.CharField(_('Título do Álbum'), max_length=200)
    slug = models.SlugField(_('Identificador (Slug)'), max_length=220, unique=True, blank=True)
    category = models.ForeignKey(
        AlbumCategory,
        verbose_name=_('Categoria'),
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='albums'
    )
    event_date = models.DateField(_('Data do Registro / Evento'), blank=True, null=True)
    year = models.IntegerField(_('Ano Principal'), blank=True, null=True, db_index=True)
    description = models.TextField(_('Contexto do Álbum / Descrição'))
    cover_image = models.ImageField(_('Foto de Capa do Álbum'), upload_to='gallery/covers/', blank=True, null=True)
    
    is_historical_archive = models.BooleanField(
        _('Pertence ao Acervo Histórico (Décadas Passadas)'),
        default=False,
        help_text=_('Identifica fotos históricas de celebrações, batismos e cultos dos primeiros anos.')
    )
    is_featured = models.BooleanField(_('Destaque na Galeria Principal'), default=False)

    class Meta:
        verbose_name = _('Álbum Fotográfico')
        verbose_name_plural = _('Álbuns Fotográficos')
        ordering = ['-year', '-event_date', '-created_at']

    def __str__(self):
        year_str = f" ({self.year})" if self.year else ""
        return f"{self.title}{year_str}"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        if self.event_date and not self.year:
            self.year = self.event_date.year
        super().save(*args, **kwargs)

    @property
    def photo_count(self):
        return self.photos.count()


class Photo(models.Model):
    """
    Fotografia individual do acervo.
    Cada foto possui legenda, datação, autoria, alt_text acessível e metadados de preservação.
    """
    album = models.ForeignKey(
        Album,
        verbose_name=_('Álbum'),
        on_delete=models.CASCADE,
        related_name='photos'
    )
    image = models.ImageField(_('Arquivo de Imagem'), upload_to='gallery/photos/')
    title = models.CharField(_('Título da Imagem'), max_length=150, blank=True)
    caption = models.TextField(_('Legenda Explicativa com Contexto Histórico'), blank=True)
    alt_text = models.CharField(
        _('Texto Alternativo (Acessibilidade e Leitores de Tela)'),
        max_length=255,
        help_text=_('Descreva o conteúdo visual da foto para pessoas com deficiência visual.')
    )
    
    year = models.IntegerField(_('Ano Estimado'), blank=True, null=True)
    approximate_date = models.CharField(_('Datação Apropriada'), max_length=100, blank=True)
    photographer_credit = models.CharField(_('Fotógrafo / Fonte do Registro'), max_length=150, blank=True, default='Arquivo MLP')
    
    order = models.PositiveIntegerField(_('Ordem de Exibição no Álbum'), default=0)
    is_cover = models.BooleanField(_('Definir como Capa do Álbum'), default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _('Fotografia')
        verbose_name_plural = _('Fotografias do Acervo')
        ordering = ['order', 'id']

    def __str__(self):
        return self.title or f"Foto #{self.id} — {self.album.title}"


class HeroOrbitPhoto(models.Model):
    """
    Fotografias exibidas na galeria tridimensional orbital (Hero 3D) na página inicial.
    Gerenciáveis diretamente pelo painel administrativo (área restrita).
    """
    title = models.CharField(_('Título / Identificação'), max_length=150)
    image = models.ImageField(_('Arquivo de Imagem'), upload_to='gallery/hero_orbit/')
    alt_text = models.CharField(
        _('Texto Alternativo (Acessibilidade)'),
        max_length=255,
        blank=True,
        help_text=_('Descrição acessível para leitores de tela.')
    )
    order = models.PositiveIntegerField(
        _('Ordem na Órbita'),
        default=0,
        help_text=_('Menor número aparece primeiro no carrossel 3D.')
    )
    is_active = models.BooleanField(
        _('Ativo na Órbita'),
        default=True,
        help_text=_('Marque para exibir esta foto na galeria orbital 3D.')
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('Foto em Órbita da Hero')
        verbose_name_plural = _('Fotos em Órbita da Hero')
        ordering = ['order', 'id']

    def __str__(self):
        return f"{self.order}. {self.title}"
