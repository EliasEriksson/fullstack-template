from dataclasses import dataclass


@dataclass
class Claims:
    audience = "aud"
    issuer = "iss"
    subject = "sub"
    session = "sid"
    issued = "iat"
    expires = "exp"
