"""Backend tests: random dish, meal filter, Google Maps URL, review creation."""

from __future__ import annotations

import os
import sys
import tempfile
from pathlib import Path

import pytest

sys.path.insert(0, os.path.dirname(__file__))

import database  # noqa: E402
from main import app  # noqa: E402

from fastapi.testclient import TestClient  # noqa: E402


@pytest.fixture(scope="session")
def client():
    """Fresh temp DB per test session."""
    tmp = tempfile.mkdtemp(prefix="hanoi_test_")
    database.DATABASE_PATH = Path(tmp) / "test.db"
    with TestClient(app) as c:
        yield c


MEALS = ["breakfast", "lunch", "dinner", "snack"]


# ---------- health & categories ----------

def test_health(client):
    r = client.get("/api/health")
    assert r.status_code == 200
    data = r.json()
    assert data["status"] == "healthy"
    assert data["demo_mode"] is True


def test_categories_count(client):
    r = client.get("/api/categories")
    assert r.status_code == 200
    cats = r.json()
    assert len(cats) == 4
    slugs = {c["slug"] for c in cats}
    assert slugs == set(MEALS)


# ---------- list dishes ----------

def test_list_dishes_total(client):
    r = client.get("/api/dishes")
    assert r.status_code == 200
    dishes = r.json()
    assert len(dishes) >= 30  # yêu cầu ~30 món demo


def test_filter_by_meal(client):
    for meal in MEALS:
        r = client.get("/api/dishes", params={"meal": meal})
        assert r.status_code == 200
        dishes = r.json()
        assert len(dishes) > 0, f"meal={meal} should have data"
        for d in dishes:
            assert d["meal_type"] == meal


def test_filter_by_meal_invalid(client):
    r = client.get("/api/dishes", params={"meal": "midnight"})
    assert r.status_code == 200
    assert r.json() == []


def test_filter_by_rating(client):
    r = client.get("/api/dishes", params={"min_rating": 9})
    assert r.status_code == 200
    for d in r.json():
        assert d["avg_rating"] >= 9


def test_filter_by_price(client):
    r = client.get("/api/dishes", params={"max_price": 20000})
    assert r.status_code == 200
    for d in r.json():
        assert d["avg_price"] <= 20000


def test_filter_by_district(client):
    r = client.get("/api/dishes", params={"district": "Hoàn Kiếm"})
    assert r.status_code == 200
    # phải có ít nhất 1 món có quán ở quận Hoàn Kiếm
    assert len(r.json()) > 0


# ---------- random dish ----------

def test_random_all(client):
    r = client.get("/api/dishes/random")
    assert r.status_code == 200
    d = r.json()
    assert d["meal_type"] in MEALS
    assert d["name"]


def test_random_by_meal(client):
    for meal in MEALS:
        r = client.get("/api/dishes/random", params={"meal": meal})
        assert r.status_code == 200
        assert r.json()["meal_type"] == meal


def test_random_respects_available_data(client):
    """Random with a query for which data exists must always return a dish."""
    for _ in range(5):
        r = client.get("/api/dishes/random", params={"meal": "dinner"})
        assert r.status_code == 200


# ---------- Google Maps URL ----------

def test_google_maps_url_format(client):
    r = client.get("/api/dishes")
    assert r.status_code == 200
    dish = r.json()[0]
    rr = client.get(f"/api/dishes/{dish['id']}/restaurants")
    assert rr.status_code == 200
    restaurants = rr.json()
    assert len(restaurants) > 0
    for rest in restaurants:
        link = rest["maps_link"]
        assert link.startswith("https://www.google.com/maps/search/?api=1&query=")
        query = link.split("query=", 1)[1]
        assert "+" in query


def test_restaurants_have_source_and_demo_flag(client):
    r = client.get("/api/dishes")
    assert r.status_code == 200
    dish = r.json()[0]
    rr = client.get(f"/api/dishes/{dish['id']}/restaurants")
    for rest in rr.json():
        assert rest["maps_source"]
        assert rest["is_demo"] is True


# ---------- recipe ----------

def test_recipe_fields(client):
    r = client.get("/api/dishes")
    dish = r.json()[0]
    rr = client.get(f"/api/dishes/{dish['id']}/recipe")
    assert rr.status_code == 200
    rec = rr.json()
    assert isinstance(rec["ingredients"], list) and len(rec["ingredients"]) > 0
    assert isinstance(rec["steps"], list) and len(rec["steps"]) > 0
    assert rec["source"]


def test_recipe_404(client):
    r = client.get("/api/dishes/random")
    assert r.status_code == 200
    dish = r.json()
    rr = client.get(f"/api/dishes/{dish['id'] * 10000}/recipe")
    assert rr.status_code == 404


# ---------- dish detail ----------

def test_dish_detail_by_slug(client):
    r = client.get("/api/dishes")
    dish = r.json()[0]
    rd = client.get(f"/api/dishes/{dish['slug']}")
    assert rd.status_code == 200
    info = rd.json()
    assert info["slug"] == dish["slug"]
    assert "restaurants" in info
    assert "recipe" in info
    assert "reviews" in info
    assert info["is_demo"] is True


