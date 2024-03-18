# from .configuration import ApiConfiguration
# from .configuration import Variables
# from pathlib import Path
# import os
# import re
#
# original = os.environ.copy()
#
#
# private_pattern = re.compile(
#     r"^-----BEGIN PRIVATE KEY-----\n.*\n-----END PRIVATE KEY-----(\n|$)",
#     re.DOTALL,
# )
# public_pattern = re.compile(
#     r"^-----BEGIN PUBLIC KEY-----\n.*\n-----END PUBLIC KEY-----(\n|$)",
#     re.DOTALL,
# )
#
#
# def test_defaults():
#     configuration = ApiConfiguration()
#     assert configuration.mode == "dev"
#     assert private_pattern.search(configuration.jwt_private_key)
#     assert public_pattern.search(configuration.jwt_public_key)
#     assert configuration.password_pepper == ""
#     assert configuration.port == 8080
#     assert len(configuration.environment) == 3
#
#
# async def test_modified_defaults():
#     defaults = {
#         Variables.password_pepper: "pepper",
#         Variables.jwt_private_key: __file__,
#         Variables.jwt_public_key: __file__,
#     }
#     configuration = ApiConfiguration(
#         defaults=defaults,
#     )
#     with Path(__file__) as file:
#         contents = file.read_text()
#     assert configuration.jwt_private_key == contents
#     assert configuration.jwt_public_key == contents
#     assert configuration.password_pepper == "pepper"
#     assert len(configuration.environment) == 5
#
#
# async def test_overwriting_defaults():
#     defaults = {
#         Variables.password_pepper: "pepper",
#         Variables.jwt_private_key: __file__,
#         Variables.jwt_public_key: __file__,
#     }
#     cli = {
#         Variables.password_pepper: "",
#         Variables.jwt_private_key: None,
#         Variables.jwt_public_key: None,
#     }
#     configuration = ApiConfiguration(
#         cli=cli,
#         defaults=defaults,
#     )
#     assert configuration.mode == "dev"
#     assert configuration.password_pepper == ""
#     assert private_pattern.search(configuration.jwt_private_key)
#     assert public_pattern.search(configuration.jwt_public_key)
