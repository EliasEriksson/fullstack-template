from litestar.contrib.sqlalchemy.dto import SQLAlchemyDTO
from litestar.dto import DTOConfig
from database import models


class User(SQLAlchemyDTO[models.User]):
    config = DTOConfig(
        max_nested_depth=2,
    )


class PatchUser(SQLAlchemyDTO[models.User]):
    config = DTOConfig(
        exclude={"id", "created", "modified"},
        max_nested_depth=2,
        partial=True,
    )
