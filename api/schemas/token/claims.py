from dataclasses import dataclass


@dataclass
class Claims:
    audience = "aud"
    issuer = "iss"
    subject = "sub"
    session = "sid"
    secure = "sec"
    issued = "iat"
    expires = "exp"
