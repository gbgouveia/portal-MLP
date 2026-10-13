from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class UserRole(models.TextChoices):
    ADMIN = 'admin', _('Administrador Geral')
    INSTITUTIONAL_EDITOR = 'editor', _('Editor Institucional')
    MEDIA_TEAM = 'media', _('Equipe de Mídia')
    EVENT_MANAGER = 'events', _('Responsável por Eventos')
    REVIEWER = 'reviewer', _('Revisor Editorial')


class User(AbstractUser):
    """
    Modelo de usuário customizado do Ministério Luz da Palavra.
    Implementa separação de papéis e permissões no backend.
    """
    role = models.CharField(
        _('Função / Papel'),
        max_length=20,
        choices=UserRole.choices,
        default=UserRole.INSTITUTIONAL_EDITOR,
        help_text=_('Define as permissões operacionais do usuário no painel MLP.')
    )
    phone = models.CharField(_('Telefone / WhatsApp'), max_length=30, blank=True)
    bio = models.TextField(_('Biografia Curta'), blank=True)
    avatar = models.ImageField(_('Foto de Perfil'), upload_to='avatars/', blank=True, null=True)

    class Meta:
        verbose_name = _('Usuário')
        verbose_name_plural = _('Usuários')
        ordering = ['username']

    def __str__(self):
        full = self.get_full_name()
        return f"{full} ({self.get_role_display()})" if full else self.username

    @property
    def is_mlp_admin(self):
        return self.is_superuser or self.role == UserRole.ADMIN

    @property
    def can_manage_history(self):
        return self.is_mlp_admin or self.role in [UserRole.INSTITUTIONAL_EDITOR, UserRole.REVIEWER]

    @property
    def can_manage_media(self):
        return self.is_mlp_admin or self.role in [UserRole.MEDIA_TEAM, UserRole.INSTITUTIONAL_EDITOR]

    @property
    def can_manage_events(self):
        return self.is_mlp_admin or self.role in [UserRole.EVENT_MANAGER, UserRole.INSTITUTIONAL_EDITOR]
