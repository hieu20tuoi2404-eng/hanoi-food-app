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
        assert d["rarity"]["key"] in {"common", "rare", "epic", "legendary"}
        assert d["rarity"]["label"]
        assert 1 <= d["rarity"]["level"] <= 4


def test_rarity_matches_rating(client):
    r = client.get("/api/dishes")
    for d in r.json():
        rating = d["avg_rating"]
        key = d["rarity"]["key"]
        if rating >= 9.5:
            assert key == "legendary"
        elif rating >= 8.5:
            assert key == "epic"
        elif rating >= 7.5:
            assert key == "rare"
        else:
            assert key == "common"


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


# ============================================================
# 2.0: metadata (cuisine, ingredients, verification)
# ============================================================

def test_dishes_have_cuisine_and_ingredients(client):
    r = client.get("/api/dishes")
    assert r.status_code == 200
    for d in r.json():
        assert d["cuisine"]
        assert isinstance(d["key_ingredients"], list) and len(d["key_ingredients"]) > 0
        assert d["dish_origin"]
        assert d["verification_status"]
        # calories must NOT be fabricated -> NULL shows as None
        assert d["calories_estimate"] is None
        assert d["calories_source"] == ""


def test_dish_detail_has_metadata(client):
    r = client.get("/api/dishes")
    dish = next(d for d in r.json() if d["slug"] == "pho-bo-ha-noi")
    rr = client.get(f"/api/dishes/{dish['slug']}")
    info = rr.json()
    assert info["cuisine"]
    assert info["key_ingredients"]
    assert all(rest["tags_verification"] for rest in info["restaurants"])


# ============================================================
# 2.0: preferences / advanced random
# ============================================================

def test_preferences_endpoint(client):
    r = client.get("/api/preferences")
    assert r.status_code == 200
    data = r.json()
    assert data["healthy_options"] and data["occasion_options"]
    assert data["color_options"] and data["meal_types"]


def test_advanced_random_healthy(client):
    r = client.post("/api/dishes/random/advanced", json={"diet": "vegetarian"})
    assert r.status_code == 200
    d = r.json()["dish"]
    assert d["vegetarian"] is True


def test_advanced_random_spicy(client):
    r = client.post("/api/dishes/random/advanced", json={"occasion": "drinking"})
    assert r.status_code in (200, 404)


def test_advanced_random_no_match(client):
    r = client.post("/api/dishes/random/advanced", json={"max_price": 5})
    assert r.status_code == 404


def test_by_color(client):
    r = client.get("/api/dishes/by-color", params={"color": "yellow"})
    assert r.status_code == 200
    for d in r.json():
        assert d["dominant_color"] == "yellow" or "yellow" in d["color_tags"]


# ============================================================
# 2.0: eating-style / mood filters on the list endpoint
# ============================================================

def test_list_filter_healthy(client):
    r = client.get("/api/dishes", params={"diet": "healthy"})
    assert r.status_code == 200
    dishes = r.json()
    assert dishes
    for d in dishes:
        assert d["healthy_score"] is not None and d["healthy_score"] >= 6


def test_list_filter_light_oil(client):
    r = client.get("/api/dishes", params={"diet": "light_oil"})
    assert r.status_code == 200
    dishes = r.json()
    assert dishes
    for d in dishes:
        assert d["oil_level"] in {"low", "medium"}


def test_list_filter_rich_oil(client):
    r = client.get("/api/dishes", params={"diet": "rich_oil"})
    assert r.status_code == 200
    dishes = r.json()
    assert dishes
    for d in dishes:
        assert d["oil_level"] == "high"


def test_list_filter_vegetarian(client):
    r = client.get("/api/dishes", params={"diet": "vegetarian"})
    assert r.status_code == 200
    dishes = r.json()
    assert dishes
    for d in dishes:
        assert d["vegetarian"] is True


def test_list_filter_color(client):
    r = client.get("/api/dishes", params={"color": "yellow"})
    assert r.status_code == 200
    dishes = r.json()
    assert dishes
    for d in dishes:
        assert d["dominant_color"] == "yellow" or "yellow" in d["color_tags"]


