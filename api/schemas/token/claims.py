from dataclasses import dataclass


@dataclass
class Claims:
    audience = "aud"
    issuer = "iss"
    subject = "sub"
    session = "sid"
    email = "eml"
    secure = "sec"
    issued = "iat"
    expires = "exp"
