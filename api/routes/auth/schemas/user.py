from __future__ import annotations
from msgspec import Struct
from msgspec import field
from database import models
from database import Session
from litestar.exceptions import ClientException
from . import password


class Patchable(Struct):
    emails: list[str] | None = field(default=None)
    password: password.Patchable | None = field(default=None)

    async def patch(self, session: Session, user: models.User) -> models.User:
        if self.emails is not None:
            async with session.transaction():
                existing = {email.address for email in user.emails}
                for email in user.emails:
                    if email.address not in self.emails:
                        print("removing", email.address)
                        await session.emails.delete(email)

                for address in self.emails:
                    if address not in existing:
                        print("adding", address)
                        created = await session.emails.create(address, user=user, verification=await session.verifications.create())
                        print(f"email to {created.address}: verification: {created.verification.code}")
            # new = [
            #     await session.emails.create(
            #         address,
            #         user=user,
            #         verification=await session.verifications.create(),
            #     )
            #     for address in self.emails
            #     if address not in existing
            # ]
            # keep = (email for email in user.emails if email.address in self.emails)
            # user.emails = [*keep, *new]
            # for email in new:
            #     print(
            #         f"email to {email.address}: verification: {email.verification.code}"
            #     )
            # print([email.address for email in user.emails])
        if self.password is not None:
            if self.password.new != self.password.old:
                raise ClientException()
            if not user.verify(self.password.old):
                raise ClientException()
            user.hash = self.password.create_hash()
        return user
