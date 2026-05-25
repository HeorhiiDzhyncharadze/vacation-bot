import os
import aiosqlite

DB_PATH = os.environ.get("DB_PATH", "users.db")

_CREATE_TABLE = """
CREATE TABLE IF NOT EXISTS users (
    user_id  INTEGER PRIMARY KEY,
    total    REAL    NOT NULL,
    start_m  INTEGER NOT NULL DEFAULT 1,
    end_m    INTEGER NOT NULL,
    lang     TEXT    NOT NULL DEFAULT 'uk'
)
"""


async def init_db():
    async with aiosqlite.connect(DB_PATH) as conn:
        await conn.execute(_CREATE_TABLE)
        await conn.commit()


async def get_user(user_id: int) -> dict | None:
    async with aiosqlite.connect(DB_PATH) as conn:
        conn.row_factory = aiosqlite.Row
        async with conn.execute(
            "SELECT * FROM users WHERE user_id = ?", (user_id,)
        ) as cursor:
            row = await cursor.fetchone()
            return dict(row) if row else None


async def save_user(user_id: int, total: float, start_m: int, end_m: int, lang: str):
    async with aiosqlite.connect(DB_PATH) as conn:
        await conn.execute(
            "INSERT OR REPLACE INTO users (user_id, total, start_m, end_m, lang) "
            "VALUES (?, ?, ?, ?, ?)",
            (user_id, total, start_m, end_m, lang),
        )
        await conn.commit()


async def delete_user(user_id: int):
    async with aiosqlite.connect(DB_PATH) as conn:
        await conn.execute("DELETE FROM users WHERE user_id = ?", (user_id,))
        await conn.commit()


async def update_lang(user_id: int, lang: str):
    async with aiosqlite.connect(DB_PATH) as conn:
        await conn.execute(
            "UPDATE users SET lang = ? WHERE user_id = ?", (lang, user_id)
        )
        await conn.commit()
