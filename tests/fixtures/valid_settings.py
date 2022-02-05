from pydantic import BaseSettings, Field

SETTINGS_ATTR = "logging_level"
SETTINGS_MARKDOWN_FIRST_LINE = f"# `{SETTINGS_ATTR}`\n"


class EmptySettings(BaseSettings):
    logging_level: str

    class Config:
        title = "Empty"


class FullSettings(BaseSettings):
    logging_level: str = Field(
        "some_value",
        description="use FullSettings like this",
        example="this is an example use",
        possible_values=["aaa", "bbb"],
    )

    class Config:
        title = "Full"


class RequiredSettings(BaseSettings):
    logging_level: str = Field(..., description="RequiredSettings")

    class Config:
        title = "Required"


class MultipleSettings(BaseSettings):
    username: str
    password: str
