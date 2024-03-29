from api.schemas.token import Token, Algorithms, Claims
from datetime import datetime
from datetime import timedelta
from uuid import uuid4
import re

jwt_pattern = re.compile(r"^ey[^.]+\.[^.]+\.[^.]+$")


# async def test_constants() -> None:
#     assert Algorithms.RS512 == "RS512"
#     assert Claims.audience == "aud"
#     assert Claims.subject == "sub"
#     assert Claims.expires == "exp"
#     assert Claims.issued == "iat"
#     assert Claims.issuer == "iss"


# async def test_encode_decode(token: Token, audience: str) -> None:
#     jwt = token.encode()
#     assert isinstance(jwt, str)
#     assert jwt_pattern.match(jwt)
#     result = Token.decode(jwt, audience)
#     assert result == token
