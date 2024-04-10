from sqlalchemy import String, Column, Integer
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class APIKeyUsage(Base):
    __tablename__ = 'api_key_usage'
    key = Column(String, primary_key=True)
    usage_count_24h = Column(Integer, default=0)
    last_usage_time = Column(Integer)


engine = create_async_engine('sqlite+aiosqlite:///api_keys.db', echo=True)
Session = async_sessionmaker(bind=engine)


async def setup_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all(engine))