def test_list_filter_occasion_date(client):
    r = client.get("/api/dishes", params={"occasion": "date"})
    assert r.status_code == 200
    dishes = r.json()
    assert dishes
    for d in dishes:
        detail = client.get(f"/api/dishes/{d['slug']}").json()
        tags = [t for rs in detail["restaurants"] for t in rs["occasion_tags"]]
        assert "date" in tags


def test_list_filter_occasion_solo(client):
    r = client.get("/api/dishes", params={"occasion": "solo"})
    assert r.status_code == 200
    dishes = r.json()
    assert dishes
    for d in dishes:
        detail = client.get(f"/api/dishes/{d['slug']}").json()
        tags = [t for rs in detail["restaurants"] for t in rs["occasion_tags"]]
        assert "solo" in tags


def test_list_filter_occasion_drinking(client):
    r = client.get("/api/dishes", params={"occasion": "drinking"})
    assert r.status_code == 200
    dishes = r.json()
    assert dishes
    for d in dishes:
        detail = client.get(f"/api/dishes/{d['slug']}").json()
        tags = [t for rs in detail["restaurants"] for t in rs["occasion_tags"]]
        assert "drinking" in tags


def test_list_filter_meal_plus_diet(client):
    r = client.get("/api/dishes", params={"meal": "breakfast", "diet": "healthy"})
    assert r.status_code == 200
    dishes = r.json()
    assert dishes
    for d in dishes:
        assert d["meal_type"] == "breakfast"
        assert d["healthy_score"] >= 6


# ============================================================
# 2.0: zodiac (entertainment only, privacy)
# ============================================================

def test_zodiac_profile_creates(client):
    r = client.post("/api/zodiac/profile", json={"day": 5, "month": 4, "consent_save": False})
    assert r.status_code == 201
    p = r.json()
    assert p["sign_key"] == "aries"
    assert p["year"] is None  # no year unless consent
    assert "Giải trí" in p["entertainment_note"] or "Gợi ý vui" in p["entertainment_note"]


def test_zodiac_profile_saves_year_with_consent(client):
    r = client.post("/api/zodiac/profile", json={"day": 1, "month": 1, "year": 1995, "consent_save": True})
    assert r.status_code == 201
    assert r.json()["year"] == 1995


def test_zodiac_recommendation(client):
    r = client.get("/api/zodiac/recommendation", params={"day": 25, "month": 8})
    assert r.status_code == 200
    data = r.json()
    assert data["sign"]["name"] == "Xử Nữ"
    assert data["flavour"]
    assert "Gợi ý vui" in data["entertainment_note"]


def test_zodiac_delete(client):
    r = client.post("/api/zodiac/profile", json={"day": 10, "month": 10})
    pid = r.json()["id"]
    rr = client.delete(f"/api/zodiac/profile/{pid}")
    assert rr.status_code == 200
    assert rr.json()["deleted"] is True


def test_zodiac_invalid_date(client):
    r = client.post("/api/zodiac/profile", json={"day": 30, "month": 2})
    assert r.status_code == 422


# ============================================================
# 2.0: fate rolls (max 3/session)
# ============================================================

def test_fate_roll_basic(client):
    r = client.post("/api/fate/roll", json={}, headers={"X-Session-Id": "tester-1"})
    assert r.status_code == 200
    data = r.json()
    assert data["dish"]["name"]
    assert 1 <= data["roll"] <= 6


def test_fate_roll_limit_3(client):
    headers = {"X-Session-Id": "tester-fate-limit"}
    for i in range(3):
        r = client.post("/api/fate/roll", json={}, headers=headers)
        assert r.status_code == 200
        assert r.json()["limit_reached"] is False
    r4 = client.post("/api/fate/roll", json={}, headers=headers)
    assert r4.status_code == 200
    assert r4.json()["limit_reached"] is True


def test_fate_roll_linh_vat_on_6(client):
    # statistical but run enough; at least one 6 should appear among messages
    for _ in range(40):
        r = client.post("/api/fate/roll", json={}, headers={"X-Session-Id": "tester-fate-6"})
        if r.json()["roll"] == 6:
            assert r.json()["linh_vat"] is not None
            return
    # no assert failure needed, probabilistic


