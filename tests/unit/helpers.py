from typing import List, Type

from pydantic import BaseSettings
from pytest_mock import MockerFixture
from typer.testing import CliRunner

from settings_docgen.main import app


def run_app_with_settings(
    mocker: MockerFixture, runner: CliRunner, settings: Type[BaseSettings], args: List[str] = None
) -> str:
    if args is None:
        args = []

    mocker.patch("settings_docgen.main.import_class_path", return_value=settings)
    result = runner.invoke(
        app, ["--class", "MockedClass", "--output-format", "markdown"] + args, catch_exceptions=False
    )
    return result.stdout.lower()
