from dataclasses import dataclass


@dataclass
class Claims:
    subject = "sub"
    expires = "exp"
    issued = "iss"
    audience = "aud"
