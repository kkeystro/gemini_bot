import time
from premium.models import PremiumUsers, Session
from sqlalchemy import func, select


async def add_user(uid):
    async with Session() as session:
        async with session.begin():
            new_key = PremiumUsers(uid=uid)
            session.add(new_key)


async def set_premium(uid):
    async with Session() as session:
        async with session.begin():
            result = await session.execute(select(PremiumUsers).filter_by(uid=uid))
            user = result.scalars().first()
            if user.is_premium == 0:
                user.is_premium = 1


async def check_premium(uid):
    async with Session() as session:
        async with session.begin():
            result = await session.execute(select(PremiumUsers).filter_by(uid=uid))
            user = result.scalars().first()
            if user.is_premium == 0:
                return False
    return True
