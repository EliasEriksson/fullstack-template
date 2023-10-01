from litestar.contrib.sqlalchemy.dto import SQLAlchemyDTO
from litestar.dto import DTOConfig
from database import models


class User(SQLAlchemyDTO[models.User]):
    config = DTOConfig()


class CreateUser(SQLAlchemyDTO[models.User]):
    config = DTOConfig(
        exclude={"id", "created", "modified"},
    )


class PatchUser(SQLAlchemyDTO[models.User]):
    config = DTOConfig(
        exclude={"id", "created", "modified"},
        partial=True,
    )
