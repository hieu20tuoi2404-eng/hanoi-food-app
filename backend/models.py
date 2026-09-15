"""Pydantic models for request/response validation."""

from __future__ import annotations

from typing import Any, Optional

from pydantic import BaseModel, Field


# ============================================================
# Rarity tiers — NEW gamified scale
# ============================================================
# (min_rating, key, label, level)

RARITY_TIERS: list[tuple[float, str, str, int]] = [
    (9.5, "legendary", "Huyền thoại", 4),
    (8.5, "epic", "Sử thi", 3),
    (7.5, "rare", "Hiếm", 2),
    (0.0, "common", "Thường", 1),
]


def compute_rarity(rating: float) -> dict[str, str | int]:
    """Return rarity info for a given average rating."""
    for threshold, key, label, level in RARITY_TIERS:
        if rating >= threshold:
            return {"key": key, "label": label, "level": level}
    return {"key": "common", "label": "Thường", "level": 1}


# ============================================================
# Theme configs
# ============================================================

THEMES: list[dict[str, Any]] = [
    {
        "id": "ha-noi-co-dien",
        "name": "Hà Nội cổ điển",
        "colors": {
            "bg": "#faf8f5",
            "bg_gradient": "linear-gradient(160deg, #fff8f0 0%, #faf5ef 45%, #f6f0ea 100%)",
            "card_bg": "#ffffff",
            "text": "#211a14",
            "text_muted": "#6b6257",
            "accent": "#d4451a",
            "accent_dark": "#b03810",
            "accent_light": "#fff1eb",
            "border": "#e9e2d9",
        },
        "mascot": "default",
        "is_unlocked": True,
    },
    {
        "id": "pho-dem",
        "name": "Phố đêm",
        "colors": {
            "bg": "#0f172a",
            "bg_gradient": "linear-gradient(160deg, #0f172a 0%, #1e293b 45%, #1a1f33 100%)",
            "card_bg": "#1e293b",
            "text": "#e2e8f0",
            "text_muted": "#94a3b8",
            "accent": "#f59e0b",
            "accent_dark": "#d97706",
            "accent_light": "#1e293b",
            "border": "#334155",
        },
        "mascot": "owl",
        "is_unlocked": True,
    },
    {
        "id": "hoi-meo",
        "name": "Hội mèo",
        "colors": {
            "bg": "#fef7ee",
            "bg_gradient": "linear-gradient(160deg, #fef7ee 0%, #fff5e6 45%, #fef0dc 100%)",
            "card_bg": "#ffffff",
            "text": "#1c1917",
            "text_muted": "#78716c",
            "accent": "#f97316",
            "accent_dark": "#ea580c",
            "accent_light": "#fff7ed",
            "border": "#e7e5e4",
        },
        "mascot": "cat",
        "is_unlocked": True,
    },
    {
        "id": "healthy",
        "name": "Healthy",
        "colors": {
            "bg": "#f0fdf4",
            "bg_gradient": "linear-gradient(160deg, #f0fdf4 0%, #ecfdf5 45%, #f0faf5 100%)",
            "card_bg": "#ffffff",
            "text": "#14532d",
            "text_muted": "#4ade80",
            "accent": "#16a34a",
            "accent_dark": "#15803d",
            "accent_light": "#dcfce7",
            "border": "#bbf7d0",
        },
        "mascot": "leaf",
        "is_unlocked": True,
    },
    {
        "id": "toi-gian",
        "name": "Tối giản",
        "colors": {
            "bg": "#fafafa",
            "bg_gradient": "linear-gradient(160deg, #fafafa 0%, #f5f5f5 45%, #fafafa 100%)",
            "card_bg": "#ffffff",
            "text": "#18181b",
            "text_muted": "#71717a",
            "accent": "#18181b",
            "accent_dark": "#09090b",
            "accent_light": "#f4f4f5",
            "border": "#e4e4e7",
        },
        "mascot": "none",
        "is_unlocked": True,
    },
    {
        "id": "tet-le-hoi",
        "name": "Tết / Lễ hội",
        "colors": {
            "bg": "#fef2f2",
            "bg_gradient": "linear-gradient(160deg, #fef2f2 0%, #fff1f2 45%, #fef7f7 100%)",
            "card_bg": "#ffffff",
            "text": "#1c1917",
            "text_muted": "#9a3412",
            "accent": "#dc2626",
            "accent_dark": "#b91c1c",
            "accent_light": "#fef2f2",
            "border": "#fecaca",
        },
        "mascot": "lantern",
        "is_unlocked": True,
    },
]


