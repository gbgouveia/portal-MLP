from django.urls import path
from . import views

app_name = 'public'

urlpatterns = [
    path('', views.home_view, name='home'),
    path('legado-pastor-leonel/', views.legacy_view, name='legacy'),
    path('nossa-historia/', views.history_view, name='history'),
    path('agenda-cultos/', views.events_list_view, name='events'),
    path('agenda-cultos/<slug:slug>/', views.event_detail_view, name='event_detail'),
    path('acervo-fotografico/', views.gallery_list_view, name='gallery'),
    path('acervo-fotografico/<slug:slug>/', views.album_detail_view, name='album_detail'),
    path('mensagens-e-ao-vivo/', views.media_list_view, name='media'),
    path('mensagens-e-ao-vivo/<slug:slug>/', views.media_detail_view, name='media_detail'),
    path('pagina/<slug:slug>/', views.institutional_page_view, name='page_detail'),
    path('contato-e-horarios/', views.contact_view, name='contact'),
    path('cadastro/', views.cadastro_view, name='cadastro'),
    path('entrar/', views.entrar_view, name='entrar'),
    path('perfil/', views.perfil_view, name='perfil'),
    path('avisos/', views.avisos_view, name='avisos'),
]
