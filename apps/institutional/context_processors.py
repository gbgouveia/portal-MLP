from .models import InstitutionalSetting


def institutional_settings_context(request):
    """
    Injeta as configurações institucionais globais (endereço, contatos, frase institucional)
    em todos os templates Django.
    """
    try:
        settings_obj = InstitutionalSetting.get_solo()
    except Exception:
        settings_obj = None

    return {
        'institutional': settings_obj,
    }
