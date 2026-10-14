import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), '..', 'static', 'images', 'hero')
os.makedirs(OUTPUT_DIR, exist_ok=True)

ITEMS = [
    {
        "filename": "culto-historico-1970.webp",
        "title": "Primeiros Cultos de Fé — Anos 1970",
        "subtitle": "Arquivo Memorial MLP • Registro Histórico",
        "bg_top": (24, 18, 14),
        "bg_bottom": (10, 8, 7),
        "accent": (242, 209, 109),
    },
    {
        "filename": "pregacao-expositiva.webp",
        "title": "Proclamação das Sagradas Escrituras",
        "subtitle": "Ministério da Palavra & Zelo Doutrinário",
        "bg_top": (32, 22, 14),
        "bg_bottom": (12, 9, 8),
        "accent": (191, 135, 31),
    },
    {
        "filename": "oracao-comunitaria.webp",
        "title": "Vigília de Oração & Intercessão",
        "subtitle": "Comunidade Reunida em Clamor Comunitário",
        "bg_top": (20, 16, 24),
        "bg_bottom": (8, 6, 9),
        "accent": (242, 209, 109),
    },
    {
        "filename": "escola-biblica-fundacional.webp",
        "title": "Escola Bíblica Dominical Pioneira",
        "subtitle": "Ensino e Discipulado através das Décadas",
        "bg_top": (28, 20, 16),
        "bg_bottom": (11, 8, 7),
        "accent": (166, 117, 75),
    },
    {
        "filename": "ceia-senhor-memorial.webp",
        "title": "Celebração da Santa Ceia do Senhor",
        "subtitle": "Comunhão, Memória e Gratidão ao Criador",
        "bg_top": (35, 18, 12),
        "bg_bottom": (14, 7, 5),
        "accent": (242, 209, 109),
    },
    {
        "filename": "louvor-congregacional.webp",
        "title": "Adoração e Cânticos de Louvor",
        "subtitle": "Coro Institucional & Hinologia Histórica",
        "bg_top": (22, 20, 16),
        "bg_bottom": (9, 8, 7),
        "accent": (191, 135, 31),
    },
    {
        "filename": "edificacao-templo.webp",
        "title": "Templo Sede — Marco de Continuidade",
        "subtitle": "Edificação e Crescimento da Comunidade de Fé",
        "bg_top": (25, 22, 18),
        "bg_bottom": (10, 9, 7),
        "accent": (242, 209, 109),
    },
    {
        "filename": "congrega-geracoes.webp",
        "title": "Legado que Atravessa Gerações",
        "subtitle": "Famílias Unificadas na Graça e Fidelidade",
        "bg_top": (30, 24, 18),
        "bg_bottom": (12, 10, 8),
        "accent": (191, 135, 31),
    },
]

def create_gallery_tile(item):
    w, h = 960, 600
    img = Image.new('RGB', (w, h), item['bg_bottom'])
    draw = ImageDraw.Draw(img)

    # Gradiente de fundo vertical
    for y in range(h):
        factor = y / h
        r = int(item['bg_top'][0] * (1 - factor) + item['bg_bottom'][0] * factor)
        g = int(item['bg_top'][1] * (1 - factor) + item['bg_bottom'][1] * factor)
        b = int(item['bg_top'][2] * (1 - factor) + item['bg_bottom'][2] * factor)
        draw.line([(0, y), (w, y)], fill=(r, g, b))

    # Luz dourada difusa no centro
    glow = Image.new('RGBA', (w, h), (0, 0, 0, 0))
    glow_draw = ImageDraw.Draw(glow)
    cx, cy = w // 2, h // 2
    accent = item['accent']
    glow_draw.ellipse([cx - 240, cy - 160, cx + 240, cy + 160], fill=(accent[0], accent[1], accent[2], 40))
    glow = glow.filter(ImageFilter.GaussianBlur(60))
    img.paste(glow, (0, 0), glow)
    draw = ImageDraw.Draw(img)

    # Moldura interna decorativa
    draw.rectangle([24, 24, w - 24, h - 24], outline=(item['accent'][0], item['accent'][1], item['accent'][2], 60), width=1)
    draw.rectangle([32, 32, w - 32, h - 32], outline=(item['accent'][0], item['accent'][1], item['accent'][2], 30), width=1)

    # Monograma e divisor
    draw.text((w // 2 - 35, 80), "M L P", fill=item['accent'])
    draw.line([(w // 2 - 120, 120), (w // 2 + 120, 120)], fill=(item['accent'][0], item['accent'][1], item['accent'][2]), width=1)

    # Título do registro histórico
    draw.text((w // 2 - 200, h // 2 - 20), item['title'], fill=(242, 241, 240))
    draw.text((w // 2 - 180, h // 2 + 25), item['subtitle'], fill=item['accent'])

    # Selo de identificação explícito
    draw.text((w // 2 - 130, h - 70), "ACERVO HISTÓRICO • MINISTÉRIO LUZ DA PALAVRA", fill=(160, 140, 120))

    dest = os.path.join(OUTPUT_DIR, item['filename'])
    img.save(dest, 'WEBP', quality=88)
    print(f"[OK] Gerado tile: {dest}")

def create_pastor_portrait():
    w, h = 800, 1000
    img = Image.new('RGBA', (w, h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    cx, cy = w // 2, h // 2

    # Halo dourado radiante suave atrás do pastor
    halo = Image.new('RGBA', (w, h), (0, 0, 0, 0))
    halo_draw = ImageDraw.Draw(halo)
    halo_draw.ellipse([cx - 260, cy - 300, cx + 260, cy + 220], fill=(242, 209, 109, 45))
    halo_draw.ellipse([cx - 180, cy - 220, cx + 180, cy + 140], fill=(191, 135, 31, 75))
    halo = halo.filter(ImageFilter.GaussianBlur(80))
    img.paste(halo, (0, 0), halo)

    # Silhueta pastoral respeitosa e digna (cabeça, ombros e peito)
    # Cabeça
    draw.ellipse([cx - 110, cy - 280, cx + 110, cy - 60], fill=(18, 14, 12, 245), outline=(242, 209, 109, 160), width=2)
    # Ombros e busto pastoral
    bust_points = [
        (cx - 280, h - 60),
        (cx - 240, cy + 40),
        (cx - 140, cy - 40),
        (cx + 140, cy - 40),
        (cx + 240, cy + 40),
        (cx + 280, h - 60),
        (cx + 280, h),
        (cx - 280, h),
    ]
    draw.polygon(bust_points, fill=(14, 11, 10, 250), outline=(191, 135, 31, 140))

    # Gola / Lapela pastoral em tom dourado suave
    draw.line([(cx - 40, cy - 35), (cx, cy + 120)], fill=(242, 209, 109, 200), width=2)
    draw.line([(cx + 40, cy - 35), (cx, cy + 120)], fill=(242, 209, 109, 200), width=2)

    # Selo memorial
    draw.text((cx - 110, h - 140), "RETRATO MEMORIAL", fill=(242, 209, 109, 220))
    draw.text((cx - 100, h - 115), "PASTOR LEONEL", fill=(242, 241, 240, 240))
    draw.text((cx - 135, h - 90), "Fundador • Desde os anos 1970", fill=(191, 135, 31, 200))

    dest = os.path.join(OUTPUT_DIR, 'pastor-leonel-portrait.webp')
    img.save(dest, 'WEBP', quality=92)
    print(f"[OK] Gerado retrato pastoral: {dest}")

if __name__ == '__main__':
    for item in ITEMS:
        create_gallery_tile(item)
    create_pastor_portrait()
    print("Concluído!")
