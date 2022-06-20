import json
from collections import OrderedDict
from typing import Callable, List, Union

import pytest
from click.testing import CliRunner, Result

from addrparser.cli import main as addrparser


@pytest.fixture
def addrparser_invoker() -> Callable[[List[str]], Result]:
    def inner(command: List[str]) -> Result:
        runner = CliRunner()
        result = runner.invoke(addrparser, command)
        return result

    return inner


def output2dict(output: str) -> Union[OrderedDict, None]:
    data = json.loads(output, object_pairs_hook=OrderedDict)
    if isinstance(data, OrderedDict):
        return data
    return None


def test_cli_parser(addrparser_invoker: Callable[[List[str]], Result]) -> None:
    address = "Katu 7b"

    result = addrparser_invoker([address])
    assert result.exit_code == 0

    parsed = output2dict(result.output)
    assert parsed == OrderedDict(
        {"input": address, "result": {"street_name": "Katu", "house_number": "7b"}}
    )


def test_cli_parser_with_locale(
    addrparser_invoker: Callable[[List[str]], Result]
) -> None:
    address = "Katu 7b"
    result = addrparser_invoker([address, "--locale", "fi"])
    assert result.exit_code == 0
    parsed = output2dict(result.output)
    assert parsed == OrderedDict(
        {"input": address, "result": {"street_name": "Katu", "house_number": "7b"}}
    )


def test_cli_parser_multiline(
    addrparser_invoker: Callable[[List[str]], Result]
) -> None:
    address = r"Katu 7b\n65100 Vaasa"
    result = addrparser_invoker([address, "--locale", "fi"])
    assert result.exit_code == 0
    parsed = output2dict(result.output)
    assert parsed == OrderedDict(
        {
            "input": address,
            "result": {
                "street_name": "Katu",
                "house_number": "7b",
                "zip_number": "65100",
                "zip_name": "Vaasa",
            },
        }
    )


def test_cli_running_with_invalid_address_should_fail(
    addrparser_invoker: Callable[[List[str]], Result]
) -> None:
    result = addrparser_invoker(["Katu 7b8"])
    assert result.exit_code == 1
    assert result.output == (
        '"Katu 7b8" is not valid. Address has invalid form. Expected end of text, '
        "found '8'  (at char 7), (line:1, col:8)\n"
        "Aborted!\n"
    )


def test_cli_running_with_unsupported_locale_should_fail(
    addrparser_invoker: Callable[[List[str]], Result]
) -> None:
    result = addrparser_invoker(["Katu 7b", "--locale", "sv"])
    assert result.exit_code == 1
    assert (
        result.output == "Parsing with such locale 'sv' is not supported.\nAborted!\n"
    )