# ============================================================
# Exploration levels
# ============================================================

EXPLORATION_LEVELS: list[dict[str, Any]] = [
    {"key": "newcomer", "name": "Người mới", "min_xp": 0, "icon": "🌱", "desc": "Vừa mới bắt đầu khám phá Hà Nội"},
    {"key": "foodie", "name": "Người sành ăn", "min_xp": 20, "icon": "🍽", "desc": "Đã thử qua kha khá món"},
    {"key": "hunter", "name": "Thợ săn món ngon", "min_xp": 50, "icon": "🎯", "desc": "Biết chính xác món nào đáng thử"},
    {"key": "explorer", "name": "Nhà khám phá Hà Nội", "min_xp": 100, "icon": "🏆", "desc": "Đã đi qua mọi ngóc ngách ẩm thực"},
]


ACHIEVEMENTS: list[dict[str, Any]] = [
    {"key": "first_bite", "name": "Miếng đầu tiên", "desc": "Xem chi tiết một món ăn", "icon": "🍴", "xp": 2},
    {"key": "five_dishes", "name": "Khai vị", "desc": "Xem 5 món ăn khác nhau", "icon": "🍱", "xp": 5},
    {"key": "ten_dishes", "name": "Ăn đa dạng", "desc": "Xem 10 món ăn", "icon": "🍜", "xp": 10},
    {"key": "all_dishes", "name": "Quán quân nếm thử", "desc": "Xem tất cả 30 món", "icon": "👑", "xp": 30},
    {"key": "first_review", "name": "Đánh giá đầu tiên", "desc": "Viết một đánh giá", "icon": "✍️", "xp": 3},
    {"key": "five_reviews", "name": "Reviewer cứng", "desc": "Viết 5 đánh giá", "icon": "📝", "xp": 10},
    {"key": "three_districts", "name": "Rong ruổi", "desc": "Xem món từ 3 quận khác nhau", "icon": "🗺", "xp": 5},
    {"key": "all_meals", "name": "No từ sáng đến tối", "desc": "Xem đủ 4 nhóm bữa", "icon": "⏰", "xp": 8},
    {"key": "rare_finder", "name": "Săn đồ hiếm", "desc": "Xem một món cấp Hiếm trở lên", "icon": "💎", "xp": 5},
    {"key": "legendary_finder", "name": "Chạm tới huyền thoại", "desc": "Xem một món Huyền thoại", "icon": "🌟", "xp": 15},
]


def get_exploration_level(xp: int) -> dict[str, Any]:
    """Return the current level info for a given XP total."""
    result = EXPLORATION_LEVELS[0]
    for lvl in EXPLORATION_LEVELS:
        if xp >= lvl["min_xp"]:
            result = lvl
    return result


def get_next_level(xp: int) -> Optional[dict[str, Any]]:
    """Return the next level to unlock, or None if max level."""
    for lvl in EXPLORATION_LEVELS:
        if xp < lvl["min_xp"]:
            return lvl
    return None


# ============================================================
# Zodiac (kept from previous version)
# ============================================================

ZODIAC_SIGNS: list[dict[str, Any]] = [
    {"key": "aries", "name": "Bạch Dương", "emoji": "♈", "month_day": (3, 21), "label": "23/3 - 19/4"},
    {"key": "taurus", "name": "Kim Ngưu", "emoji": "♉", "month_day": (4, 20), "label": "20/4 - 20/5"},
    {"key": "gemini", "name": "Song Tử", "emoji": "♊", "month_day": (5, 21), "label": "21/5 - 21/6"},
    {"key": "cancer", "name": "Cự Giải", "emoji": "♋", "month_day": (6, 22), "label": "22/6 - 22/7"},
    {"key": "leo", "name": "Sư Tử", "emoji": "♌", "month_day": (7, 23), "label": "23/7 - 22/8"},
    {"key": "virgo", "name": "Xử Nữ", "emoji": "♍", "month_day": (8, 23), "label": "23/8 - 22/9"},
    {"key": "libra", "name": "Thiên Bình", "emoji": "♎", "month_day": (9, 23), "label": "23/9 - 23/10"},
    {"key": "scorpio", "name": "Bọ Cạp", "emoji": "♏", "month_day": (10, 24), "label": "24/10 - 22/11"},
    {"key": "sagittarius", "name": "Nhân Mã", "emoji": "♐", "month_day": (11, 23), "label": "23/11 - 21/12"},
    {"key": "capricorn", "name": "Ma Kết", "emoji": "♑", "month_day": (12, 22), "label": "22/12 - 19/1"},
    {"key": "aquarius", "name": "Bảo Bình", "emoji": "♒", "month_day": (1, 20), "label": "20/1 - 18/2"},
    {"key": "pisces", "name": "Song Ngư", "emoji": "♓", "month_day": (2, 19), "label": "19/2 - 20/3"},
]

