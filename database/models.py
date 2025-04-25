from sqlalchemy import String, ForeignKey, Integer, BigInteger
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine, AsyncSession

engine = create_async_engine(url='postgresql+asyncpg://postgres:admin@localhost:5432/barber_shop', echo=True)
async_session = async_sessionmaker(engine, class_=AsyncSession)


class Base(AsyncAttrs, DeclarativeBase):
    pass

class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id = mapped_column(BigInteger)
    name: Mapped[str] = mapped_column(String(20), nullable=True)
    phone_number: Mapped[str] = mapped_column(String(25), nullable=True)

class Barber(Base):
    __tablename__ = 'barbers'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    barber_name: Mapped[str] = mapped_column(String(25))
    barber_time: Mapped[str] = mapped_column()

class Service(Base):
    __tablename__ = 'services'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(15))
    description: Mapped[str] = mapped_column(String(128))
    price: Mapped[int]

class Reserve(Base):
    __tablename__ = 'reservations'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user: Mapped[int] = mapped_column(ForeignKey('users.id'))
    barber: Mapped[str] = mapped_column(ForeignKey('barbers.barber_name'))
    service: Mapped[str] = mapped_column(ForeignKey('services.name'))
    time: Mapped[str] = mapped_column(ForeignKey('barbers.barber_time'))

async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
