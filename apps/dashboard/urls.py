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
    path('midia/', views.media_list, name='media_list'),
    path('midia/novo/', views.media_create, name='media_create'),
    path('midia/<int:pk>/toggle-live/', views.media_toggle_live, name='media_toggle_live'),
    path('auditoria/', views.audit_list, name='audit_list'),
    path('usuarios/', views.users_list, name='users_list'),
]
