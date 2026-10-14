from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.dashboard_index, name='index'),
    path('legado/', views.legacy_profile_edit, name='legacy_edit'),
    path('linha-do-tempo/', views.milestones_list, name='milestones_list'),
    path('linha-do-tempo/novo/', views.milestone_create, name='milestone_create'),
    path('linha-do-tempo/<int:pk>/editar/', views.milestone_edit, name='milestone_edit'),
    path('linha-do-tempo/<int:pk>/arquivar/', views.milestone_archive, name='milestone_archive'),
    path('eventos/', views.events_list, name='events_list'),
    path('eventos/novo/', views.event_create, name='event_create'),
    path('eventos/<int:pk>/editar/', views.event_edit, name='event_edit'),
    path('albuns/', views.albums_list, name='albums_list'),
    path('albuns/novo/', views.album_create, name='album_create'),
    path('albuns/<int:pk>/fotos/', views.album_photos, name='album_photos'),
    path('fotos-orbita/', views.hero_photos_list, name='hero_photos_list'),
    path('fotos-orbita/nova/', views.hero_photo_create, name='hero_photo_create'),
    path('fotos-orbita/<int:pk>/editar/', views.hero_photo_edit, name='hero_photo_edit'),
    path('fotos-orbita/<int:pk>/toggle-active/', views.hero_photo_toggle_active, name='hero_photo_toggle_active'),
    path('fotos-orbita/<int:pk>/excluir/', views.hero_photo_delete, name='hero_photo_delete'),
    path('midia/', views.media_list, name='media_list'),
    path('midia/novo/', views.media_create, name='media_create'),
    path('midia/<int:pk>/toggle-live/', views.media_toggle_live, name='media_toggle_live'),
    path('auditoria/', views.audit_list, name='audit_list'),
    path('usuarios/', views.users_list, name='users_list'),
    path('usuarios/exportar-csv/', views.users_export_csv, name='users_export_csv'),
    path('usuarios/<int:pk>/toggle-status/', views.user_toggle_status, name='user_toggle_status'),
    path('avisos/', views.dashboard_avisos_list, name='avisos_list'),
    path('whatsapp/envios/', views.dashboard_whatsapp_logs, name='whatsapp_logs'),
]