# ============================================================
# 2.0: group voting
# ============================================================

def test_group_room_flow(client):
    dishes = client.get("/api/dishes").json()
    d1, d2 = dishes[0], dishes[1]
    r = client.post("/api/group-rooms", json={"host_name": "Host", "config": {}})
    assert r.status_code == 201
    code = r.json()["room_code"]
    assert len(code) == 6

    # vote
    v1 = client.post(f"/api/group-rooms/{code}/votes", json={"voter_name": "An", "dish_id": d1["id"]})
    assert v1.status_code == 200
    # second vote by same name -> duplicate
    v2 = client.post(f"/api/group-rooms/{code}/votes", json={"voter_name": "An", "dish_id": d2["id"]})
    assert v2.status_code == 409
    # different voter
    v3 = client.post(f"/api/group-rooms/{code}/votes", json={"voter_name": "Binh", "dish_id": d1["id"]})
    assert v3.status_code == 200

    payload = client.get(f"/api/group-rooms/{code}").json()
    assert payload["vote_tally"]["total_votes"] == 2
    assert payload["vote_tally"]["winner"]["id"] == d1["id"]

    fin = client.post(f"/api/group-rooms/{code}/finish")
    assert fin.status_code == 200
    assert fin.json()["status"] == "finished"
    assert fin.json()["winner"]["id"] == d1["id"]


def test_group_room_not_found(client):
    r = client.get("/api/group-rooms/NOPE99")
    assert r.status_code == 404


# ============================================================
# 2.0: themes
# ============================================================

def test_themes_list(client):
    r = client.get("/api/themes")
    assert r.status_code == 200
    themes = r.json()
    # 5 original + 12 zodiac = 17 total
    assert len(themes) == 17
    ids = {t["id"] for t in themes}
    assert "ha-noi-co-dien" in ids
    assert "hoi-meo" not in ids
    # All 12 zodiac themes present
    for zid in ["rat", "ox", "tiger", "rabbit", "dragon", "snake",
                "horse", "goat", "monkey", "rooster", "dog", "pig"]:
        assert zid in ids


def test_theme_get_by_id(client):
    r = client.get("/api/themes/dragon")
    assert r.status_code == 200
    data = r.json()
    assert data["id"] == "dragon"
    assert data["name"] == "Nhà Rồng"
    assert "mascot_id" in data


def test_theme_get_by_id_not_found(client):
    r = client.get("/api/themes/nope")
    assert r.status_code == 404


def test_theme_select_persist(client):
    r = client.post("/api/themes/select", json={"theme_id": "pho-dem"}, headers={"X-Session-Id": "theme-user"})
    assert r.status_code == 200
    sel = client.get("/api/themes/selection", headers={"X-Session-Id": "theme-user"})
    assert sel.json()["theme_id"] == "pho-dem"


def test_theme_select_bad(client):
    r = client.post("/api/themes/select", json={"theme_id": "nope"}, headers={"X-Session-Id": "theme-user-2"})
    assert r.status_code == 404


# ============================================================
# 3.0: mascots
# ============================================================

def test_mascots_list(client):
    r = client.get("/api/mascots")
    assert r.status_code == 200
    mascots = r.json()
    assert len(mascots) == 12
    ids = {m["id"] for m in mascots}
    for mid in ["ty", "suu", "dan", "mao", "thin", "ty-snake",
                "ngo", "mui", "than", "dau", "tuat", "hoi"]:
        assert mid in ids


def test_mascot_get_by_id(client):
    r = client.get("/api/mascots/thin")
    assert r.status_code == 200
    data = r.json()
    assert data["animal"] == "Rồng"
    assert data["id"] == "thin"


def test_mascot_get_by_id_not_found(client):
    r = client.get("/api/mascots/nope")
    assert r.status_code == 404


def test_user_mascot_set_and_get(client):
    sid = "mascot-test-user"
    r = client.post("/api/user/mascot", json={"mascot_id": "thin"}, headers={"X-Session-Id": sid})
    assert r.status_code == 200
    assert r.json()["mascot_id"] == "thin"
    g = client.get("/api/user/mascot", headers={"X-Session-Id": sid})
    assert g.json()["mascot_id"] == "thin"


