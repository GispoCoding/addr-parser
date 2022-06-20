"""Command line tool for Address Parser."""


import json
from dataclasses import asdict

import click

from addrparser.parser import AddressParseException, AddressParser


def locale_parser_factory(locale: str) -> AddressParser:
    """Creates and returns an AddressParser with locele support.

    Args:
        locale (str): Two-letter ISO-3166 country code

    Raises:
        click.Abort: Raises if no support for given country code

    Returns:
        AddressParser: AddressParser for parsing addresses of given country
    """

    try:
        parser = AddressParser(locale)
    except ValueError:
        click.echo(f"Parsing with such locale '{locale}' is not supported.")
        raise click.Abort()
    return parser


@click.command()
@click.argument("address")
@click.option(
    "-l",
    "--locale",
    type=click.STRING,
    default="fi",
    help="Country code in two-letter ISO 3166",
)
def main(address: str, locale: str) -> None:
    """Cli tool for parsing text addresses.

    Args:
        address (str): address text
    """
    parser = locale_parser_factory(locale)

    address = address.replace(r"\n", "\n")
    try:
        result = parser.parse(address)
    except AddressParseException as e:
        click.echo(f'"{address}" is not valid. {e}')
        raise click.Abort()

    address_with_newline = address.replace("\n", r"\n")
    data = {
        "input": address_with_newline,
        "result": {k: v for k, v in asdict(result).items() if v is not None},
    }
    click.echo(json.dumps(data, indent=2, ensure_ascii=False))
