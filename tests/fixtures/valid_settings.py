from typing import Literal

from pydantic import AliasChoices, AliasPath, BaseModel, Field
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing_extensions import Annotated

SETTINGS_ATTR = "logging_level"
SETTINGS_MARKDOWN_FIRST_LINE = f"# `{SETTINGS_ATTR}`\n"


class EmptySettings(BaseSettings):
    logging_level: str


class FullSettings(BaseSettings):
    logging_level: str = Field(
        "some_value",
        description="use FullSettings like this",
        examples=["aaa", "bbb"],
    )


class PossibleValuesSettings(BaseSettings):
    literal: Literal["debug", "info"]
    simple: str = Field(..., json_schema_extra={"possible_values": ["debug", "info"]})
    simple_tuple: str = Field(..., json_schema_extra={"possible_values": [["debug"], ["info"]]})
    tuple_with_explanation: str = Field(
        ..., json_schema_extra={"possible_values": [["debug", "Debug level"], ["info", "Info level"]]}
    )


class ExamplesSettings(BaseSettings):
    only_values: str = Field(..., examples=["debug", "info"])
    structured_text: str = Field(..., json_schema_extra={"examples": "debug, info"})
    simple: str = Field(..., json_schema_extra={"examples": ["debug", "info"]})
    simple_tuple: str = Field(..., json_schema_extra={"examples": [["debug"], ["info"]]})
    tuple_with_explanation: str = Field(
        ..., json_schema_extra={"examples": [["debug", "Debug level"], ["info", "Info level"]]}
    )
    possible_values_and_examples: str = Field(
        ...,
        json_schema_extra={
            "possible_values": [["debug", "Debug level"], ["info", "Info level"]],
            "examples": [["debug", "Debug level"], ["info", "Info level"]],
        },
    )


class RequiredSettings(BaseSettings):
    logging_level: str = Field(..., description="RequiredSettings")


class MultipleSettings(BaseSettings):
    username: str
    password: str


class ValidationAliasSettings(BaseSettings):
    logging_level_alias: str = Field(..., validation_alias="logging_level")


class ValidationAliasPathSettings(BaseSettings):
    logging_level: str = Field(..., validation_alias=AliasPath("logging_level", 0))


class ValidationAliasChoicesSettings(BaseSettings):
    logging_level: str = Field(..., validation_alias=AliasChoices("logging", "level"))


class EnvPrefixSettings(BaseSettings):
    logging_level: str

    model_config = SettingsConfigDict(env_prefix="PREFIX_")


class DeepSubModel(BaseModel):
    leaf: str


class SubModel(BaseModel):
    nested: str
    deep: DeepSubModel


class EnvNestedDelimiterSettings(BaseSettings):
    """Expected environment variables.

    - `DIRECT`
    - `SUB_MODEL__NESTED`
    - `SUB_MODEL__DEEP__LEAF`
    """

    model_config = SettingsConfigDict(env_nested_delimiter="__")

    direct: str
    sub_model: SubModel


class EnvPrefixAndNestedDelimiterSettings(BaseSettings):
    """Expected environment variables.

    - `PREFIX_DIRECT`
    - `PREFIX_SUB_MODEL__NESTED`
    - `PREFIX_SUB_MODEL__DEEP__LEAF`
    """

    model_config = SettingsConfigDict(env_prefix="PREFIX_", env_nested_delimiter="__")

    direct: str
    sub_model: SubModel


class SimpleSubModel(BaseModel):
    leaf: str


class SettingsSubModelWithSubModel(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="PREFIX_SUB_MODEL_", env_nested_delimiter="__")

    nested: str
    sub_model_2: SimpleSubModel


class SettingsWithSettingsSubModel(BaseSettings):
    """Expected environment variables.

    - `PREFIX_DIRECT`
    - `PREFIX_SUB_MODEL_NESTED`
    - `PREFIX_SUB_MODEL_SUB_MODEL_2__LEAF`
    """

    model_config = SettingsConfigDict(env_prefix="PREFIX_")

    direct: str
    sub_model_1: Annotated[SettingsSubModelWithSubModel, Field(default_factory=SettingsSubModelWithSubModel)]


class SettingsSubModel(BaseSettings):
    """Expected environment variables.

    - `LEAF`
    """

    model_config = SettingsConfigDict(env_prefix="")
    leaf: str


class SettingsWithSettingsSubModelNoPrefixOrDelimiter(BaseSettings):
    """Expected environment variables.

    - `LEAF`
    """

    my_leaf: Annotated[SettingsSubModel, Field(default_factory=SettingsSubModel)]
