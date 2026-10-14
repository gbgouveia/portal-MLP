from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from apps.legacy.models import PastoralProfile, HistoricalMilestone, HistoricalDocument, Testimonial
from apps.events.models import Event, EventCategory
from apps.gallery.models import Album, Photo, AlbumCategory, HeroOrbitPhoto
from apps.media_library.models import MediaItem, MediaCategory
from apps.pages.models import InstitutionalPage
from apps.institutional.models import InstitutionalSetting, ServiceSchedule
import csv
from django.http import HttpResponse
from django.core.paginator import Paginator
from django.db.models import Q
from apps.accounts.models import User, UserRole
from apps.audit.models import AuditLog, AuditAction
from apps.core.models import PublicationStatus


@login_required
def dashboard_index(request):
    """
    Visão geral com indicadores calculados exclusivamente a partir dos dados reais do banco.
    """
    milestone_count = HistoricalMilestone.objects.count()
    photo_count = Photo.objects.count()
    album_count = Album.objects.count()
    event_count = Event.objects.count()
    media_count = MediaItem.objects.count()
    hero_photo_count = HeroOrbitPhoto.objects.filter(is_active=True).count()
    live_stream = MediaItem.objects.filter(is_live=True).first()
    recent_audits = AuditLog.objects.select_related('user').order_by('-created_at')[:8]
    
    # Rascunhos pendentes de revisão
    pending_milestones = HistoricalMilestone.objects.filter(status=PublicationStatus.IN_REVIEW).count()
    pending_events = Event.objects.filter(status=PublicationStatus.IN_REVIEW).count()

    context = {
        'milestone_count': milestone_count,
        'photo_count': photo_count,
        'album_count': album_count,
        'event_count': event_count,
        'media_count': media_count,
        'hero_photo_count': hero_photo_count,
        'live_stream': live_stream,
        'recent_audits': recent_audits,
        'pending_reviews': pending_milestones + pending_events,
    }
    return render(request, 'dashboard/index.html', context)


# ==========================================
# 1. GESTÃO DO LEGADO DO PASTOR LEONEL
# ==========================================
@login_required
def legacy_profile_edit(request):
    pastoral = PastoralProfile.get_solo()
    if request.method == 'POST':
        pastoral.full_name = request.POST.get('full_name', pastoral.full_name)
        pastoral.title = request.POST.get('title', pastoral.title)
        pastoral.ministry_start_year = int(request.POST.get('ministry_start_year') or 1970)
        pastoral.portrait_caption = request.POST.get('portrait_caption', '')
        pastoral.short_bio = request.POST.get('short_bio', '')
        pastoral.full_biography = request.POST.get('full_biography', '')
        pastoral.core_values = request.POST.get('core_values', '')

        if 'portrait' in request.FILES:
            pastoral.portrait = request.FILES['portrait']

        pastoral.save()
        AuditLog.log(request.user, AuditAction.UPDATE, pastoral, details='Atualização do perfil pastoral oficial do Pr. Leonel')
        messages.success(request, 'Perfil pastoral do Pastor Leonel atualizado com sucesso!')
        return redirect('dashboard:legacy_edit')

    return render(request, 'dashboard/legacy_form.html', {'pastoral': pastoral})


# ==========================================
# 2. LINHA DO TEMPO HISTÓRICA (MARCOS)
# ==========================================
@login_required
def milestones_list(request):
    milestones = HistoricalMilestone.objects.all().order_by('year', 'order')
    return render(request, 'dashboard/milestones_list.html', {'milestones': milestones})


