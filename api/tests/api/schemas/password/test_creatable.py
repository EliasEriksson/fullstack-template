from api import schemas
import msgspec
import json


async def test_creatable() -> None:
    msgspec.json.decode(
        json.dumps({"password": "asd123", "repeat": "asd123"}).encode("utf-8"),
        type=schemas.password.Creatable,
    )
    try:
        msgspec.json.decode(
            json.dumps({"password": "asd123", "repeat": "asd1234"}).encode("utf-8"),
            type=schemas.password.Creatable,
        )
    except msgspec.ValidationError:
        pass
    else:
        raise Exception("Validation should fail.")