def test_dish_detail_404(client):
    r = client.get("/api/dishes/khong-ton-tai-mon")
    assert r.status_code == 404


# ---------- reviews ----------

def test_create_review_valid(client):
    r = client.get("/api/dishes")
    dish = r.json()[0]
    rr = client.post(
        f"/api/dishes/{dish['id']}/reviews",
        json={"rating": 10, "comment": "Món này rất ngon và đáng thử!", "reviewer_name": "Tester"},
    )
    assert rr.status_code == 201
    created = rr.json()
    assert created["rating"] == 10
    assert created["is_demo"] is False
    assert created["dish_id"] == dish["id"]

    # review mới phải xuất hiện trong danh sách
    lst = client.get(f"/api/dishes/{dish['id']}/reviews").json()
    ids = [rv["id"] for rv in lst]
    assert created["id"] in ids


def test_create_review_rating_too_high(client):
    r = client.get("/api/dishes")
    dish = r.json()[0]
    rr = client.post(
        f"/api/dishes/{dish['id']}/reviews",
        json={"rating": 11, "comment": "Điểm vượt quá 10"},
    )
    assert rr.status_code == 422


def test_create_review_rating_too_low(client):
    r = client.get("/api/dishes")
    dish = r.json()[0]
    rr = client.post(
        f"/api/dishes/{dish['id']}/reviews",
        json={"rating": 0, "comment": "Điểm dưới 1"},
    )
    assert rr.status_code == 422


def test_create_review_comment_too_short(client):
    r = client.get("/api/dishes")
    dish = r.json()[0]
    rr = client.post(
        f"/api/dishes/{dish['id']}/reviews",
        json={"rating": 8, "comment": "ok"},  # chỉ 2 ký tự < min 3
    )
    assert rr.status_code == 422


def test_create_review_missing_fields(client):
    r = client.get("/api/dishes")
    dish = r.json()[0]
    rr = client.post(f"/api/dishes/{dish['id']}/reviews", json={"comment": "Thiếu rating"})
    assert rr.status_code == 422


def test_create_review_unknown_dish(client):
    rr = client.post(
        "/api/dishes/999999/reviews",
        json={"rating": 8, "comment": "Món không tồn tại"},
    )
    assert rr.status_code == 404


def test_demo_reviews_flagged(client):
    r = client.get("/api/dishes")
    dish = next(d for d in r.json() if d["slug"] == "pho-bo-ha-noi")
    rr = client.get(f"/api/dishes/{dish['id']}/reviews").json()
    assert len(rr) > 0
    for rv in rr:
        assert rv["is_demo"] is True


# ---------- rarity ----------

def test_all_dishes_have_rarity(client):
    r = client.get("/api/dishes")
    assert r.status_code == 200
    for d in r.json():
        assert "rarity" in d
        assert d["rarity"]["key"] in {"cuc-pham", "dac-biet", "hiem", "quoc-dan", "toi-mat"}
        assert d["rarity"]["label"]
        assert 1 <= d["rarity"]["level"] <= 5


def test_rarity_matches_rating(client):
    r = client.get("/api/dishes")
    for d in r.json():
        rating = d["avg_rating"]
        key = d["rarity"]["key"]
        if rating >= 9.0:
            assert key == "cuc-pham"
        elif rating >= 8.5:
            assert key == "dac-biet"
        elif rating >= 8.0:
            assert key == "hiem"
        elif rating >= 7.0:
            assert key == "quoc-dan"
        else:
            assert key == "toi-mat"


def test_random_returns_rarity(client):
    r = client.get("/api/dishes/random")
    assert r.status_code == 200
    assert "rarity" in r.json()


# ---------- budget random ----------

def test_random_respects_max_price(client):
    for _ in range(5):
        r = client.get("/api/dishes/random", params={"max_price": 30000})
        assert r.status_code == 200
        assert r.json()["avg_price"] <= 30000


def test_random_respects_min_price(client):
    for _ in range(5):
        r = client.get("/api/dishes/random", params={"min_price": 45000})
        assert r.status_code == 200
        assert r.json()["avg_price"] >= 45000


def test_random_respects_budget_and_meal(client):
    for _ in range(5):
        r = client.get("/api/dishes/random", params={"meal": "breakfast", "min_price": 20000, "max_price": 40000})
        assert r.status_code == 200
        d = r.json()
        assert d["meal_type"] == "breakfast"
        assert 20000 <= d["avg_price"] <= 40000


def test_random_budget_no_match_404(client):
    r = client.get("/api/dishes/random", params={"max_price": 5})
    assert r.status_code == 404


# ---------- quẻ trưa (fortune) ----------

def test_fortune_returns_dish_and_message(client):
    r = client.get("/api/fortunes")
    assert r.status_code == 200
    data = r.json()
    assert "dish" in data and "fortune" in data
    assert data["dish"]["name"]
    assert len(data["fortune"]) > 0
    assert data["luck"] in {"may_mắn", "bình_thường", "đặc_biệt"}


def test_fortune_by_meal(client):
    r = client.get("/api/fortunes", params={"meal": "lunch"})
    assert r.status_code == 200
    assert r.json()["dish"]["meal_type"] == "lunch"