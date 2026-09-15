"""SQLite database connection and table creation."""

from __future__ import annotations

from pathlib import Path

import aiosqlite
from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parent.parent / ".env")

DATABASE_PATH = Path(__file__).resolve().parent.parent / "data" / "hanoi_food.db"


async def get_db() -> aiosqlite.Connection:
    db = await aiosqlite.connect(str(DATABASE_PATH))
    db.row_factory = aiosqlite.Row
    await db.execute("PRAGMA journal_mode=WAL")
    await db.execute("PRAGMA foreign_keys=ON")
    return db


async def _ensure_columns(db: aiosqlite.Connection, table: str, columns: dict[str, str]) -> None:
    """Add missing columns to an existing table (idempotent migration)."""
    cur = await db.execute(f"PRAGMA table_info({table})")
    existing = {row["name"] for row in await cur.fetchall()}
    for name, ddl in columns.items():
        if name not in existing:
            await db.execute(f"ALTER TABLE {table} ADD COLUMN {name} {ddl}")


async def init_db() -> None:
    DATABASE_PATH.parent.mkdir(parents=True, exist_ok=True)
    db = await aiosqlite.connect(str(DATABASE_PATH))
    db.row_factory = aiosqlite.Row
    await db.executescript(
        """
        CREATE TABLE IF NOT EXISTS dishes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            slug TEXT NOT NULL UNIQUE,
            description TEXT NOT NULL,
            meal_type TEXT NOT NULL CHECK(meal_type IN ('breakfast','lunch','dinner','snack')),
            image_url TEXT NOT NULL DEFAULT '',
            image_source TEXT NOT NULL DEFAULT 'Demo - Chưa xác minh',
            avg_rating REAL NOT NULL DEFAULT 5.0,
            avg_price INTEGER NOT NULL DEFAULT 0,
            is_demo INTEGER NOT NULL DEFAULT 1,
            created_at TEXT NOT NULL DEFAULT (datetime('now'))
        );

        CREATE TABLE IF NOT EXISTS restaurants (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            dish_id INTEGER NOT NULL,
            name TEXT NOT NULL,
            address TEXT NOT NULL,
            district TEXT NOT NULL,
            hours TEXT NOT NULL DEFAULT '',
            price_range TEXT NOT NULL DEFAULT '',
            maps_link TEXT NOT NULL DEFAULT '',
            maps_source TEXT NOT NULL DEFAULT 'Demo - Chưa xác minh',
            is_demo INTEGER NOT NULL DEFAULT 1,
            FOREIGN KEY (dish_id) REFERENCES dishes(id) ON DELETE CASCADE
        );

        CREATE TABLE IF NOT EXISTS recipes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            dish_id INTEGER NOT NULL UNIQUE,
            ingredients TEXT NOT NULL DEFAULT '[]',
            portions TEXT NOT NULL DEFAULT '1-2 người',
            cook_time TEXT NOT NULL DEFAULT '',
            steps TEXT NOT NULL DEFAULT '[]',
            source TEXT NOT NULL DEFAULT 'Demo - Chưa xác minh',
            FOREIGN KEY (dish_id) REFERENCES dishes(id) ON DELETE CASCADE
        );

        CREATE TABLE IF NOT EXISTS reviews (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            dish_id INTEGER NOT NULL,
            rating INTEGER NOT NULL CHECK(rating BETWEEN 1 AND 10),
            comment TEXT NOT NULL DEFAULT '',
            reviewer_name TEXT NOT NULL DEFAULT 'Ẩn danh',
            is_demo INTEGER NOT NULL DEFAULT 1,
            created_at TEXT NOT NULL DEFAULT (datetime('now')),
            FOREIGN KEY (dish_id) REFERENCES dishes(id) ON DELETE CASCADE
        );

        CREATE TABLE IF NOT EXISTS zodiac_profiles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            birth_day INTEGER NOT NULL,
            birth_month INTEGER NOT NULL,
            birth_year INTEGER,
            consent_save BOOLEAN NOT NULL DEFAULT 0,
            created_at TEXT NOT NULL DEFAULT (datetime('now'))
        );

        CREATE TABLE IF NOT EXISTS group_rooms (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            room_code TEXT NOT NULL UNIQUE,
            host_name TEXT NOT NULL,
            config TEXT NOT NULL DEFAULT '{}',
            ends_at TEXT,
            status TEXT NOT NULL DEFAULT 'open' CHECK(status IN ('open','finished')),
            created_at TEXT NOT NULL DEFAULT (datetime('now'))
        );

        CREATE TABLE IF NOT EXISTS group_votes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            room_id INTEGER NOT NULL,
            dish_id INTEGER NOT NULL,
            voter_name TEXT NOT NULL,
            created_at TEXT NOT NULL DEFAULT (datetime('now')),
            FOREIGN KEY (room_id) REFERENCES group_rooms(id) ON DELETE CASCADE,
            FOREIGN KEY (dish_id) REFERENCES dishes(id) ON DELETE CASCADE,
            UNIQUE (room_id, voter_name)
        );

        CREATE TABLE IF NOT EXISTS user_views (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id TEXT NOT NULL,
            dish_id INTEGER NOT NULL,
            viewed_at TEXT NOT NULL DEFAULT (datetime('now')),
            FOREIGN KEY (dish_id) REFERENCES dishes(id) ON DELETE CASCADE,
            UNIQUE (session_id, dish_id)
        );

        CREATE TABLE IF NOT EXISTS user_reviews (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id TEXT NOT NULL,
            dish_id INTEGER NOT NULL,
            created_at TEXT NOT NULL DEFAULT (datetime('now')),
            FOREIGN KEY (dish_id) REFERENCES dishes(id) ON DELETE CASCADE,
            UNIQUE (session_id, dish_id)
        );

        CREATE TABLE IF NOT EXISTS theme_selections (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id TEXT NOT NULL UNIQUE,
            theme_id TEXT NOT NULL DEFAULT 'ha-noi-co-dien',
            updated_at TEXT NOT NULL DEFAULT (datetime('now'))
        );

        CREATE TABLE IF NOT EXISTS fate_rolls (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id TEXT NOT NULL,
            dish_id INTEGER NOT NULL,
            rolled_at TEXT NOT NULL DEFAULT (datetime('now')),
            FOREIGN KEY (dish_id) REFERENCES dishes(id) ON DELETE CASCADE
        );

        CREATE TABLE IF NOT EXISTS user_mascots (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id TEXT NOT NULL UNIQUE,
            mascot_id TEXT NOT NULL,
            birthday_day INTEGER,
            birthday_month INTEGER,
            consent_save INTEGER NOT NULL DEFAULT 0,
            created_at TEXT NOT NULL DEFAULT (datetime('now')),
            updated_at TEXT NOT NULL DEFAULT (datetime('now'))
        );
        """
    )

    # ---- Migrations for DBs created before the metadata columns existed ----
    await _ensure_columns(db, "dishes", {
        "healthy_score": "INTEGER DEFAULT NULL",
        "oil_level": "TEXT NOT NULL DEFAULT 'unknown'",
        "spicy_level": "TEXT NOT NULL DEFAULT 'none'",
        "vegetarian": "INTEGER NOT NULL DEFAULT 0",
        "protein_level": "TEXT NOT NULL DEFAULT 'unknown'",
        "calories_estimate": "INTEGER",
        "calories_source": "TEXT NOT NULL DEFAULT ''",
        "dominant_color": "TEXT NOT NULL DEFAULT ''",
        "color_tags": "TEXT NOT NULL DEFAULT '[]'",
        "color_source": "TEXT NOT NULL DEFAULT ''",
        "verification_status": "TEXT NOT NULL DEFAULT 'demo'",
        "cuisine": "TEXT NOT NULL DEFAULT 'Việt Nam'",
        "key_ingredients": "TEXT NOT NULL DEFAULT '[]'",
        "dish_origin": "TEXT NOT NULL DEFAULT 'Hà Nội'",
    })
    await _ensure_columns(db, "restaurants", {
        "occasion_tags": "TEXT NOT NULL DEFAULT '[]'",
        "tags_verification": "TEXT NOT NULL DEFAULT 'demo'",
    })

    await db.execute(
        "UPDATE dishes SET verification_status='demo', color_source='Chưa xác minh - tạm gán theo món' "
        "WHERE verification_status IS NULL OR verification_status=''"
    )

    # Indexes live AFTER column migration so they exist on fresh databases too.
    await db.executescript(
        """
        CREATE INDEX IF NOT EXISTS idx_dishes_meal ON dishes(meal_type);
        CREATE INDEX IF NOT EXISTS idx_dishes_healthy ON dishes(healthy_score);
        CREATE INDEX IF NOT EXISTS idx_restaurants_dish ON restaurants(dish_id);
        CREATE INDEX IF NOT EXISTS idx_reviews_dish ON reviews(dish_id);
        CREATE INDEX IF NOT EXISTS idx_group_votes_room ON group_votes(room_id);
        CREATE INDEX IF NOT EXISTS idx_user_views_session ON user_views(session_id);
        CREATE INDEX IF NOT EXISTS idx_user_views_dish ON user_views(dish_id);
        """
    )
    await db.commit()
    await db.close()
