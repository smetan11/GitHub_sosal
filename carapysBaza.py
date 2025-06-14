from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy import select

SQLALCHEMY_DATABASE_URL = "sqlite+aiosqlite:///./bot_database.db"

engine = create_async_engine(SQLALCHEMY_DATABASE_URL, future=True, echo=True)
async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'
    tg_id = Column(String, primary_key=True)
    username = Column(String)
    lite_count = Column(Integer, default=0)
    medium_count = Column(Integer, default=0)
    hard_count = Column(Integer, default=0)


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def add_user(tg_id, username):
    async with async_session() as db:
        db.add(User(tg_id=tg_id, username=username))
        await db.commit()


async def get_user(tg_id):
    async with async_session() as db:
        result = await db.execute(select(User).where(User.tg_id == tg_id))
        return result.scalars().first()


async def update_score(tg_id, score, mode):
    async with async_session() as db:
        user = await get_user(tg_id)
        if user:
            if mode == "lite":
                user.lite_count += score
            elif mode == "medium":
                user.medium_count += score
            elif mode == "hard":
                user.hard_count += score

            db.add(user)
            await db.commit()
