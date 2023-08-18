from sqlalchemy.ext.asyncio import async_sessionmaker
from .engine import engine

Session = async_sessionmaker(engine, expire_on_commit=False)
