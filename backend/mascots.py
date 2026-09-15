"""12 con giáp — mascot config + zodiac-themed palettes for the app."""

from __future__ import annotations

from typing import Any


# ============================================================
# 12 Zodiac mascots
# ============================================================

MASCOTS: list[dict[str, Any]] = [
    {
        "id": "ty",
        "name": "Tý",
        "animal": "Chuột",
        "theme_color": "#94A3B8",
        "secondary_color": "#CBD5E1",
        "emoji": "🐀",
        "greeting": "Chuột nhanh nhẹn, hôm nay thử món ăn nhanh nào!",
        "encouragement": "Món này đang chờ bạn khám phá.",
        "fallback_message": "Không sao, mình thử một lựa chọn khác nhé.",
        "asset_source": "original-app-asset",
        "verification_status": "demo",
    },
    {
        "id": "suu",
        "name": "Sửu",
        "animal": "Trâu",
        "theme_color": "#92400E",
        "secondary_color": "#D97706",
        "emoji": "🐂",
        "greeting": "Trâu bền bỉ, hôm nay thưởng thức một món truyền thống nhé!",
        "encouragement": "Món này đang chờ bạn khám phá.",
        "fallback_message": "Không sao, mình thử một lựa chọn khác nhé.",
        "asset_source": "original-app-asset",
        "verification_status": "demo",
    },
    {
        "id": "dan",
        "name": "Dần",
        "animal": "Hổ",
        "theme_color": "#EA580C",
        "secondary_color": "#FB923C",
        "emoji": "🐅",
        "greeting": "Hổ dũng cảm, hôm nay thử món đậm vị nào!",
        "encouragement": "Món này đang chờ bạn khám phá.",
        "fallback_message": "Không sao, mình thử một lựa chọn khác nhé.",
        "asset_source": "original-app-asset",
        "verification_status": "demo",
    },
    {
        "id": "mao",
        "name": "Mão",
        "animal": "Mèo",
        "theme_color": "#DB2777",
        "secondary_color": "#F9A8D4",
        "emoji": "🐈",
        "greeting": "Mèo tinh tế, hôm nay chọn một món tinh tế nào!",
        "encouragement": "Món này đang chờ bạn khám phá.",
        "fallback_message": "Không sao, mình thử một lựa chọn khác nhé.",
        "asset_source": "original-app-asset",
        "verification_status": "demo",
    },
    {
        "id": "thin",
        "name": "Thìn",
        "animal": "Rồng",
        "theme_color": "#C2410C",
        "secondary_color": "#F59E0B",
        "emoji": "🐉",
        "greeting": "Rồng power, hôm nay thử một món thật đặc biệt nhé!",
        "encouragement": "Món này đang chờ bạn khám phá.",
        "fallback_message": "Không sao, mình thử một lựa chọn khác nhé.",
        "asset_source": "original-app-asset",
        "verification_status": "demo",
    },
    {
        "id": "ty-snake",
        "name": "Tỵ",
        "animal": "Rắn",
        "theme_color": "#16A34A",
        "secondary_color": "#86EFAC",
        "emoji": "🐍",
        "greeting": "Rắn khéo léo, hôm nay khám phá một hương vị mới nào!",
        "encouragement": "Món này đang chờ bạn khám phá.",
        "fallback_message": "Không sao, mình thử một lựa chọn khác nhé.",
        "asset_source": "original-app-asset",
        "verification_status": "demo",
    },
    {
        "id": "ngo",
        "name": "Ngọ",
        "animal": "Ngựa",
        "theme_color": "#DC2626",
        "secondary_color": "#FCA5A5",
        "emoji": "🐴",
        "greeting": "Ngựa phóng khoáng, hôm nay phiêu lưu cùng một món mới!",
        "encouragement": "Món này đang chờ bạn khám phá.",
        "fallback_message": "Không sao, mình thử một lựa chọn khác nhé.",
        "asset_source": "original-app-asset",
        "verification_status": "demo",
    },
    {
        "id": "mui",
        "name": "Mùi",
        "animal": "Dê",
        "theme_color": "#0D9488",
        "secondary_color": "#5EEAD4",
        "emoji": "🐐",
        "greeting": "Dê hiền lành, hôm nay thưởng thức một món nhẹ nhàng nhé!",
        "encouragement": "Món này đang chờ bạn khám phá.",
        "fallback_message": "Không sao, mình thử một lựa chọn khác nhé.",
        "asset_source": "original-app-asset",
        "verification_status": "demo",
    },
    {
        "id": "than",
        "name": "Thân",
        "animal": "Khỉ",
        "theme_color": "#F97316",
        "secondary_color": "#FDBA74",
        "emoji": "🐒",
        "greeting": "Khỉ tinh nghịch, hôm nay chơi trò random món nào!",
        "encouragement": "Món này đang chờ bạn khám phá.",
        "fallback_message": "Không sao, mình thử một lựa chọn khác nhé.",
        "asset_source": "original-app-asset",
        "verification_status": "demo",
    },
    {
        "id": "dau",
        "name": "Dậu",
        "animal": "Gà",
        "theme_color": "#E11D48",
        "secondary_color": "#FDA4AF",
        "emoji": "🐓",
        "greeting": "Gà mạnh mẽ, dậy sớm đi ăn sáng nào!",
        "encouragement": "Món này đang chờ bạn khám phá.",
        "fallback_message": "Không sao, mình thử một lựa chọn khác nhé.",
        "asset_source": "original-app-asset",
        "verification_status": "demo",
    },
    {
        "id": "tuat",
        "name": "Tuất",
        "animal": "Chó",
        "theme_color": "#7C3AED",
        "secondary_color": "#C4B5FD",
        "emoji": "🐕",
        "greeting": "Chó trung thành, hôm nay cùng nhau ăn món ngon nào!",
        "encouragement": "Món này đang chờ bạn khám phá.",
        "fallback_message": "Không sao, mình thử một lựa chọn khác nhé.",
        "asset_source": "original-app-asset",
        "verification_status": "demo",
    },
    {
        "id": "hoi",
        "name": "Hợi",
        "animal": "Lợn",
        "theme_color": "#EC4899",
        "secondary_color": "#F9A8D4",
        "emoji": "🐷",
        "greeting": "Lợn đáng yêu, hôm nay ăn gì cũng được, miễn là ngon!",
        "encouragement": "Món này đang chờ bạn khám phá.",
        "fallback_message": "Không sao, mình thử một lựa chọn khác nhé.",
        "asset_source": "original-app-asset",
        "verification_status": "demo",
    },
]

