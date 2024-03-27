# import os
#
# import pytest
# from database import models
# from sqlalchemy import select
# from database.configuration_old import DatabaseConfiguration
# from database.configuration_old import Variables
# from database import Database
# from shared import hash
#
#
# @pytest.fixture
# async def database():
#     print("setting up database configuration for tests", os.environ.get(Variables.mode))
#     configuration = DatabaseConfiguration()
#     database = Database(configuration)
#     await database.create()
#     yield database
#     await database.delete()
#
#
# async def test_user(database: Database) -> None:
#     async with database._session_maker() as session:
#         users = await session.execute(select(models.User))
#         assert len(users.scalars().all()) == 0
#         await session.commit()
#
#         async with session.begin():
#             users = [
#                 models.User(email="jessie@rocket.com", hash=hash.password("asd123")),
#                 models.User(email="james@rocket.com", hash=hash.password("asd123")),
#                 models.User(email="giovani@rocket.com", hash=hash.password("asd123")),
#             ]
#             session.add_all(users)
#
#         users = await session.execute(select(models.User))
#         assert len(users.scalars().all()) == 4
#         await session.commit()
