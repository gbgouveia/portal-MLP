import os
import urllib.request
import json
from django.core.management.base import BaseCommand
from django.utils.text import slugify
from apps.media_library.models import MediaItem, MediaCategory

CHANNEL_ID = "UCkvN5Uqsjhj6lSpIX5JhBpA"
UPLOADS_PLAYLIST_ID = "UUkvN5Uqsjhj6lSpIX5JhBpA"

class Command(BaseCommand):
    help = "Sincroniza os últimos cultos e verifica lives no canal oficial do YouTube com baixo consumo de cota."

    def handle(self, *args, **options):
        api_key = os.getenv("YOUTUBE_API_KEY")
        if not api_key:
            self.stdout.write(self.style.ERROR("ERRO: YOUTUBE_API_KEY não encontrada no ambiente/.env."))
            return

        self.stdout.write(f"Consultando últimos vídeos do canal oficial ({CHANNEL_ID})...")
        playlist_url = f"https://www.googleapis.com/youtube/v3/playlistItems?part=snippet&playlistId={UPLOADS_PLAYLIST_ID}&maxResults=5&key={api_key}"
        
        try:
            req = urllib.request.Request(playlist_url, headers={'User-Agent': 'PortalMLP/1.0'})
            with urllib.request.urlopen(req) as response:
                data = json.loads(response.read().decode('utf-8'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Falha ao consultar playlist: {e}"))
            return

        items = data.get("items", [])
        if not items:
            self.stdout.write("Nenhum vídeo encontrado.")
            return

        video_ids = [item["snippet"]["resourceId"]["videoId"] for item in items if "resourceId" in item.get("snippet", {})]
        self.stdout.write(f"Encontrados {len(video_ids)} vídeos recentes. Verificando detalhes e status de live...")

        videos_url = f"https://www.googleapis.com/youtube/v3/videos?part=snippet,liveStreamingDetails&id={','.join(video_ids)}&key={api_key}"
        try:
            req = urllib.request.Request(videos_url, headers={'User-Agent': 'PortalMLP/1.0'})
            with urllib.request.urlopen(req) as response:
                details_data = json.loads(response.read().decode('utf-8'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Falha ao consultar detalhes dos vídeos: {e}"))
            return

        cat_cultos, _ = MediaCategory.objects.get_or_create(
            slug="cultos-e-celebracoes",
            defaults={"name": "Cultos e Celebrações"}
        )

        live_found = False
        synced_count = 0

        for video in details_data.get("items", []):
            vid = video["id"]
            title = video["snippet"]["title"]
            desc = video["snippet"]["description"]
            live_details = video.get("liveStreamingDetails", {})
            is_currently_live = bool(live_details.get("actualStartTime") and not live_details.get("actualEndTime"))

            # Determina tipo
            m_type = "livestream" if is_currently_live else "video"

            base_slug = slugify(title) or f"video-{vid}"
            slug = base_slug[:200]

            item, created = MediaItem.objects.update_or_create(
                youtube_video_id=vid,
                defaults={
                    "title": title[:200],
                    "slug": slug,
                    "description": desc or title,
                    "media_type": m_type,
                    "is_live": is_currently_live,
                    "category": cat_cultos,
                    "preacher": "Pr. Leonel" if "Pr." in title or "Pastor" in title else "Ministério Luz da Palavra",
                    "status": "published",
                }
            )

            if is_currently_live:
                live_found = True
                self.stdout.write(self.style.SUCCESS(f" [AO VIVO] {title} ({vid})"))
            else:
                action = "Criado" if created else "Atualizado"
                self.stdout.write(f" - {action}: {title} ({vid})")
            
            synced_count += 1

        if not live_found:
            # Garante que nenhum item antigo fique com is_live=True
            MediaItem.objects.filter(is_live=True).exclude(youtube_video_id__in=video_ids).update(is_live=False)

        self.stdout.write(self.style.SUCCESS(f"Sincronização concluída com sucesso! {synced_count} registros processados."))
