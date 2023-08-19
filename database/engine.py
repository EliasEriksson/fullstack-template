from sqlalchemy.ext.asyncio import create_async_engine
from .configuration import Configuration

engine = create_async_engine("sqlite+aiosqlite:///database.sqlite", echo=True)
