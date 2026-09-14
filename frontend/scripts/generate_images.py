"""Generate local SVG food illustrations for all 30 dishes.

Outputs styled SVGs into frontend/public/images/<slug>.svg.
Each image uses a meal-type color palette + a representative food emoji,
so no external image hosting is required. All illustrations are original
(demo) artworks, clearly marked as such.
"""

from __future__ import annotations

import sys
from pathlib import Path

# Allow importing the backend seed module.
ROOT = Path(__file__).resolve().parents[1]
BACKEND = ROOT.parent / "backend"
sys.path.insert(0, str(BACKEND))

import seed  # noqa: E402

OUT_DIR = ROOT / "public" / "images"

PALETTES = {
    # meal_type -> (background top, background bottom, text color, accent)
    "breakfast": ("#FFE8B0", "#F8B052", "#7A4300", "#FFF6E3"),
    "lunch": ("#D6F0D0", "#7FBF6B", "#1F4A1F", "#F1FFF0"),
    "dinner": ("#F7D3D0", "#E08B7F", "#6E1F14", "#FFF4F2"),
    "snack": ("#EAD3F5", "#C78FE0", "#4A1F5E", "#FAF0FF"),
}

# Representative food emoji per dish slug (local demo illustrations only).
EMOJI: dict[str, str] = {
    "pho-bo-ha-noi": "🍜",
    "bun-cha": "🍖",
    "banh-cuon": "🥟",
    "xoi-xeo": "🍚",
    "banh-mi-pate": "🥖",
    "pho-ga": "🍜",
    "chao-suon": "🥣",
    "banh-bao": "🥟",
    "mi-van-than": "🍝",
    "com-lang-vong": "🍙",
    "bun-bo-nam-bo": "🍜",
    "com-tam-suon-nuong": "🍚",
    "bun-oc": "🐌",
    "banh-da-cua": "🦀",
    "nem-chua-ran": "🥠",
    "pho-xao": "🍲",
    "cha-ca-la-vong": "🐟",
    "bun-thang": "🍲",
    "lau-bo-nhung-me": "🥘",
    "nuong-bbq": "🍢",
    "bun-rieu-cua": "🦀",
    "vit-quay": "🦆",
    "thit-kho-trung-vit": "🍖",
    "cha-gio-tom": "🍤",
    "banh-goi": "🥟",
    "trung-vit-lon": "🥚",
    "banh-trang-tron": "🥗",
    "xoi-xeo-via-he": "🍘",
    "nem-chua-thanh-hoa": "🍖",
    "banh-ran": "🍥",
}

FALLBACK = {
    "breakfast": "🍳",
    "lunch": "🍽",
    "dinner": "🍽",
    "snack": "🍿",
}


def esc(text: str) -> str:
    return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def build_svg(name: str, slug: str, meal_type: str) -> str:
    top, bottom, text_c, accent = PALETTES[meal_type]
    emoji = EMOJI.get(slug, FALLBACK[meal_type])
    name = esc(name)
    meal_label = {
        "breakfast": "BỮA SÁNG",
        "lunch": "BỮA TRƯA",
        "dinner": "BỮA TỐI",
        "snack": "ĂN VẶT",
    }[meal_type]

    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 600 420" role="img" aria-label="{name}">
  <defs>
    <linearGradient id="bg" x1="0" y1="0" x2="0.4" y2="1">
      <stop offset="0%" stop-color="{top}"/>
      <stop offset="100%" stop-color="{bottom}"/>
    </linearGradient>
    <radialGradient id="plate" cx="50%" cy="42%" r="60%">
      <stop offset="0%" stop-color="#FFFFFF" stop-opacity="0.95"/>
      <stop offset="100%" stop-color="{accent}"/>
    </radialGradient>
  </defs>

  <rect width="600" height="420" fill="url(#bg)"/>

  <!-- decorative steam -->
  <path d="M120 90 q12 -16 0 -32 q-12 -16 0 -32" stroke="{accent}" stroke-width="4" fill="none" stroke-linecap="round" opacity="0.5"/>
  <path d="M290 70 q12 -16 0 -32 q-12 -16 0 -32" stroke="{accent}" stroke-width="4" fill="none" stroke-linecap="round" opacity="0.5"/>
  <path d="M460 80 q12 -16 0 -32 q-12 -16 0 -32" stroke="{accent}" stroke-width="4" fill="none" stroke-linecap="round" opacity="0.5"/>

  <circle cx="512" cy="95" r="8" fill="{accent}" opacity="0.55"/>
  <circle cx="80" cy="330" r="6" fill="{accent}" opacity="0.45"/>
  <circle cx="545" cy="320" r="5" fill="{accent}" opacity="0.5"/>

  <!-- plate -->
  <ellipse cx="300" cy="250" rx="150" ry="105" fill="url(#plate)" stroke="#ffffff" stroke-width="3"/>
  <ellipse cx="300" cy="250" rx="118" ry="80" fill="none" stroke="{bottom}" stroke-width="2" opacity="0.35"/>

  <!-- food emoji -->
  <text x="300" y="275" text-anchor="middle" font-size="150" dominant-baseline="middle">{emoji}</text>

  <!-- name + label -->
  <text x="300" y="385" text-anchor="middle" font-size="30" font-weight="700"
        fill="{text_c}" font-family="'Segoe UI', Arial, sans-serif">{name}</text>
  <text x="300" y="408" text-anchor="middle" font-size="14" letter-spacing="3"
        fill="{text_c}" opacity="0.75" font-family="'Segoe UI', Arial, sans-serif">{meal_label} · DEMO</text>

  <rect x="1" y="1" width="598" height="418" fill="none" stroke="{text_c}" stroke-width="2" opacity="0.35" rx="0"/>
</svg>
"""


def generate() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    written = []
    for dish in seed.DISHES:
        slug = dish["slug"]
        svg = build_svg(dish["name"], slug, dish["meal_type"])
        (OUT_DIR / f"{slug}.svg").write_text(svg, encoding="utf-8")
        written.append(slug)
    # fallback placeholder
    fallback = build_svg("Món ăn Hà Nội", "fallback", "lunch")
    (OUT_DIR / "fallback.svg").write_text(fallback, encoding="utf-8")
    print(f"Generated {len(written)} SVGs + fallback.svg in {OUT_DIR}")


if __name__ == "__main__":
    generate()