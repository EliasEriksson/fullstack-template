from dataclasses import dataclass


@dataclass
class Claims:
    audience = "aud"
    issuer = "iss"
    subject = "sub"
    issued = "iat"
    expires = "exp"