@login_required
def milestone_create(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        year = int(request.POST.get('year') or 1970)
        approximate_date = request.POST.get('approximate_date_display', '')
        summary = request.POST.get('summary', '')
        full_story = request.POST.get('full_story', '')
        status = request.POST.get('status', PublicationStatus.DRAFT)
        is_featured = request.POST.get('is_featured') == 'on'

        milestone = HistoricalMilestone(
            title=title,
            year=year,
            approximate_date_display=approximate_date,
            summary=summary,
            full_story=full_story,
            status=status,
            is_featured=is_featured,
        )
        if 'primary_image' in request.FILES:
            milestone.primary_image = request.FILES['primary_image']

        milestone.save()
        AuditLog.log(request.user, AuditAction.CREATE, milestone, details=f'Marco histórico criado: {title} ({year})')
        messages.success(request, f'Marco "{title}" cadastrado com sucesso!')
        return redirect('dashboard:milestones_list')

    return render(request, 'dashboard/milestone_form.html', {'milestone': None, 'statuses': PublicationStatus.choices})


@login_required
def milestone_edit(request, pk):
    milestone = get_object_or_404(HistoricalMilestone, pk=pk)
    if request.method == 'POST':
        milestone.title = request.POST.get('title', milestone.title)
        milestone.year = int(request.POST.get('year') or milestone.year)
        milestone.approximate_date_display = request.POST.get('approximate_date_display', '')
        milestone.summary = request.POST.get('summary', '')
        milestone.full_story = request.POST.get('full_story', '')
        milestone.status = request.POST.get('status', milestone.status)
        milestone.is_featured = request.POST.get('is_featured') == 'on'

        if 'primary_image' in request.FILES:
            milestone.primary_image = request.FILES['primary_image']

        milestone.save()
        AuditLog.log(request.user, AuditAction.UPDATE, milestone, details=f'Marco histórico editado: {milestone.title}')
        messages.success(request, f'Marco "{milestone.title}" atualizado com sucesso!')
        return redirect('dashboard:milestones_list')

    return render(request, 'dashboard/milestone_form.html', {'milestone': milestone, 'statuses': PublicationStatus.choices})


@login_required
def milestone_archive(request, pk):
    milestone = get_object_or_404(HistoricalMilestone, pk=pk)
    milestone.status = PublicationStatus.ARCHIVED
    milestone.save()
    AuditLog.log(request.user, AuditAction.ARCHIVE, milestone, details='Marco arquivado pelo gestor')
    messages.info(request, f'Marco "{milestone.title}" foi arquivado.')
    return redirect('dashboard:milestones_list')


# ==========================================
# 3. EVENTOS E AGENDA
# ==========================================
@login_required
def events_list(request):
    events = Event.objects.all().order_by('-start_datetime')
    return render(request, 'dashboard/events_list.html', {'events': events})


@login_required
def event_create(request):
    categories = EventCategory.objects.all()
    if request.method == 'POST':
        title = request.POST.get('title')
        category_id = request.POST.get('category')
        start_datetime = request.POST.get('start_datetime')
        location_name = request.POST.get('location_name', 'Templo Sede MLP')
        address = request.POST.get('address', '')
        summary = request.POST.get('summary', '')
        description = request.POST.get('description', '')
        status = request.POST.get('status', PublicationStatus.DRAFT)
        is_featured = request.POST.get('is_featured') == 'on'

        event = Event(
            title=title,
            category_id=category_id if category_id else None,
            start_datetime=start_datetime,
            location_name=location_name,
            address=address,
            summary=summary,
            description=description,
            status=status,
            is_featured=is_featured,
        )
        if 'cover_image' in request.FILES:
            event.cover_image = request.FILES['cover_image']

        event.save()
        AuditLog.log(request.user, AuditAction.CREATE, event, details=f'Evento cadastrado: {title}')
        messages.success(request, f'Evento "{title}" criado com sucesso!')
        return redirect('dashboard:events_list')

    return render(request, 'dashboard/event_form.html', {'event': None, 'categories': categories, 'statuses': PublicationStatus.choices})


@login_required
def event_edit(request, pk):
    event = get_object_or_404(Event, pk=pk)
    categories = EventCategory.objects.all()
    if request.method == 'POST':
        event.title = request.POST.get('title', event.title)
        category_id = request.POST.get('category')
        event.category_id = category_id if category_id else None
        event.location_name = request.POST.get('location_name', event.location_name)
        event.address = request.POST.get('address', event.address)
        event.summary = request.POST.get('summary', event.summary)
        event.description = request.POST.get('description', event.description)
        event.status = request.POST.get('status', event.status)
        event.is_featured = request.POST.get('is_featured') == 'on'

        dt_str = request.POST.get('start_datetime')
        if dt_str:
            event.start_datetime = dt_str

        if 'cover_image' in request.FILES:
            event.cover_image = request.FILES['cover_image']

        event.save()
        AuditLog.log(request.user, AuditAction.UPDATE, event, details=f'Evento editado: {event.title}')
        messages.success(request, f'Evento "{event.title}" atualizado!')
        return redirect('dashboard:events_list')

    return render(request, 'dashboard/event_form.html', {'event': event, 'categories': categories, 'statuses': PublicationStatus.choices})


# ==========================================
# 4. ÁLBUNS E FOTOGRAFIAS (UPLOAD EM LOTE)
# ==========================================
@login_required
def albums_list(request):
    albums = Album.objects.all().order_by('-created_at')
    return render(request, 'dashboard/albums_list.html', {'albums': albums})


@login_required
def album_create(request):
    categories = AlbumCategory.objects.all()
    if request.method == 'POST':
        title = request.POST.get('title')
        category_id = request.POST.get('category')
        year = request.POST.get('year')
        description = request.POST.get('description', '')
        is_historical = request.POST.get('is_historical_archive') == 'on'
        status = request.POST.get('status', PublicationStatus.DRAFT)

        album = Album(
            title=title,
            category_id=category_id if category_id else None,
            year=int(year) if year else None,
            description=description,
            is_historical_archive=is_historical,
            status=status,
        )
        if 'cover_image' in request.FILES:
            album.cover_image = request.FILES['cover_image']

        album.save()
        AuditLog.log(request.user, AuditAction.CREATE, album, details=f'Álbum criado: {title}')
        messages.success(request, f'Álbum "{title}" criado. Agora adicione fotografias.')
        return redirect('dashboard:album_photos', pk=album.pk)

    return render(request, 'dashboard/album_form.html', {'album': None, 'categories': categories, 'statuses': PublicationStatus.choices})


@login_required
def album_photos(request, pk):
    album = get_object_or_404(Album, pk=pk)
    if request.method == 'POST' and 'photos' in request.FILES:
        files = request.FILES.getlist('photos')
        created_count = 0
        for f in files:
            Photo.objects.create(
                album=album,
                image=f,
                title=f.name.rsplit('.', 1)[0].replace('-', ' ').title(),
                alt_text=f"Fotografia do acervo do álbum {album.title}",
                year=album.year,
                photographer_credit='Acervo Memorial MLP'
            )
            created_count += 1

        AuditLog.log(request.user, AuditAction.CREATE, album, details=f'{created_count} fotografias enviadas em lote para {album.title}')
        messages.success(request, f'{created_count} fotografias adicionadas com sucesso!')
        return redirect('dashboard:album_photos', pk=album.pk)

    photos = album.photos.all().order_by('order', 'id')
    return render(request, 'dashboard/photo_upload.html', {'album': album, 'photos': photos})


# ==========================================
# 5. CATÁLOGO DE VÍDEOS & AO VIVO OFICIAL
# ==========================================
@login_required
def media_list(request):
    items = MediaItem.objects.all().order_by('-created_at')
    return render(request, 'dashboard/media_list.html', {'media_items': items})


@login_required
def media_create(request):
    categories = MediaCategory.objects.all()
    if request.method == 'POST':
        title = request.POST.get('title')
        category_id = request.POST.get('category')
        youtube_id = request.POST.get('youtube_video_id', '')
        preacher = request.POST.get('preacher', 'Pr. Leonel')
        biblical_reference = request.POST.get('biblical_reference', '')
        description = request.POST.get('description', '')
        is_live = request.POST.get('is_live') == 'on'
        status = request.POST.get('status', PublicationStatus.PUBLISHED)

        if is_live:
            # Desmarca qualquer outra live anterior ativa
            MediaItem.objects.filter(is_live=True).update(is_live=False)

        item = MediaItem(
            title=title,
            category_id=category_id if category_id else None,
            youtube_video_id=youtube_id,
            preacher=preacher,
            biblical_reference=biblical_reference,
            description=description,
            is_live=is_live,
            status=status,
        )
        item.save()
        AuditLog.log(request.user, AuditAction.CREATE, item, details=f'Mídia adicionada: {title}')
        messages.success(request, f'Vídeo/Mensagem "{title}" cadastrado com sucesso!')
        return redirect('dashboard:media_list')

    return render(request, 'dashboard/media_form.html', {'item': None, 'categories': categories, 'statuses': PublicationStatus.choices})


@login_required
def media_toggle_live(request, pk):
    item = get_object_or_404(MediaItem, pk=pk)
    if not item.is_live:
        MediaItem.objects.filter(is_live=True).update(is_live=False)
        item.is_live = True
        item.status = PublicationStatus.PUBLISHED
        messages.success(request, f'Transmissão ao vivo ativada para "{item.title}"!')
    else:
        item.is_live = False
        messages.info(request, f'Transmissão ao vivo de "{item.title}" foi encerrada.')

    item.save()
    AuditLog.log(request.user, AuditAction.UPDATE, item, details=f'Status de transmissão ao vivo alternado para: {item.is_live}')
    return redirect('dashboard:media_list')


# ==========================================
# 6. AUDITORIA E USUÁRIOS
# ==========================================
@login_required
def audit_list(request):
    logs = AuditLog.objects.select_related('user').all().order_by('-created_at')[:50]
    return render(request, 'dashboard/audit_list.html', {'logs': logs})


@login_required
def users_list(request):
    if not request.user.is_mlp_admin:
        messages.error(request, 'Acesso restrito a administradores.')
        return redirect('dashboard:index')

    users = User.objects.all().order_by('username')
    return render(request, 'dashboard/users_list.html', {'users': users})


# ==========================================
# 7. FOTOS EM ÓRBITA DA HERO 3D (ÁREA RESTRITA)
# ==========================================
@login_required
def hero_photos_list(request):
    """
    Lista e gerencia as fotografias que circulam em órbita na galeria 3D da página inicial.
    """
    photos = HeroOrbitPhoto.objects.all().order_by('order', 'id')
    active_count = photos.filter(is_active=True).count()
    return render(request, 'dashboard/hero_photos_list.html', {
        'photos': photos,
        'total_count': photos.count(),
        'active_count': active_count,
    })


@login_required
def hero_photo_create(request):
    """
    Adiciona uma nova fotografia para a galeria orbital 3D.
    """
    if request.method == 'POST':
        title = request.POST.get('title', '').strip()
        alt_text = request.POST.get('alt_text', '').strip()
        order = int(request.POST.get('order') or 0)
        is_active = request.POST.get('is_active') == 'on'

        if not title:
            messages.error(request, 'O título da foto é obrigatório.')
            return render(request, 'dashboard/hero_photo_form.html', {'photo': None})

        if 'image' not in request.FILES:
            messages.error(request, 'Por favor, selecione um arquivo de imagem.')
            return render(request, 'dashboard/hero_photo_form.html', {'photo': None})

        photo = HeroOrbitPhoto(
            title=title,
            alt_text=alt_text or title,
            order=order,
            is_active=is_active,
            image=request.FILES['image']
        )
        photo.save()
        AuditLog.log(request.user, AuditAction.CREATE, photo, details=f'Foto adicionada à órbita da Hero 3D: {title}')
        messages.success(request, f'Foto "{title}" adicionada com sucesso à órbita 3D!')
        return redirect('dashboard:hero_photos_list')

    next_order = (HeroOrbitPhoto.objects.order_by('-order').values_list('order', flat=True).first() or 0) + 1
    return render(request, 'dashboard/hero_photo_form.html', {'photo': None, 'next_order': next_order})


@login_required
def hero_photo_edit(request, pk):
    """
    Edita dados ou substitui a imagem de uma foto em órbita da Hero 3D.
    """
    photo = get_object_or_404(HeroOrbitPhoto, pk=pk)
    if request.method == 'POST':
        photo.title = request.POST.get('title', photo.title).strip()
        photo.alt_text = request.POST.get('alt_text', photo.alt_text).strip()
        photo.order = int(request.POST.get('order') or 0)
        photo.is_active = request.POST.get('is_active') == 'on'

        if 'image' in request.FILES:
            photo.image = request.FILES['image']

        photo.save()
        AuditLog.log(request.user, AuditAction.UPDATE, photo, details=f'Foto da órbita 3D editada: {photo.title}')
        messages.success(request, f'Foto "{photo.title}" atualizada com sucesso!')
        return redirect('dashboard:hero_photos_list')

    return render(request, 'dashboard/hero_photo_form.html', {'photo': photo})


@login_required
def hero_photo_toggle_active(request, pk):
    """
    Ativa/Desativa exibição de uma fotografia na órbita 3D com um clique.
    """
    photo = get_object_or_404(HeroOrbitPhoto, pk=pk)
    photo.is_active = not photo.is_active
    photo.save(update_fields=['is_active', 'updated_at'])
    status_str = "ativada" if photo.is_active else "desativada"
    AuditLog.log(request.user, AuditAction.UPDATE, photo, details=f'Foto da órbita 3D {status_str}: {photo.title}')
    messages.info(request, f'Foto "{photo.title}" foi {status_str} na órbita 3D.')
    return redirect('dashboard:hero_photos_list')


@login_required
def hero_photo_delete(request, pk):
    """
    Remove uma fotografia da órbita 3D.
    """
    photo = get_object_or_404(HeroOrbitPhoto, pk=pk)
    if request.method == 'POST':
        title = photo.title
        AuditLog.log(request.user, AuditAction.DELETE, photo, details=f'Foto removida da órbita 3D: {title}')
        photo.delete()
        messages.success(request, f'Foto "{title}" removida da órbita 3D com sucesso.')
        return redirect('dashboard:hero_photos_list')

    return render(request, 'dashboard/hero_photo_confirm_delete.html', {'photo': photo})


# ==========================================
# 6. GESTÃO DE MEMBROS E USUÁRIOS (ETAPA 4)
# ==========================================
@login_required
def users_list(request):
    """
    Lista de irmãos/usuários com busca, filtros (ativo/inativo), paginação.
    """
    if not request.user.is_mlp_admin:
        messages.error(request, 'Acesso restrito a administradores.')
        return redirect('dashboard:index')

    search = request.GET.get('q', '').strip()
    status_filter = request.GET.get('status', '').strip()

    users_qs = User.objects.all().order_by('-date_joined')
    if search:
        users_qs = users_qs.filter(
            Q(username__icontains=search) |
            Q(first_name__icontains=search) |
            Q(last_name__icontains=search) |
            Q(email__icontains=search) |
            Q(phone__icontains=search)
        )
    if status_filter == 'ativo':
        users_qs = users_qs.filter(is_active=True)
    elif status_filter == 'inativo':
        users_qs = users_qs.filter(is_active=False)

    paginator = Paginator(users_qs, 15)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    context = {
        'users': page_obj,
        'search': search,
        'status_filter': status_filter,
        'total_count': users_qs.count(),
    }
    return render(request, 'dashboard/users_list.html', context)


@login_required
def users_export_csv(request):
    """
    Exportação oficial da lista de membros em CSV com codificação UTF-8 BOM.
    """
    if not request.user.is_mlp_admin:
        messages.error(request, 'Acesso restrito a administradores.')
        return redirect('dashboard:index')

    response = HttpResponse(content_type='text/csv; charset=utf-8')
    response['Content-Disposition'] = 'attachment; filename="membros_mlp.csv"'
    response.write('\ufeff'.encode('utf-8'))

    writer = csv.writer(response)
    writer.writerow(['ID', 'Nome de Usuário', 'Nome Completo', 'E-mail', 'Telefone', 'Papel', 'Ativo', 'Data de Cadastro'])

    for u in User.objects.all().order_by('first_name', 'username'):
        writer.writerow([
            u.id,
            u.username,
            u.get_full_name(),
            u.email,
            u.phone,
            u.get_role_display(),
            'Sim' if u.is_active else 'Não',
            u.date_joined.strftime('%d/%m/%Y %H:%M') if u.date_joined else ''
        ])
    return response


@login_required
def user_toggle_status(request, pk):
    """
    Ativa/Desativa o acesso de um irmão na congregação.
    """
    if not request.user.is_mlp_admin:
        messages.error(request, 'Acesso restrito a administradores.')
        return redirect('dashboard:index')

    u = get_object_or_404(User, pk=pk)
    if u.id == request.user.id:
        messages.error(request, 'Você não pode desativar o seu próprio usuário.')
        return redirect('dashboard:users_list')

    u.is_active = not u.is_active
    u.save(update_fields=['is_active'])
    status_str = 'ativado' if u.is_active else 'desativado'
    AuditLog.log(request.user, AuditAction.UPDATE, u, details=f'Membro {u.username} {status_str}')
    messages.success(request, f'Membro {u.get_full_name() or u.username} foi {status_str} com sucesso.')
    return redirect('dashboard:users_list')


@login_required
def dashboard_avisos_list(request):
    """
    Painel de gestão de avisos (criar, fixar, expirar e excluir).
    Integrado com o Firestore em tempo real.
    """
    if not request.user.is_mlp_admin:
        messages.error(request, 'Acesso restrito a administradores.')
        return redirect('dashboard:index')
    return render(request, 'dashboard/avisos_list.html')


@login_required
def dashboard_whatsapp_logs(request):
    """
    Consulta ao registro de envios do WhatsApp Business (Meta Cloud API).
    Exibe registros de envios, status de entrega e custos.
    """
    if not request.user.is_mlp_admin:
        messages.error(request, 'Acesso restrito a administradores.')
        return redirect('dashboard:index')
    return render(request, 'dashboard/whatsapp_logs.html')

