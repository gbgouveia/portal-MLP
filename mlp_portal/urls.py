"""
URL configuration for mlp_portal project.
Ministério Luz da Palavra — Portal Institucional e Legado Pastoral
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

urlpatterns = [
    # Painel Técnico Django Admin (restrito a superadministradores técnicos)
    path('admin-tecnico/', admin.site.urls),

    # Autenticação Administrativa Oficial MLP
    path('painel/login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('painel/logout/', auth_views.LogoutView.as_view(next_page='/painel/login/'), name='logout'),

    # Painel Administrativo Customizado MLP
    path('painel/', include('apps.dashboard.urls')),

    # Portal Público (Página inicial, Legado do Pr. Leonel, História, Cultos, Galeria, etc.)
    path('', include('apps.core.urls')),
]

# Servir mídias e estáticos em desenvolvimento local
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