ZODIAC_HINTS: dict[str, dict[str, Any]] = {
    "aries":      {"flavour": "món có vị đậm và nhiều năng lượng", "hint_tags": ["spicy", "high_protein"]},
    "taurus":     {"flavour": "món ấm bụng, đậm vị và nhiều topping", "hint_tags": ["rich"]},
    "gemini":     {"flavour": "món lạ, nhiều màu sắc và thú vị để thử", "hint_tags": ["colorful"]},
    "cancer":     {"flavour": "món nước ấm, nhẹ nhàng và an toàn", "hint_tags": ["light"]},
    "leo":        {"flavour": "món \"xịn xò\" xứng tầm để khoe với bạn bè", "hint_tags": ["high_price"]},
    "virgo":      {"flavour": "món gọn gàng, vệ sinh và vừa miệng", "hint_tags": ["light_oil"]},
    "libra":      {"flavour": "món cân bằng hài hoà cả vị lẫn màu", "hint_tags": ["balanced"]},
    "scorpio":    {"flavour": "món đậm đà, nhiều gia vị và bí ẩn", "hint_tags": ["spicy"]},
    "sagittarius":{"flavour": "món mới lạ đáng để ăn thử một lần", "hint_tags": ["new"]},
    "capricorn":  {"flavour": "món vừa no, vừa tiết kiệm và chất lượng", "hint_tags": ["value"]},
    "aquarius":   {"flavour": "món khác biệt, sáng tạo không theo khuôn", "hint_tags": ["unique"]},
    "pisces":     {"flavour": "món thanh dịu, mềm mại và gần gũi", "hint_tags": ["light"]},
}


def determine_zodiac(day: int, month: int) -> str | None:
    """Return zodiac sign key for a birthday (month/day). Boundary-safe.

    Uses the sign start boundaries; the active sign is the one whose start
    boundary is the latest one at or before the date. Dates before the first
    boundary belong to the final sign (Capricorn, 22/12).
    """
    # Sorted by (start_month, start_day): the sign active on each boundary.
    boundaries = [
        (1, 20, "aquarius"),
        (2, 19, "pisces"),
        (3, 21, "aries"),
        (4, 20, "taurus"),
        (5, 21, "gemini"),
        (6, 22, "cancer"),
        (7, 23, "leo"),
        (8, 23, "virgo"),
        (9, 23, "libra"),
        (10, 24, "scorpio"),
        (11, 23, "sagittarius"),
        (12, 22, "capricorn"),
    ]
    for b_month, b_day, key in boundaries:
        if (month, day) < (b_month, b_day):
            # Date is before this boundary -> previous boundary's sign.
            return boundaries[boundaries.index((b_month, b_day, key)) - 1][2]
    return "capricorn"


# ============================================================
# Lookup / filter options
# ============================================================

HEALTHY_OPTIONS = [
    {"id": "healthy", "label": "Healthy", "desc": "Món nhiều rau, ít dầu, ít tinh bột nặng"},
    {"id": "light_oil", "label": "Ít dầu mỡ", "desc": "oil_level = low"},
    {"id": "rich_oil", "label": "Dầu mỡ thoải mái", "desc": "oil_level = high"},
    {"id": "high_protein", "label": "Nhiều đạm", "desc": "protein_level = high"},
    {"id": "vegetarian", "label": "Ăn chay", "desc": "vegetarian = true"},
    {"id": "spicy", "label": "Ăn cay", "desc": "spicy_level >= medium"},
    {"id": "light", "label": "Ăn nhẹ", "desc": "portion nhẹ, snack/breakfast"},
]

