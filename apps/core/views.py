import json
from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from apps.institutional.models import InstitutionalSetting, ServiceSchedule, MinistryLeader, MinistryDepartment
from apps.legacy.models import PastoralProfile, HistoricalMilestone, HistoricalDocument, Testimonial
from apps.events.models import Event, EventCategory
from apps.gallery.models import Album, Photo, AlbumCategory, HeroOrbitPhoto
from apps.media_library.models import MediaItem, MediaCategory
from apps.pages.models import InstitutionalPage


def home_view(request):
    """
    Página inicial editorial:
    Eixo narrativo com a história do Pastor Leonel, próximos eventos,
    transmissão ao vivo oficial (apenas confirmada), acervo fotográfico e cultos.
    """
    pastoral = PastoralProfile.get_solo()
    featured_milestones = HistoricalMilestone.published.filter(is_featured=True).order_by('year', 'order')[:4]
    if not featured_milestones.exists():
        featured_milestones = HistoricalMilestone.published.order_by('year', 'order')[:4]

    upcoming_events = Event.published.filter(start_datetime__gte=timezone.now()).order_by('start_datetime')[:3]
    recent_photos = Photo.objects.filter(album__status='published').order_by('-id')[:6]
    
    # Transmissão ao vivo oficial confirmada e última transmissão para fallback
    live_broadcast = MediaItem.published.filter(is_live=True).first()
    latest_broadcast = MediaItem.published.order_by('-event_date', '-created_at').first()
    recent_messages = MediaItem.published.order_by('-event_date', '-created_at')[:3]
    
    schedules = ServiceSchedule.objects.filter(is_active=True).order_by('weekday', 'time')
    testimonials = Testimonial.published.filter(is_featured=True)[:3]

    # Fotos da galeria 3D em órbita (Hero)
    orbit_photos = HeroOrbitPhoto.objects.filter(is_active=True).order_by('order', 'id')
    hero_orbit_photos_list = []
    for op in orbit_photos:
        if op.image:
            hero_orbit_photos_list.append({
                'src': op.image.url,
                'alt': op.alt_text or op.title
            })
    hero_orbit_photos_json = json.dumps(hero_orbit_photos_list) if hero_orbit_photos_list else ""

    context = {
        'pastoral': pastoral,
        'milestones': featured_milestones,
        'upcoming_events': upcoming_events,
        'recent_photos': recent_photos,
        'live_broadcast': live_broadcast,
        'latest_broadcast': latest_broadcast,
        'recent_messages': recent_messages,
        'schedules': schedules,
        'testimonials': testimonials,
        'hero_orbit_photos_json': hero_orbit_photos_json,
    }
    return render(request, 'public/home.html', context)


def legacy_view(request):
    """
    Página editorial dedicada ao Legado do Pastor Leonel:
    Biografia, linha do tempo interativa completa (iniciada nos anos 1970),
    documentos digitalizados e testemunhos autorizados.
    """
    pastoral = PastoralProfile.get_solo()
    milestones = HistoricalMilestone.published.all().order_by('year', 'order')
    decades = sorted(list(set(m.decade for m in milestones if m.decade)))
    documents = HistoricalDocument.published.all().order_by('-year', 'title')[:8]
    testimonials = Testimonial.published.all().order_by('order', '-created_at')
    
    context = {
        'pastoral': pastoral,
        'milestones': milestones,
        'decades': decades,
        'documents': documents,
        'testimonials': testimonials,
    }
    return render(request, 'public/legacy.html', context)


def history_view(request):
    """
    Trajetória institucional da comunidade de fé:
    Origens, lideranças e ministérios em continuidade com o legado.
    """
    leaders = MinistryLeader.objects.filter(is_active=True).order_by('order', 'name')
    departments = MinistryDepartment.objects.filter(is_active=True).order_by('order', 'name')
    history_page = InstitutionalPage.published.filter(slug='nossa-historia').first()
    
    context = {
        'leaders': leaders,
        'departments': departments,
        'history_page': history_page,
    }
    return render(request, 'public/history.html', context)


