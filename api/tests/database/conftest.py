import pytest
from api.configuration import Configuration
from api.database import Database


@pytest.fixture
async def database():
    configuration = Configuration()
    print("USING MODE:", configuration.mode)
    print("USING CONNECTION URL:", configuration.database.url)
    database = Database(configuration)
    await database.create()
    yield database
    await database.delete()
