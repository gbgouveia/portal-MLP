from django.db import models
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
from apps.core.models import PublishableModel


class InstitutionalPage(PublishableModel):
    """
    Páginas institucionais editáveis (Nossa História, Declaração de Fé, Liderança, Horários, etc.)
    """
    title = models.CharField(_('Título da Página'), max_length=150)
    slug = models.SlugField(_('Identificador (Slug)'), max_length=170, unique=True, blank=True)
    subtitle = models.CharField(_('Subtítulo'), max_length=250, blank=True)
    body = models.TextField(_('Conteúdo Editorial (HTML / Texto Estruturado)'))
    cover_image = models.ImageField(_('Imagem de Cabeçalho'), upload_to='pages/covers/', blank=True, null=True)
    
    meta_title = models.CharField(_('Título SEO (Meta Title)'), max_length=100, blank=True)
    meta_description = models.TextField(_('Descrição SEO (Meta Description)'), blank=True, max_length=200)
    order = models.PositiveIntegerField(_('Ordem no Menu'), default=0)

    class Meta:
        verbose_name = _('Página Institucional')
        verbose_name_plural = _('Páginas Institucionais')
        ordering = ['order', 'title']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)


class PageRevision(models.Model):
    """
    Histórico de revisões e auditoria textual de páginas institucionais.
    """
    page = models.ForeignKey(InstitutionalPage, related_name='revisions', on_delete=models.CASCADE)
    author = models.ForeignKey('accounts.User', on_delete=models.SET_NULL, null=True, blank=True)
    title = models.CharField(_('Título gravado'), max_length=150)
    body = models.TextField(_('Conteúdo gravado'))
    comment = models.CharField(_('Nota da Revisão'), max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _('Revisão de Página')
        verbose_name_plural = _('Revisões de Páginas')
        ordering = ['-created_at']

    def __str__(self):
        return f"Revisão de {self.page.title} em {self.created_at.strftime('%d/%m/%Y %H:%M')}"