def events_list_view(request):
    """
    Agenda de eventos da comunidade: futuros e anteriores com filtros.
    """
    now = timezone.now()
    category_slug = request.GET.get('categoria')
    
    upcoming = Event.published.filter(start_datetime__gte=now)
    past = Event.published.filter(start_datetime__lt=now)

    if category_slug:
        upcoming = upcoming.filter(category__slug=category_slug)
        past = past.filter(category__slug=category_slug)

    categories = EventCategory.objects.all()

    context = {
        'upcoming_events': upcoming.order_by('start_datetime'),
        'past_events': past.order_by('-start_datetime')[:6],
        'categories': categories,
        'selected_category': category_slug,
    }
    return render(request, 'public/events_list.html', context)


def event_detail_view(request, slug):
    """
    Detalhe de um evento com localização, horário e relacionamentos com mídia.
    """
    event = get_object_or_404(Event.published, slug=slug)
    return render(request, 'public/event_detail.html', {'event': event})


def gallery_list_view(request):
    """
    Galeria fotográfica documental: álbuns categorizados e acervo histórico.
    """
    category_slug = request.GET.get('categoria')
    albums = Album.published.all()
    
    if category_slug:
        albums = albums.filter(category__slug=category_slug)

    categories = AlbumCategory.objects.all()
    
    # Destaca álbuns do acervo histórico
    historical_albums = albums.filter(is_historical_archive=True).order_by('-year')
    regular_albums = albums.filter(is_historical_archive=False).order_by('-event_date', '-year')

    context = {
        'albums': albums,
        'historical_albums': historical_albums,
        'regular_albums': regular_albums,
        'categories': categories,
        'selected_category': category_slug,
    }
    return render(request, 'public/gallery_list.html', context)


def album_detail_view(request, slug):
    """
    Visualização das fotos de um álbum com metadados e lightbox acessível.
    """
    album = get_object_or_404(Album.published, slug=slug)
    photos = album.photos.all().order_by('order', 'id')
    return render(request, 'public/album_detail.html', {'album': album, 'photos': photos})


def media_list_view(request):
    """
    Biblioteca audiovisual e transmissões oficiais no YouTube.
    """
    category_slug = request.GET.get('categoria')
    items = MediaItem.published.all()
    
    if category_slug:
        items = items.filter(category__slug=category_slug)

    live_broadcast = MediaItem.published.filter(is_live=True).first()
    categories = MediaCategory.objects.all()

    context = {
        'media_items': items.order_by('-event_date', '-created_at'),
        'live_broadcast': live_broadcast,
        'categories': categories,
        'selected_category': category_slug,
    }
    return render(request, 'public/media_list.html', context)


def media_detail_view(request, slug):
    """
    Página de mensagem individual com player seguro incorporado.
    """
    item = get_object_or_404(MediaItem.published, slug=slug)
    related_items = MediaItem.published.exclude(id=item.id).order_by('-created_at')[:3]
    return render(request, 'public/media_detail.html', {'item': item, 'related_items': related_items})


def institutional_page_view(request, slug):
    """
    Renderizador de páginas institucionais dinâmicas e editáveis.
    """
    page = get_object_or_404(InstitutionalPage.published, slug=slug)
    return render(request, 'public/institutional_page.html', {'page': page})


def contact_view(request):
    """
    Página oficial de contato, horários dos cultos e localização.
    """
    schedules = ServiceSchedule.objects.filter(is_active=True).order_by('weekday', 'time')
    return render(request, 'public/contact.html', {'schedules': schedules})


def cadastro_view(request):
    """
    Página oficial de auto-cadastro de membros com consentimento LGPD.
    Processamento e persistência efetuados via Firebase Client SDK.
    """
    return render(request, 'public/cadastro.html')


def entrar_view(request):
    """
    Página de login de membros e administradores.
    """
    return render(request, 'public/entrar.html')


def perfil_view(request):
    """
    Página de gerenciamento de perfil do membro (troca de foto, dados e LGPD).
    """
    return render(request, 'public/perfil.html')


def avisos_view(request):
    """
    Quadro geral de avisos oficiais e comunicados do Ministério Luz da Palavra.
    """
    return render(request, 'public/avisos.html')