OCCASION_OPTIONS = [
    {"id": "solo", "label": "Đi một mình", "desc": "suitable_for_alone"},
    {"id": "date", "label": "Đi date", "desc": "date_friendly"},
    {"id": "hangout", "label": "Hẹn hò", "desc": "date_friendly / quiet"},
    {"id": "friends", "label": "Đi với bạn bè", "desc": "group_friendly"},
    {"id": "family", "label": "Đi gia đình", "desc": "family_friendly"},
    {"id": "drinking", "label": "Đi nhậu", "desc": "drinking_friendly"},
    {"id": "quick", "label": "Ăn nhanh", "desc": "quick_food"},
    {"id": "work", "label": "Làm việc / gặp khách", "desc": "work_friendly / quiet"},
]

COLOR_OPTIONS = [
    {"id": "red", "label": "Đỏ"},
    {"id": "yellow", "label": "Vàng"},
    {"id": "green", "label": "Xanh"},
    {"id": "white", "label": "Trắng"},
    {"id": "brown", "label": "Nâu"},
    {"id": "orange", "label": "Cam"},
    {"id": "purple", "label": "Tím"},
    {"id": "multi", "label": "Nhiều màu"},
]

MEAL_TYPES = [
    {"id": "breakfast", "label": "Bữa sáng"},
    {"id": "lunch", "label": "Bữa trưa"},
    {"id": "dinner", "label": "Bữa tối"},
    {"id": "snack", "label": "Ăn vặt"},
]


# ============================================================
# Request / Response models
# ============================================================

class DishSummary(BaseModel):
    id: int
    name: str
    slug: str
    description: str
    meal_type: str
    image_url: str
    image_source: str
    avg_rating: float
    avg_price: int
    is_demo: bool
    rarity: dict[str, str | int] = Field(
        default_factory=lambda: compute_rarity(5.0),
        description="Thông tin độ hiếm",
    )
    healthy_score: Optional[int] = Field(default=None, ge=1, le=10)
    oil_level: str = Field(default="unknown")
    spicy_level: str = Field(default="none")
    vegetarian: bool = False
    protein_level: str = Field(default="unknown")
    calories_estimate: Optional[int] = None
    calories_source: str = Field(default="")
    dominant_color: str = Field(default="")
    color_tags: list[str] = []
    color_source: str = Field(default="")
    verification_status: str = Field(default="demo")
    cuisine: str = Field(default="Việt Nam")
    key_ingredients: list[str] = []
    dish_origin: str = Field(default="Hà Nội")
    created_at: str


class Restaurant(BaseModel):
    id: int
    dish_id: int
    name: str
    address: str
    district: str
    hours: str
    price_range: str
    maps_link: str
    maps_source: str
    is_demo: bool
    occasion_tags: list[str] = []
    tags_verification: str = Field(default="demo")


class Recipe(BaseModel):
    id: int
    dish_id: int
    ingredients: list[str]
    portions: str
    cook_time: str
    steps: list[str]
    source: str


class Review(BaseModel):
    id: int
    dish_id: int
    rating: int = Field(ge=1, le=10)
    comment: str
    reviewer_name: str
    is_demo: bool
    created_at: str


class ReviewCreate(BaseModel):
    rating: int = Field(ge=1, le=10, description="Điểm đánh giá 1-10")
    comment: str = Field(min_length=3, max_length=500, description="Nhận xét")
    reviewer_name: str = Field(min_length=1, max_length=100, default="Ẩn danh")


class DishDetail(DishSummary):
    restaurants: list[Restaurant] = []
    recipe: Optional[Recipe] = None
    reviews: list[Review] = []


class Category(BaseModel):
    name: str
    slug: str
    count: int


# ----- Preferences -----

class Preferences(BaseModel):
    healthy_options: list[dict[str, Any]]
    occasion_options: list[dict[str, Any]]
    color_options: list[dict[str, Any]]
    meal_types: list[dict[str, Any]]


# ----- Zodiac -----

class ZodiacCreate(BaseModel):
    day: int = Field(ge=1, le=31)
    month: int = Field(ge=1, le=12)
    year: Optional[int] = Field(default=None, ge=1900, le=2100)
    consent_save: bool = Field(default=False)


