"""SQLite database connection and table creation."""

from __future__ import annotations

import os
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


async def init_db() -> None:
    DATABASE_PATH.parent.mkdir(parents=True, exist_ok=True)
    db = await aiosqlite.connect(str(DATABASE_PATH))
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

        CREATE INDEX IF NOT EXISTS idx_dishes_meal ON dishes(meal_type);
        CREATE INDEX IF NOT EXISTS idx_restaurants_dish ON restaurants(dish_id);
        CREATE INDEX IF NOT EXISTS idx_reviews_dish ON reviews(dish_id);
        """
    )
    await db.commit()
    await db.close()