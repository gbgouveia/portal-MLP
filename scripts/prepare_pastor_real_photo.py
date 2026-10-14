import os
from PIL import Image, ImageEnhance
import rembg

USER_UPLOADED_DIR = r"C:\Users\HOME\.gemini\antigravity-ide\brain\a2e5d27e-9e42-4d7c-8d6f-d430af91c44a\.user_uploaded"
PASTOR_SRC = os.path.join(USER_UPLOADED_DIR, "media_1791932287655.jpg")
REF_SRC = os.path.join(USER_UPLOADED_DIR, "media_1791932294672.png")
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "..", "static", "images", "hero")
os.makedirs(OUTPUT_DIR, exist_ok=True)

def process_pastor():
    print("Processando fotografia real do Pastor Leonel com modelo u2netp (leve)...")
    img = Image.open(PASTOR_SRC).convert("RGBA")
    
    # Usa sessão u2netp (apenas 4MB)
    session = rembg.new_session("u2netp")
    cutout = rembg.remove(img, session=session)
    
    # Redimensiona mantendo proporção com alta qualidade
    w, h = cutout.size
    target_w = 720
    target_h = int(h * (target_w / w))
    cutout = cutout.resize((target_w, target_h), Image.Resampling.LANCZOS)
    
    # Criamos máscara com desvanecimento suave na base do busto para integração perfeita com o preto
    alpha = cutout.split()[3]
    alpha_bytes = list(alpha.getdata())
    fade_start = int(target_h * 0.72)
    
    for y in range(target_h):
        if y > fade_start:
            factor = 1.0 - ((y - fade_start) / (target_h - fade_start))
            for x in range(target_w):
                idx = y * target_w + x
                alpha_bytes[idx] = int(alpha_bytes[idx] * (factor ** 1.3))
                
    alpha.putdata(alpha_bytes)
    cutout.putalpha(alpha)
    
    # Leve ajuste de contraste e luminosidade para estética cinematográfica
    rgb = cutout.convert("RGB")
    enhancer = ImageEnhance.Contrast(rgb)
    rgb = enhancer.enhance(1.08)
    enhancer_b = ImageEnhance.Brightness(rgb)
    rgb = enhancer_b.enhance(1.02)
    
    final_pastor = Image.merge("RGBA", (*rgb.split(), cutout.split()[3]))
    
    out_png = os.path.join(OUTPUT_DIR, "pastor-leonel-real.png")
    out_webp = os.path.join(OUTPUT_DIR, "pastor-leonel-real.webp")
    final_pastor.save(out_png, "PNG")
    final_pastor.save(out_webp, "WEBP", quality=95)
    print(f"[OK] Retrato real do Pastor Leonel gerado em: {out_webp}")

def extract_reference_photos():
    print("Extraindo fotografias da referência visual...")
    ref = Image.open(REF_SRC).convert("RGB")
    
    # Coordenadas dos cartões na referência original (1024x576)
    crops = [
        ("foto-pulpito-jovem.webp", (80, 160, 240, 480)),
        ("foto-congregacao-salao.webp", (238, 255, 370, 500)),
        ("foto-pregacao-pastor.webp", (600, 330, 715, 550)),
        ("foto-adoracao-cruz.webp", (715, 300, 835, 550)),
        ("foto-casal-pastoral.webp", (835, 260, 925, 550)),
    ]
    
    for filename, box in crops:
        cropped = ref.crop(box)
        cropped = cropped.resize((480, 320), Image.Resampling.LANCZOS)
        enhancer = ImageEnhance.Contrast(cropped)
        cropped = enhancer.enhance(1.12)
        out_path = os.path.join(OUTPUT_DIR, filename)
        cropped.save(out_path, "WEBP", quality=92)
        print(f"[OK] Foto extraída: {out_path}")

if __name__ == "__main__":
    process_pastor()
    extract_reference_photos()
    print("Processamento concluído com sucesso!")
