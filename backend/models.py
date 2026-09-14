"""Pydantic models for request/response validation."""

from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, Field


# ----- Rarity tiers (gamified, inspired by Trưa Nay Ăn Gì?) -----

# (min_rating, key, label, star_level)
RARITY_TIERS: list[tuple[float, str, str, int]] = [
    (9.0, "cuc-pham", "CỰC PHẨM", 5),
    (8.5, "dac-biet", "★ ĐẶC BIỆT", 4),
    (8.0, "hiem", "HIẾM", 3),
    (7.0, "quoc-dan", "QUỐC DÂN", 2),
    (0.0, "toi-mat", "TỐI MẬT", 1),
]


def compute_rarity(rating: float) -> dict[str, str | int]:
    """Return rarity info for a given average rating."""
    for threshold, key, label, level in RARITY_TIERS:
        if rating >= threshold:
            return {"key": key, "label": label, "level": level}
    return {"key": "toi-mat", "label": "TỐI MẬT", "level": 1}


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
        description="Thông tin độ hiếm tính từ avg_rating",
    )
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