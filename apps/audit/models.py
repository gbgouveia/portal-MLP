from django.db import models
from django.utils.translation import gettext_lazy as _


class AuditAction(models.TextChoices):
    CREATE = 'CREATE', _('Criação')
    UPDATE = 'UPDATE', _('Atualização')
    DELETE = 'DELETE', _('Exclusão')
    PUBLISH = 'PUBLISH', _('Publicação')
    ARCHIVE = 'ARCHIVE', _('Arquivamento')
    LOGIN = 'LOGIN', _('Autenticação')


class AuditLog(models.Model):
    """
    Trilha de auditoria das ações realizadas no painel administrativo MLP.
    Garante compliance, transparência e preservação de registros.
    """
    user = models.ForeignKey(
        'accounts.User',
        verbose_name=_('Usuário Responsável'),
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='audit_logs'
    )
    action = models.CharField(_('Ação Executada'), max_length=20, choices=AuditAction.choices, db_index=True)
    model_name = models.CharField(_('Módulo / Entidade'), max_length=100, db_index=True)
    object_id = models.CharField(_('ID do Objeto'), max_length=100, blank=True)
    object_repr = models.CharField(_('Representação do Registro'), max_length=255)
    details = models.TextField(_('Detalhes / Modificações'), blank=True)
    ip_address = models.GenericIPAddressField(_('Endereço IP'), blank=True, null=True)
    created_at = models.DateTimeField(_('Data e Hora'), auto_now_add=True, db_index=True)

    class Meta:
        verbose_name = _('Registro de Auditoria')
        verbose_name_plural = _('Trilha de Auditoria (Logs)')
        ordering = ['-created_at']

    def __str__(self):
        actor = self.user.username if self.user else 'Sistema'
        return f"[{self.created_at.strftime('%d/%m/%Y %H:%M')}] {actor} — {self.get_action_display()}: {self.object_repr}"

    @classmethod
    def log(cls, user, action, instance, details='', ip_address=None):
        """Helper rápido para registrar eventos de auditoria."""
        try:
            cls.objects.create(
                user=user if getattr(user, 'is_authenticated', False) else None,
                action=action,
                model_name=instance.__class__.__name__ if instance else 'Sistema',
                object_id=str(getattr(instance, 'pk', '')) if instance else '',
                object_repr=str(instance)[:250] if instance else '',
                details=details,
                ip_address=ip_address
            )
        except Exception:
            pass
