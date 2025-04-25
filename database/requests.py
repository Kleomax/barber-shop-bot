from sqlalchemy import select, update, delete

from .models import async_session
from .models import User, Barber, Service, Reserve
import asyncio

def connection(func):
    async def wrapper(*args, **kwargs):
        async with async_session() as session:
            return await func(session, *args, **kwargs)

    return wrapper


@connection
async def set_user(session, user_id: int):
    user = await session.scalar(select(User).where(User.user_id == user_id))

    if not user:
        session.add(User(user_id=user_id))
        await session.commit()
        return False
    else:
        return True

# @connection
# async def set_name(session, user_id: int, user_name: str):
#     session.add(User())


@connection
async def update_user(session, user_id: int, name: str, phone_number: str):
    await session.execute(update(User).where(User.user_id == user_id).values(name=name, phone_number=phone_number))
    await session.commit()


@connection
async def get_barbers(session):
    return await session.scalars(select(Barber))


@connection
async def get_barber_time(session, barber_id):
    return await session.scalars(select(Barber).where(Barber.barber_name == barber_id))


@connection
async def get_services(session):
    return await session.scalars(select(Service))

@connection
async def set_reserve(session, user_id, barber_name, service, barber_time):
    user = await session.scalar(select(User).where(User.user_id == user_id))
    session.add(Reserve(user=user.id, barber=barber_name, service=service, time=barber_time))
    await session.commit()

@connection
async def get_reserve(session):
    return await session.scalars(select(Reserve))
@connection
async def check_reserve(session, user_id):
    user = await session.scalar(select(User).where(User.user_id == user_id))
    return await session.scalars(select(Reserve).where(Reserve.user == user.id))

@connection
async def delete_reserve(session):
    await session.execute(delete(Reserve))
    await session.commit()

    