MASCOT_MAP: dict[str, dict[str, Any]] = {m["id"]: m for m in MASCOTS}


def get_mascot(mascot_id: str) -> dict[str, Any] | None:
    return MASCOT_MAP.get(mascot_id)


# ============================================================
# Zodiac-themed palettes (1 per mascot, replaces "Hội mèo")
# ============================================================

ZODIAC_THEMES: list[dict[str, Any]] = [
    {
        "id": "rat",
        "name": "Nhà Tý",
        "mascot_id": "ty",
        "colors": {
            "bg": "#F8FAFC",
            "bg_gradient": "linear-gradient(160deg, #F8FAFC 0%, #F1F5F9 45%, #E2E8F0 100%)",
            "card_bg": "#FFFFFF",
            "text": "#0F172A",
            "text_muted": "#64748B",
            "accent": "#94A3B8",
            "accent_dark": "#64748B",
            "accent_light": "#F1F5F9",
            "border": "#CBD5E1",
        },
        "is_unlocked": True,
    },
    {
        "id": "ox",
        "name": "Nhà Sửu",
        "mascot_id": "suu",
        "colors": {
            "bg": "#FFFBEB",
            "bg_gradient": "linear-gradient(160deg, #FFFBEB 0%, #FEF3C7 45%, #FDE68A 100%)",
            "card_bg": "#FFFFFF",
            "text": "#451A03",
            "text_muted": "#92400E",
            "accent": "#D97706",
            "accent_dark": "#B45309",
            "accent_light": "#FEF3C7",
            "border": "#FCD34D",
        },
        "is_unlocked": True,
    },
    {
        "id": "tiger",
        "name": "Nhà Dần",
        "mascot_id": "dan",
        "colors": {
            "bg": "#FFF7ED",
            "bg_gradient": "linear-gradient(160deg, #FFF7ED 0%, #FFEDD5 45%, #FED7AA 100%)",
            "card_bg": "#FFFFFF",
            "text": "#431407",
            "text_muted": "#9A3412",
            "accent": "#EA580C",
            "accent_dark": "#C2410C",
            "accent_light": "#FFEDD5",
            "border": "#FDBA74",
        },
        "is_unlocked": True,
    },
    {
        "id": "rabbit",
        "name": "Nhà Mão",
        "mascot_id": "mao",
        "colors": {
            "bg": "#FDF2F8",
            "bg_gradient": "linear-gradient(160deg, #FDF2F8 0%, #FCE7F3 45%, #FBCFE8 100%)",
            "card_bg": "#FFFFFF",
            "text": "#500724",
            "text_muted": "#9D174D",
            "accent": "#DB2777",
            "accent_dark": "#BE185D",
            "accent_light": "#FCE7F3",
            "border": "#F9A8D4",
        },
        "is_unlocked": True,
    },
    {
        "id": "dragon",
        "name": "Nhà Rồng",
        "mascot_id": "thin",
        "colors": {
            "bg": "#FFF7ED",
            "bg_gradient": "linear-gradient(160deg, #FFF7ED 0%, #FEF3C7 45%, #FDE68A 100%)",
            "card_bg": "#FFFFFF",
            "text": "#431407",
            "text_muted": "#92400E",
            "accent": "#C2410C",
            "accent_dark": "#9A3412",
            "accent_light": "#FEF3C7",
            "border": "#FCD34D",
        },
        "is_unlocked": True,
    },
    {
        "id": "snake",
        "name": "Nhà Tỵ",
        "mascot_id": "ty-snake",
        "colors": {
            "bg": "#F0FDF4",
            "bg_gradient": "linear-gradient(160deg, #F0FDF4 0%, #DCFCE7 45%, #BBF7D0 100%)",
            "card_bg": "#FFFFFF",
            "text": "#052E16",
            "text_muted": "#166534",
            "accent": "#16A34A",
            "accent_dark": "#15803D",
            "accent_light": "#DCFCE7",
            "border": "#86EFAC",
        },
        "is_unlocked": True,
    },
    {
        "id": "horse",
        "name": "Nhà Ngọ",
        "mascot_id": "ngo",
        "colors": {
            "bg": "#FEF2F2",
            "bg_gradient": "linear-gradient(160deg, #FEF2F2 0%, #FEE2E2 45%, #FECACA 100%)",
            "card_bg": "#FFFFFF",
            "text": "#450A0A",
            "text_muted": "#991B1B",
            "accent": "#DC2626",
            "accent_dark": "#B91C1C",
            "accent_light": "#FEE2E2",
            "border": "#FCA5A5",
        },
        "is_unlocked": True,
    },
    {
        "id": "goat",
        "name": "Nhà Mùi",
        "mascot_id": "mui",
        "colors": {
            "bg": "#F0FDFA",
            "bg_gradient": "linear-gradient(160deg, #F0FDFA 0%, #CCFBF1 45%, #99F6E4 100%)",
            "card_bg": "#FFFFFF",
            "text": "#042F2E",
            "text_muted": "#115E59",
            "accent": "#0D9488",
            "accent_dark": "#0F766E",
            "accent_light": "#CCFBF1",
            "border": "#5EEAD4",
        },
        "is_unlocked": True,
    },
    {
        "id": "monkey",
        "name": "Nhà Thân",
        "mascot_id": "than",
        "colors": {
            "bg": "#FFF7ED",
            "bg_gradient": "linear-gradient(160deg, #FFF7ED 0%, #FFEDD5 45%, #FED7AA 100%)",
            "card_bg": "#FFFFFF",
            "text": "#431407",
            "text_muted": "#9A3412",
            "accent": "#F97316",
            "accent_dark": "#EA580C",
            "accent_light": "#FFEDD5",
            "border": "#FDBA74",
        },
        "is_unlocked": True,
    },
    {
        "id": "rooster",
        "name": "Nhà Dậu",
        "mascot_id": "dau",
        "colors": {
            "bg": "#FFF1F2",
            "bg_gradient": "linear-gradient(160deg, #FFF1F2 0%, #FFE4E6 45%, #FECDD3 100%)",
            "card_bg": "#FFFFFF",
            "text": "#4C0519",
            "text_muted": "#9F1239",
            "accent": "#E11D48",
            "accent_dark": "#BE123C",
            "accent_light": "#FFE4E6",
            "border": "#FDA4AF",
        },
        "is_unlocked": True,
    },
    {
        "id": "dog",
        "name": "Nhà Tuất",
        "mascot_id": "tuat",
        "colors": {
            "bg": "#F5F3FF",
            "bg_gradient": "linear-gradient(160deg, #F5F3FF 0%, #EDE9FE 45%, #DDD6FE 100%)",
            "card_bg": "#FFFFFF",
            "text": "#2E1065",
            "text_muted": "#5B21B6",
            "accent": "#7C3AED",
            "accent_dark": "#6D28D9",
            "accent_light": "#EDE9FE",
            "border": "#C4B5FD",
        },
        "is_unlocked": True,
    },
    {
        "id": "pig",
        "name": "Nhà Hợi",
        "mascot_id": "hoi",
        "colors": {
            "bg": "#FDF2F8",
            "bg_gradient": "linear-gradient(160deg, #FDF2F8 0%, #FCE7F3 45%, #FBCFE8 100%)",
            "card_bg": "#FFFFFF",
            "text": "#500724",
            "text_muted": "#9D174D",
            "accent": "#EC4899",
            "accent_dark": "#DB2777",
            "accent_light": "#FCE7F3",
            "border": "#F9A8D4",
        },
        "is_unlocked": True,
    },
]

