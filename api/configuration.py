from __future__ import annotations
from typing import *
from shared.configuration import Configuration
from shared.configuration import ConfigurationMissingVariable
from shared.iterable import Iterable
from functools import cached_property
import re


class Variables(Iterable):
    jwt_private_key = "JWT_PRIVATE_KEY"
    jwt_public_key = "JWT_PUBLIC_KEY"
    password_pepper = "PASSWORD_PEPPER"


class ApiConfiguration(Configuration):
    _variables = Variables()
    _secure: bool
    _privateKeyPattern = re.compile(
        r"^-----BEGIN PRIVATE KEY-----.*?-----END PRIVATE KEY-----$"
    )
    _publicKeyPattern = re.compile(
        r"^-----BEGIN PUBLIC KEY-----.*?-----END PUBLIC KEY-----$"
    )
    _whitespacePattern = re.compile(r"\s")

    def __init__(
        self,
        environment: dict[str, Any] | None = None,
        secure: bool = True,
    ) -> None:
        super().__init__(environment)
        self._secure = secure
        self._write()

    @cached_property
    def jwt_private_key(self) -> str:
        try:
            result = self._string(self._variables.jwt_private_key)
            if self._privateKeyPattern.match(result):
                return result
            return (
                f"-----BEGIN PRIVATE KEY-----\n"
                + self._whitespacePattern.sub("\n", result)
                + f"\n-----END PRIVATE KEY-----"
            )
        except ConfigurationMissingVariable as error:
            if self._secure:
                raise error
            return (
                "-----BEGIN PRIVATE KEY-----\n"
                "MIIJegIBADANBgkqhkiG9w0BAQEFAASCCWQwgglgAgEAAoICDQslKgxCIJu9Ft72\n"
                "SMQ1lsa82c4lSV1M4vRDXCvGVNC1/XZw6DiHC0hyLTA0F64P3X52YsFAah2Jsu71\n"
                "jlaJ5mjTXv8e2bI8/aitkgoohFYcBlQg5FIvBpZqfM+QpD7prFYxNU9mfIQ2loAf\n"
                "05j/g0TNQcxFPwSbnHz+0EvYRV4+Ixu4qpKt3aOlWU88F9YZlPxMU/z+hFuE47Ei\n"
                "TOx65HAlPJFA7tQ0JYcDkIxyQB4a0J+UGpUkRq2bu3tDRd/3txUs9Wy0bitUBBMF\n"
                "wFg+XI8bsJ9sEX8cqehfV6N73PZWiJ59qp2SxIp04DlWjoyUOGawWPhfBp0PLuJc\n"
                "gB+rTACOZ1Yy5c8hZALMk8QzSuQ9R53Ok+/tDfeA3FdQbOlUspf6t5+lKewC55yj\n"
                "GB8vbrVDMSfxd8xAiAuH3qqhu7g72ozEOJ5ZXMp1HusqbCMn/Sm0/fXA/BWQclmk\n"
                "OoeK8T4vkzG4wzRWTmeILIoOxtqPnMbAo0A+PbV1TJpmJrlrp/YHBIQ2eMmdPCUH\n"
                "otlZRV0RMYU6iJNmqRHXxYmzkxQsEpM3G+BXHAE+wi2XZOUloDJ7c3s35QV7w4mD\n"
                "XKKjewaXx/KS5LgAyyU6NkRzjQauam1oyAt598NNrV3U0cO3rW7YOiRT0jHI0Gu7\n"
                "SvvoDMOOle6l44EZaXV3qtKnNTWsqy6GV3nmfk4S5BwfNwIDAQABAoICDQUBagMb\n"
                "Z/3KTQ1SW5gT4WXcx424XVzT/VJrNmhKqSkbs3yQdRt+O2kMLpNpsgDxCy+TCAN3\n"
                "ZLFjeMOt8YGYaa1G0XGPb4KHtf0eB2sci2MJLyZ1p1Xp3PGNXgTzF3FSDZ6gdyr0\n"
                "ApR2190vbh9XEqPB8/1EVGtDYGMbJn4J4g3Tpnz60VETWWn4B0Z43NPBpZIyzb3g\n"
                "qZ1Y79JMb3P+Nb7QWoV6Pkl8KiabST5qybU7odsp705wfnXWbbuMmUNfxBB0or1x\n"
                "w9Ed6L6KZLq9N2DmtMrFBI6sVvsQZxH7vV+9uZpFIm2mzzLIDzRxVZB5uWMVbMAQ\n"
                "Ha5IdWwg00Jl8rqFOpASR/heLLxP+7oK58OBNIyUL3ZuXez06hRsTauf64TlSNco\n"
                "eLObReWclBlKqviZUV5mmyTzJyng7RE3W0eHIRYvZlyaBJl8vcBayIBPPAS9SEsP\n"
                "xpVXZyiPEhCUk1T/XZ1HWA6/7yQB25XuzMaLVkI589dlndM5O3WFBmp4PUW2DyzH\n"
                "DZhg86+W4PSuujN63LudqKi0JM1g5BSaQt0PB7V4OK33uQMc1qZYeE8l1xdD2Whb\n"
                "QHLuNrxvYcBaSygx02KEoENU0XeAHMyaEhHyZwGUqZDK13zAOQQrCDbdcwBWAkah\n"
                "0Dg7sCshUq7bf8f58oQdzkgBBnrV156keDzVC0U3ANNV2QQ02QIBsQKCAQcDPP6s\n"
                "UPUYANnlrokdy+FxBpyafyAlET8He5/1zc17SMRY3R5gizRFVfKDukxCqXClN8MD\n"
                "e3QdgH1+AEHzVZFRLduWCsDq3m1El76W3knQ8wecBy96pHXkoeDJYWrbbnvosnZJ\n"
                "/P2WVrLG+QSzKRJVSFH66rXE2fmO8M2bQMI8lIlZ4mrz76wjxcl1M2T+peO8Wn2r\n"
                "5MPqZu8rlU+t1Ugd3iK0DolXEq0xVk28r8jB8ky3YzZQf/d4UmnCEUVmSbxm5Pxs\n"
                "AtLlw7cqtJT6T1/x/WKTCvK0IIneBGq2MyTGqUvoLMfvnJfuRM9AfF1VuHg4fJks\n"
                "rZLnvHHbQ+vc2jid1MmY1NjvnQKCAQcDcRRDHrJzqCAlms4GuqPJNOIev8xB3b6a\n"
                "325ME/b+lb9h38OFqYz5v/LyT0mMhljWnJXjfo5xnVQm5RVAxA2jMh7jDSmraVz3\n"
                "1Q8NhSH+8iLCVaFVIzJG3YB6gZ0S5TxrnBT/f4yokEEt41t9o39tTioiq++5SbE+\n"
                "qwi7vQ2tMcjpilLIC4Lu/UUdUlAVcMOgqDf2xrgyjhnRZRAv7zxtb2Ka1C1UkCXG\n"
                "fGYIbP/YPUq4tQy2tpxq2G9+y5CPQx8ufw6um/r7pXogtTycgWylLnqddx6Jqrig\n"
                "d5T0ImguPv0v+UAKZCpGgRMqeI9y+MPljE2MSRqOlaV81CZgK208GZwDYaMT4wKC\n"
                "AQcC8208B5YhJn1psO/gSC8K+TRyEVBwltOx9PTiYIVUSA4s0GrjHVcnq9eQNI9T\n"
                "2+X7mOHL5Y79Z150GLYAkUQYDsrgYrJEFSbLb+BMyQnJL/4KL/4TK5UHIICf4ncm\n"
                "uPqPJTln2PQZMK4/ZSLkRJQhRQL3vTSgyuWAXW1vgca+v7ieQRanbguWmaEofQoW\n"
                "h4MM3AVTQ+dITj66n5h5VzcdiJRlMi3zO+C5aeTzAdjW6/7+ypjvKH2RlsArCeQM\n"
                "/zqBJT/lCXm3yO68KszrgLN06CsQxdQ/UrtvpuS7XcWwhwvV6iDT+AX3KZsXL306\n"
                "JRzglKJctVt+cxnp7m4b1nvrT8HZ1HRPfQKCAQY1FyB4QA6CCfXaHyH+qxHbsuhh\n"
                "bEBnyS1x2yaQaWirw011e0WZktoVu+Dn8CmcisvbwZhkrtafwUtasG4noh68TWon\n"
                "B+TBQ43Xc8G/zO2cz4VgPYlwxn3IqQ44sytJTtu5GvbOS754esT2FzQ53trKQ/W0\n"
                "4IwMqbZ5/du6J5HRFycjY5uUPf6CmmCK7jJsig0rNbwT+1Nohpu8eD47Lyv08z8b\n"
                "G+Qlj3EnW8qULtJr1w3MMwjrdf9mLUm5oGtRgxZ9J3hUA8qYDQTdhtpzXgWSCGdm\n"
                "nxtygw+ARSR00kw/FWiHn1lA8d8vteTwQMyPutYhHycd3JDM6Zzc97cBxuJBNMpr\n"
                "XrU7AoIBBwKthCt2MkGMu/wzKuvrIrmr129YzpQqTiUjrzwmmMYHRcN+hkBysqdk\n"
                "+oAKGf0AN2OgO+NePHRE4zxnmVMEXIAKob3adPlBGhWYZrkZtwE8pvqp+Lnc9Mjf\n"
                "TVpObkhyD7gAjuLdeXFRLgr/ETLqTqzxf/j5a7s4ni2KzqDGRe/SyW8AMaoKrs/e\n"
                "h8wU8GCyIWCrOuj/2iG44/5LTwOQTDYbRhNZ3ERveUQM7yKlPl6+MVLPqEh/j+f+\n"
                "UMODqjYEZTRmYWymm4k6WiWZFlJSJZE37GhCr26SCFLuxpH1rgG6gt98VaY20Yk5\n"
                "wzOuvoRosb2EpQeAReNA9mBpoWWq3zc7Jnwvc3cq\n"
                "-----END PRIVATE KEY-----"
            )

    @cached_property
    def jwt_public_key(self) -> str:
        try:
            result = self._string(self._variables.jwt_public_key)
            if self._publicKeyPattern.match(result):
                return result
            return (
                f"-----BEGIN PUBLIC KEY-----\n"
                + self._whitespacePattern.sub("\n", result)
                + f"\n-----END PUBLIC KEY-----"
            )
        except ConfigurationMissingVariable as error:
            if self._secure:
                raise error
            return (
                "-----BEGIN PUBLIC KEY-----\n"
                "MIICLjANBgkqhkiG9w0BAQEFAAOCAhsAMIICFgKCAg0LJSoMQiCbvRbe9kjENZbG\n"
                "vNnOJUldTOL0Q1wrxlTQtf12cOg4hwtIci0wNBeuD91+dmLBQGodibLu9Y5WieZo\n"
                "017/HtmyPP2orZIKKIRWHAZUIORSLwaWanzPkKQ+6axWMTVPZnyENpaAH9OY/4NE\n"
                "zUHMRT8Em5x8/tBL2EVePiMbuKqSrd2jpVlPPBfWGZT8TFP8/oRbhOOxIkzseuRw\n"
                "JTyRQO7UNCWHA5CMckAeGtCflBqVJEatm7t7Q0Xf97cVLPVstG4rVAQTBcBYPlyP\n"
                "G7CfbBF/HKnoX1eje9z2VoiefaqdksSKdOA5Vo6MlDhmsFj4XwadDy7iXIAfq0wA\n"
                "jmdWMuXPIWQCzJPEM0rkPUedzpPv7Q33gNxXUGzpVLKX+refpSnsAuecoxgfL261\n"
                "QzEn8XfMQIgLh96qobu4O9qMxDieWVzKdR7rKmwjJ/0ptP31wPwVkHJZpDqHivE+\n"
                "L5MxuMM0Vk5niCyKDsbaj5zGwKNAPj21dUyaZia5a6f2BwSENnjJnTwlB6LZWUVd\n"
                "ETGFOoiTZqkR18WJs5MULBKTNxvgVxwBPsItl2TlJaAye3N7N+UFe8OJg1yio3sG\n"
                "l8fykuS4AMslOjZEc40GrmptaMgLeffDTa1d1NHDt61u2DokU9IxyNBru0r76AzD\n"
                "jpXupeOBGWl1d6rSpzU1rKsuhld55n5OEuQcHzcCAwEAAQ==\n"
                "-----END PUBLIC KEY-----"
            )

    @property
    def password_pepper(self) -> str:
        try:
            return self._string(self._variables.password_pepper)
        except ConfigurationMissingVariable as error:
            if self._secure:
                raise error
            return ""

    def _write(self) -> None:
        self._set(
            self._variables.jwt_private_key,
            self.jwt_private_key.removeprefix("-----BEGIN PRIVATE KEY-----")
            .lstrip()
            .removesuffix("-----END PRIVATE KEY-----")
            .rstrip(),
        )
        self._set(
            self._variables.jwt_public_key,
            self.jwt_public_key.removeprefix("-----BEGIN PUBLIC KEY-----")
            .lstrip()
            .removesuffix("-----END PUBLIC KEY-----")
            .rstrip(),
        )
        self._set(
            self._variables.password_pepper,
            self.password_pepper,
        )