def test_user_mascot_update(client):
    sid = "mascot-test-update"
    client.post("/api/user/mascot", json={"mascot_id": "ty"}, headers={"X-Session-Id": sid})
    r = client.post("/api/user/mascot", json={"mascot_id": "hoi"}, headers={"X-Session-Id": sid})
    assert r.status_code == 200
    assert r.json()["mascot_id"] == "hoi"


def test_user_mascot_delete(client):
    sid = "mascot-test-delete"
    client.post("/api/user/mascot", json={"mascot_id": "dan"}, headers={"X-Session-Id": sid})
    r = client.delete("/api/user/mascot", headers={"X-Session-Id": sid})
    assert r.status_code == 200
    assert r.json()["deleted"] is True
    g = client.get("/api/user/mascot", headers={"X-Session-Id": sid})
    assert g.json()["mascot_id"] is None


def test_user_mascot_invalid_id(client):
    r = client.post("/api/user/mascot", json={"mascot_id": "nope"}, headers={"X-Session-Id": "mascot-bad"})
    assert r.status_code == 404


def test_user_mascot_clear_by_posting_null(client):
    sid = "mascot-test-clear"
    client.post("/api/user/mascot", json={"mascot_id": "dan"}, headers={"X-Session-Id": sid})
    r = client.post("/api/user/mascot", json={"mascot_id": None}, headers={"X-Session-Id": sid})
    assert r.status_code == 200
    g = client.get("/api/user/mascot", headers={"X-Session-Id": sid})
    assert g.json()["mascot_id"] is None


# ============================================================
# 2.0: exploration profile
# ============================================================

def test_exploration_tracks_views(client):
    headers = {"X-Session-Id": "explorer-1"}
    dishes = client.get("/api/dishes").json()
    for d in dishes[:3]:
        client.get(f"/api/dishes/{d['slug']}", headers=headers)
    r = client.get("/api/exploration", headers=headers)
    assert r.status_code == 200
    data = r.json()
    assert data["viewed_count"] >= 3
    assert data["level"]["name"]
    assert isinstance(data["achievements"], list)
    keys = {a["key"] for a in data["achievements"]}
    assert "first_bite" in keys


def test_exploration_no_session_still_works(client):
    r = client.get("/api/exploration")
    assert r.status_code == 200
    assert "session_id" in r.json()


def test_rare_finder_requires_real_view(client):
    headers = {"X-Session-Id": "req-rare-finder"}
    # Fresh session: no free XP, rarity achievements locked
    prof = client.get("/api/exploration", headers=headers).json()
    assert prof["xp"] == 0
    keys = {a["key"] for a in prof["achievements"]}
    assert "rare_finder" not in keys
    assert "legendary_finder" not in keys

    # View one dish -> sampler unlocks only if it passes the tier threshold
    dishes = client.get("/api/dishes").json()
    first = dishes[0]
    client.get(f"/api/dishes/{first['slug']}", headers=headers)
    prof = client.get("/api/exploration", headers=headers).json()
    keys = {a["key"] for a in prof["achievements"]}
    if first["rarity"]["key"] in {"rare", "epic", "legendary"}:
        assert "rare_finder" in keys
    else:
        assert "rare_finder" not in keys


def test_collection_endpoint(client):
    r = client.get("/api/collection", headers={"X-Session-Id": "collector-1"})
    assert r.status_code == 200
    data = r.json()
    assert data["total"] == 30
    assert "cards" in data
    assert all(c["rarity"]["key"] for c in data["cards"])


# ============================================================
# 2.0: review attribution to session (achievement "first review")
# ============================================================

def test_review_with_session_counts(client):
    headers = {"X-Session-Id": "reviewer-ach"}
    dishes = client.get("/api/dishes").json()
    r = client.post(
        f"/api/dishes/{dishes[0]['id']}/reviews",
        json={"rating": 9, "comment": "Rất ngon", "reviewer_name": "AchUser"},
        headers=headers,
    )
    assert r.status_code == 201
    prof = client.get("/api/exploration", headers=headers).json()
    keys = {a["key"] for a in prof["achievements"]}
    assert "first_review" in keys