ZODIAC_THEME_MAP: dict[str, dict[str, Any]] = {t["id"]: t for t in ZODIAC_THEMES}


def get_zodiac_theme(theme_id: str) -> dict[str, Any] | None:
    return ZODIAC_THEME_MAP.get(theme_id)


# ============================================================
# Fate messages using selected mascot (replaces LINH_VAT_* from models.py)
# ============================================================

FATE_MESSAGES: list[str] = [
    "Bạn thật thiếu quyết đoán. Hôm nay hãy ăn đúng món này đi!",
    "Trời đất đã chọn ngay món này cho bạn rồi, đừng lăn tăn nữa!",
    "Linh vật thấy bạn xúc xắc mãi — quyết định luôn đi, đói quá rồi!",
    "Vận may đang nằm trong bát này. Ăn đi, ăn là gặp may!",
    "Thôi xong, trời bảo hôm nay món này là duyên của bạn!",
    "Món này gọi tên bạn rồi, nghe theo trái tim đi nào!",
    "Đã 3 lần rồi — linh vật mách nước, thử món này xem sao!",
]


# ============================================================
# Birthday → zodiac suggestion (entertainment only)
# ============================================================

ZODIAC_BOUNDARIES: list[tuple[str, str, int, int, str]] = [
    ("aries",   "Bạch Dương", 3, 21, "♈"),
    ("taurus",  "Kim Ngưu",   4, 20, "♉"),
    ("gemini",  "Song Tử",     5, 21, "♊"),
    ("cancer",  "Cự Giải",    6, 22, "♋"),
    ("leo",     "Sư Tử",       7, 23, "♌"),
    ("virgo",   "Xử Nữ",      8, 23, "♍"),
    ("libra",   "Thiên Bình",  9, 23, "♎"),
    ("scorpio", "Bọ Cạp",     10, 24, "♏"),
    ("sagittarius", "Nhân Mã", 11, 22, "♐"),
    ("capricorn", "Ma Kết",   12, 22, "♑"),
    ("aquarius", "Bảo Bình",  1, 19, "♒"),
    ("pisces",  "Song Ngư",   2, 19, "♓"),
]

