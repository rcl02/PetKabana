"""
GERAR IMAGENS (opcional) — recria tudo em assets/img a partir de ferramentas/originais.

Gera: fotos AVIF + WebP em vários tamanhos, imagem de compartilhamento (OG 1200x630),
favicon.ico, favicon-32.png, apple-touch-icon.png e ícones 192/512 do manifest.

Precisa de Python com Pillow 11.2+ (suporte a AVIF):
    python ferramentas/gerar-imagens.py
"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageOps

RAIZ = Path(__file__).resolve().parent.parent
ORIG = RAIZ / "ferramentas" / "originais"
SAIDA = RAIZ / "assets" / "img"
SAIDA.mkdir(parents=True, exist_ok=True)
PREFIXO = "banho-tosa-domicilio-petkabana-"

# arquivo original -> (nome no site, altura do foco do recorte quadrado: 0 = topo, 1 = base)
FOTOS = {
    "husky.jpg": ("husky-olhos-azuis", .40),
    "cachorro-branco-bandana.jpg": ("cachorro-branco-bandana-verde", .38),
    "maltes-laco-azul.jpg": ("maltes-laco-azul", .40),
    "basset-hound.jpg": ("basset-hound", .40),
    "shih-tzu-antes.jpg": ("shih-tzu-antes-da-tosa", .35),
    "bulldog-frances.jpg": ("bulldog-frances-bandana", .35),
    "rottweiler.jpg": ("rottweiler", .33),
    "pastor-alemao.jpg": ("pastor-alemao-pelo-longo", .45),
    "shih-tzu-bandana.jpg": ("shih-tzu-bandana", .40),
}


def salvar(img, nome, avif=True):
    img = img.convert("RGB")
    img.save(SAIDA / f"{nome}.webp", "WEBP", quality=78, method=6)
    if avif:
        img.save(SAIDA / f"{nome}.avif", "AVIF", quality=55)


def largura(img, w):
    return img.resize((w, round(img.height * w / img.width)), Image.LANCZOS)


# 1) Fotos da galeria: quadradas 400/720 + versão inteira 720 para o lightbox
for arq, (slug, foco) in FOTOS.items():
    img = ImageOps.exif_transpose(Image.open(ORIG / arq))
    w, h = img.size
    lado = min(w, h)
    y0 = max(0, min(h - lado, round(foco * h - lado / 2)))
    quadrada = img.crop((0, y0, lado, y0 + lado))
    for tam in (400, 720):
        salvar(quadrada.resize((tam, tam), Image.LANCZOS), f"{PREFIXO}{slug}-{tam}")
    salvar(largura(img, 720), f"{PREFIXO}{slug}-inteira-720", avif=False)

# 2) Foto da van com a equipe (hero e seção da van)
van = ImageOps.exif_transpose(Image.open(ORIG / "van-equipe.jpg"))
for tam in (640, 960):
    salvar(largura(van, tam), f"pet-shop-movel-petkabana-van-equipe-{tam}")


# 3) Logo (cabana) desenhado no mesmo traço do SVG do site (viewBox 64)
def cabana(px, fundo=None):
    s = px / 64
    im = Image.new("RGBA", (px, px), fundo or (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.polygon([(4 * s, 30 * s), (32 * s, 6 * s), (60 * s, 30 * s)], fill="#D9963A")
    d.rounded_rectangle((13 * s, 29 * s, 51 * s, 56 * s), radius=4 * s, fill="#8B5A2B")
    d.rounded_rectangle((27 * s, 39 * s, 37 * s, 56 * s), radius=5 * s, fill="#F97316")
    for cx, cy, r in ((52, 14, 5), (58, 24, 3)):
        d.ellipse(((cx - r) * s, (cy - r) * s, (cx + r) * s, (cy + r) * s), fill="#BDE6F7", outline="#5BB8E0", width=max(1, round(1.5 * s)))
    return im


grande = cabana(512)
grande.resize((32, 32), Image.LANCZOS).save(RAIZ / "favicon-32.png")
grande.save(RAIZ / "favicon.ico", sizes=[(16, 16), (32, 32), (48, 48)])
for tam, destino in ((180, RAIZ / "apple-touch-icon.png"), (192, SAIDA / "icone-192.png"), (512, SAIDA / "icone-512.png")):
    fundo = Image.new("RGBA", (512, 512), "#FFF1E6")
    fundo.alpha_composite(cabana(400), (56, 50))
    fundo.convert("RGB").resize((tam, tam), Image.LANCZOS).save(destino)

# 4) Imagem de compartilhamento (WhatsApp, Instagram, Facebook): 1200x630
og = Image.new("RGB", (1200, 630), "#F97316")
foto = ImageOps.fit(van, (640, 630), centering=(.45, .5))
og.paste(foto, (560, 0))
d = ImageDraw.Draw(og)
fonte = lambda n, t: ImageFont.truetype(f"C:/Windows/Fonts/{n}", t)
og.paste(cabana(120).convert("RGB"), (56, 60), cabana(120))
d.text((56, 200), "Petkabana", font=fonte("seguibl.ttf", 76), fill="#2A1608")
d.text((60, 290), "ESTÉTICA ANIMAL", font=fonte("segoeuib.ttf", 26), fill="#2A1608")
d.text((56, 360), "Banho & Tosa\nna porta da sua casa", font=fonte("segoeuib.ttf", 46), fill="#FFFFFF", spacing=6,
       stroke_width=2, stroke_fill="#7C2D12")
d.text((60, 520), "Pet shop móvel · Cotia e São Paulo", font=fonte("segoeuib.ttf", 28), fill="#2A1608")
og.save(SAIDA / "petkabana-banho-tosa-domicilio-og.jpg", "JPEG", quality=85, optimize=True, progressive=True)

assert (SAIDA / f"{PREFIXO}husky-olhos-azuis-720.avif").exists()
print("OK:", len(list(SAIDA.iterdir())), "arquivos em assets/img")
