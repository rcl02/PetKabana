# Site Petkabana – Estética Animal

Landing page estática (HTML + CSS + JS puro) que leva o visitante a agendar pelo WhatsApp.

## Arquivos

| Arquivo | O que é |
|---|---|
| `index.html` | Página com todos os textos, SEO (title, Open Graph, schema.org LocalBusiness + FAQPage) e ícones SVG |
| `style.css` | Estilos (cores da marca no topo, em `:root`) |
| `script.js` | Menu mobile, animações ao rolar e lightbox da galeria |
| `assets/img` | Fotos em AVIF/WebP em vários tamanhos, ícones e imagem de compartilhamento (OG 1200×630) |
| `assets/fonts` | Fonte Baloo 2 (WOFF2, auto-hospedada) |
| `ferramentas/gerar-imagens.py` | Recria `assets/img` e os ícones a partir de `ferramentas/originais` |
| `_headers` | Regras de cache para o Cloudflare Pages |
| `robots.txt`, `sitemap.xml`, `favicon.ico`, `apple-touch-icon.png`, `site.webmanifest` | SEO e ícones |

## O que falta preencher

Procure por `✏️ PREENCHER` / `✏️ CONFIRMAR` no `index.html`:

- **Domínio**: troque `https://petkabana.pages.dev/` pelo endereço final no `index.html`, `robots.txt` e `sitemap.xml`.
- **Logo oficial**: hoje é um desenho simples da cabana (SVG `i-logo`).
- **Hospedagem**: detalhes reais do serviço.
- **Depoimentos**: os 3 cartões rosa tracejados são espaços reservados.
- **Bairros de São Paulo**: confirmar se ainda são atendidos.
- **Perguntas frequentes**: o texto aparece na seção `#perguntas` e no FAQPage do `<head>`; altere os dois juntos.

## Trocar ou adicionar fotos

1. Coloque o JPG original em `ferramentas/originais` e adicione-o à lista `FOTOS` em `ferramentas/gerar-imagens.py`.
2. Rode (precisa de Python com Pillow 11.2+):
   ```
   python ferramentas/gerar-imagens.py
   ```
3. Copie um `<li>` da galeria no `index.html` e troque o nome do arquivo e o texto `alt`.

## Publicar grátis no Cloudflare Pages

Cloudflare → Workers & Pages → Create → Pages → **Upload assets** → arraste esta pasta (a pasta `ferramentas` pode ficar de fora) → Deploy.
Depois de saber o endereço final, atualize o domínio (veja acima).
