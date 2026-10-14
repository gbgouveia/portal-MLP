from django.contrib import admin
from django.utils.html import format_html
from .models import AlbumCategory, Album, Photo, HeroOrbitPhoto


@admin.register(HeroOrbitPhoto)
class HeroOrbitPhotoAdmin(admin.ModelAdmin):
    list_display = ('preview_thumbnail', 'title', 'order', 'is_active', 'created_at')
    list_editable = ('order', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('title', 'alt_text')

    def preview_thumbnail(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="height: 45px; border-radius: 4px; object-fit: cover;" />', obj.image.url)
        return "-"
    preview_thumbnail.short_description = "Prévia"


@admin.register(AlbumCategory)
class AlbumCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Album)
class AlbumAdmin(admin.ModelAdmin):
    list_display = ('title', 'year', 'category', 'status', 'is_featured', 'is_historical_archive')
    list_filter = ('status', 'is_featured', 'is_historical_archive', 'year')
    search_fields = ('title', 'description')
    prepopulated_fields = {'slug': ('title',)}


@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):
    list_display = ('title', 'album', 'year', 'order', 'is_cover')
    list_filter = ('album', 'is_cover', 'year')
    search_fields = ('title', 'caption', 'alt_text')

