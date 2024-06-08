from __future__ import annotations
from litestar.contrib.sqlalchemy.dto import SQLAlchemyDTOConfig
from litestar.contrib.sqlalchemy.dto import SQLAlchemyDTO
from database import models


class DTO(SQLAlchemyDTO[models.Email]):
    config = SQLAlchemyDTOConfig(
        exclude={"code", "user"},
    )