class ZodiacProfile(BaseModel):
    id: int
    day: int
    month: int
    year: Optional[int] = None
    consent_save: bool = False
    sign_key: str
    sign_name: str
    sign_emoji: str
    entertainment_note: str = "Gợi ý vui, không phải tư vấn khoa học."


class ZodiacRecommendation(BaseModel):
    sign: dict[str, Any]
    flavour: str
    dish: Optional[dict[str, Any]] = None
    entertainment_note: str = "Gợi ý vui, không phải tư vấn khoa học."


class ZodiacDeleteResult(BaseModel):
    deleted: bool = True
    message: str = "Đã xóa thông tin ngày sinh."


# ----- Advanced random -----

class AdvancedRandomRequest(BaseModel):
    meal: Optional[str] = None
    min_price: Optional[int] = Field(default=None, ge=0)
    max_price: Optional[int] = Field(default=None, ge=0)
    diet: Optional[str] = None
    occasion: Optional[str] = None
    color: Optional[str] = None
    exclude_slug: Optional[str] = None


# ----- Fate -----

LINH_VAT_MESSAGES: list[str] = [
    "Bạn thật thiếu quyết đoán. Hôm nay hãy ăn đúng món này đi!",
    "Trời đất đã chọn ngay món này cho bạn rồi, đừng lăn tăn nữa!",
    "Linh vật thấy bạn xúc xắc mãi — quyết định luôn đi, đói quá rồi!",
    "Vận may đang nằm trong bát này. Ăn đi, ăn là gặp may!",
    "Thôi xong, trời bảo hôm nay món này là duyên của bạn!",
]

LINH_VAT_NAMES: list[dict[str, str]] = [
    {"key": "tho", "label": "Mèo thần tài", "emoji": "🐱"},
    {"key": "cho", "label": "Chó vàng", "emoji": "🐶"},
    {"key": "gau", "label": "Gấu trúc lười", "emoji": "🐼"},
    {"key": "shiba", "label": "Shiba hay gắt", "emoji": "🐕"},
    {"key": "roi", "label": "Rồng nhỏ", "emoji": "🐉"},
    {"key": "ech", "label": "Ếch may mắn", "emoji": "🐸"},
    {"key": "ca", "label": "Cá vàng", "emoji": "🐠"},
    {"key": "ho", "label": "Hổ dễ thương", "emoji": "🐯"},
]


class FateRollRequest(BaseModel):
    meal: Optional[str] = None
    diet: Optional[str] = None
    occasion: Optional[str] = None
    color: Optional[str] = None
    likely: bool = Field(default=False)
    exclude_slug: Optional[str] = None


class FateRollResponse(BaseModel):
    roll: int
    dish: dict[str, Any]
    linh_vat: Optional[dict[str, str]] = None
    message: Optional[str] = None
    likely_done: bool = False


# ----- Group voting -----

class GroupRoomCreate(BaseModel):
    host_name: str = Field(min_length=1, max_length=40)
    config: dict[str, Any] = Field(default_factory=dict)
    ends_at: Optional[str] = None


class GroupJoinRequest(BaseModel):
    voter_name: str = Field(min_length=1, max_length=40)


class GroupVoteRequest(BaseModel):
    voter_name: str = Field(min_length=1, max_length=40)
    dish_id: int


class VoteTallyItem(BaseModel):
    dish: dict[str, Any]
    votes: int
    voters: list[str] = []


class VoteTally(BaseModel):
    winner: Optional[dict[str, Any]] = None
    tied: list[dict[str, Any]] = []
    tally: list[VoteTallyItem]
    total_votes: int
    status: str = "open"


class FinishResult(BaseModel):
    status: str = "finished"
    winner: Optional[dict[str, Any]] = None
    tied: list[dict[str, Any]] = []
    total_votes: int = 0


# ----- Themes -----

class ThemeSelection(BaseModel):
    theme_id: str
    updated_at: str


# ----- Exploration -----

class ExplorationStats(BaseModel):
    session_id: str
    level: dict[str, Any]
    next_level: Optional[dict[str, Any]] = None
    xp: int
    viewed_count: int
    reviewed_count: int
    districts_explored: int
    meal_types_explored: int
    achievements: list[dict[str, Any]]
    unlocked_count: int
    total_achievements: int