# Maps zodiac sign key to the mascot ID that "corresponds" loosely for entertainment
SIGN_TO_MASCOT: dict[str, str] = {
    "aries": "dan",       # Hổ
    "taurus": "suu",      # Trâu
    "gemini": "than",     # Khỉ
    "cancer": "mao",      # Mèo
    "leo": "dan",         # Hổ
    "virgo": "mui",       # Dê
    "libra": "dau",       # Gà
    "scorpio": "ty-snake",# Rắn
    "sagittarius": "ngo", # Ngựa
    "capricorn": "suu",   # Trâu
    "aquarius": "ty",     # Chuột
    "pisces": "hoi",      # Lợn
}


def suggest_mascot(day: int, month: int) -> str | None:
    """Return mascot_id suggestion from birthday (entertainment only).

    Western zodiac dates (month/day boundaries):
        Aries       Mar 21 - Apr 19
        Taurus      Apr 20 - May 20
        Gemini      May 21 - Jun 20
        Cancer      Jun 21 - Jul 22
        Leo         Jul 23 - Aug 22
        Virgo       Aug 23 - Sep 22
        Libra       Sep 23 - Oct 22
        Scorpio     Oct 23 - Nov 21
        Sagittarius Nov 22 - Dec 21
        Capricorn   Dec 22 - Jan 19
        Aquarius    Jan 20 - Feb 18
        Pisces      Feb 19 - Mar 20
    """
    if not (1 <= month <= 12 and 1 <= day <= 31):
        return None

    # (start_month, start_day, zodiac_key) — ordered by calendar
    _BOUNDARIES = [
        (1,  20, "aquarius"),
        (2,  19, "pisces"),
        (3,  21, "aries"),
        (4,  20, "taurus"),
        (5,  21, "gemini"),
        (6,  22, "cancer"),
        (7,  23, "leo"),
        (8,  23, "virgo"),
        (9,  23, "libra"),
        (10, 24, "scorpio"),
        (11, 22, "sagittarius"),
        (12, 22, "capricorn"),
    ]

    for i, (sm, sd, key) in enumerate(_BOUNDARIES):
        # next boundary start
        nm, nd, nkey = _BOUNDARIES[(i + 1) % 12]
        if (month == sm and day >= sd) or (month == sm + 1 and day < nd) or (nm > sm and sm < month < nm):
            return SIGN_TO_MASCOT.get(key)

    # Edge: Aquarius spans Jan 20 – Feb 18 (wraps around year)
    if (month == 1 and day >= 20) or (month == 2 and day < 19):
        return SIGN_TO_MASCOT["aquarius"]
    return None
