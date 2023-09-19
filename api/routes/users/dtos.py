from litestar.contrib.sqlalchemy.dto import SQLAlchemyDTO
from litestar.dto import DTOConfig
from database import models


class User(SQLAlchemyDTO[models.User]):
    config = DTOConfig()
