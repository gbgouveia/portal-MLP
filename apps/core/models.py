from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class PublicationStatus(models.TextChoices):
    DRAFT = 'draft', _('Rascunho')
    IN_REVIEW = 'in_review', _('Em Revisão')
    PUBLISHED = 'published', _('Publicado')
    ARCHIVED = 'archived', _('Arquivado')


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=PublicationStatus.PUBLISHED)


class PublishableModel(models.Model):
    """
    Modelo base abstrato para entidades com fluxo editorial (rascunho, revisão, publicado, arquivado).
    Garante rastreabilidade e impede que rascunhos vazem para o site público.
    """
    status = models.CharField(
        _('Estado Editorial'),
        max_length=20,
        choices=PublicationStatus.choices,
        default=PublicationStatus.DRAFT,
        db_index=True,
    )
    created_at = models.DateTimeField(_('Criado em'), auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(_('Atualizado em'), auto_now=True)
    published_at = models.DateTimeField(_('Publicado em'), null=True, blank=True, db_index=True)

    objects = models.Manager()
    published = PublishedManager()

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if self.status == PublicationStatus.PUBLISHED and not self.published_at:
            self.published_at = timezone.now()
        elif self.status != PublicationStatus.PUBLISHED and self.published_at:
            # mantém a data anterior ou pode preservar histórico
            pass
        super().save(*args, **kwargs)

    @property
    def is_visible_publicly(self):
        return self.status == PublicationStatus.PUBLISHED
