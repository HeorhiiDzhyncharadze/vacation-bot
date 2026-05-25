import pytest
import db


@pytest.fixture(autouse=True)
def use_tmp_db(monkeypatch, tmp_path):
    monkeypatch.setattr(db, "DB_PATH", str(tmp_path / "test.db"))


@pytest.mark.asyncio
async def test_init_db_creates_table():
    await db.init_db()
    # no exception = table created


@pytest.mark.asyncio
async def test_get_nonexistent_user_returns_none():
    await db.init_db()
    result = await db.get_user(999)
    assert result is None


@pytest.mark.asyncio
async def test_save_and_get_user():
    await db.init_db()
    await db.save_user(123, 168.0, 1, 10, 'uk')
    user = await db.get_user(123)
    assert user is not None
    assert user["total"] == 168.0
    assert user["start_m"] == 1
    assert user["end_m"] == 10
    assert user["lang"] == 'uk'


@pytest.mark.asyncio
async def test_save_user_replaces_existing():
    await db.init_db()
    await db.save_user(123, 168.0, 1, 10, 'uk')
    await db.save_user(123, 200.0, 2, 11, 'en')
    user = await db.get_user(123)
    assert user["total"] == 200.0
    assert user["lang"] == 'en'


@pytest.mark.asyncio
async def test_delete_user():
    await db.init_db()
    await db.save_user(123, 168.0, 1, 10, 'uk')
    await db.delete_user(123)
    user = await db.get_user(123)
    assert user is None


@pytest.mark.asyncio
async def test_delete_nonexistent_user_is_safe():
    await db.init_db()
    await db.delete_user(999)  # should not raise


@pytest.mark.asyncio
async def test_update_lang():
    await db.init_db()
    await db.save_user(123, 168.0, 1, 10, 'uk')
    await db.update_lang(123, 'hu')
    user = await db.get_user(123)
    assert user["lang"] == 'hu'


@pytest.mark.asyncio
async def test_multiple_users_isolated():
    await db.init_db()
    await db.save_user(1, 168.0, 1, 10, 'uk')
    await db.save_user(2, 240.0, 3, 12, 'en')
    u1 = await db.get_user(1)
    u2 = await db.get_user(2)
    assert u1["total"] == 168.0
    assert u2["total"] == 240.0
