from sqlalchemy import String, Column, Integer
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class PremiumUsers(Base):
    __tablename__ = 'user_is_premium'
    uid = Column(Integer, primary_key=True)
    is_premium = Column(Integer, default=0)


engine = create_async_engine('sqlite+aiosqlite:///premium.db', echo=False)
Session = async_sessionmaker(engine)


async def setup_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
