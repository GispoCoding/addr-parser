from functools import partial

from pyparsing import Combine, LineEnd, OneOrMore
from pyparsing import Optional as Opt
from pyparsing import (
    Or,
    ParseException,
    ParserElement,
    Suppress,
    White,
    Word,
    nums,
    one_of,
    pyparsing_unicode,
    srange,
)

from addrparser import Address, AddressParseException

ParserElement.set_default_whitespace_chars(" \t")
Space = partial(White, ws=" \t")

STREET = "osoitenimi"
HOUSE_NUMBER = "osoitenumero"
APARTMENT_NUMBER = "huoneistonumero"
ENTRANCE = "porras"
POSTBOX = "postilokero"
ZIP_NUMBER = "postinumero"
ZIP_NAME = "postitoimipaikka"

osoitenimi = Combine(
    OneOrMore(
        Suppress(Opt(Space())) + Word(pyparsing_unicode.Latin1.alphas + ":.--‑–—")
    ),
    join_string=" ",
).set_name("osoitenimi")

numero = Word(nums).set_name("numero")

osoitenumerovali = Combine(numero + Word("-‑–—", exact=1) + numero).set_name(
    "osoitenumeroväli"
)
osoitenumero_jakokirjaimella = Combine(numero + Word(srange("[a-z]"))).set_name(
    "osoitenumero jakokirjaimella"
)
osoitenumero = (numero ^ osoitenumero_jakokirjaimella ^ osoitenumerovali).set_name(
    "osoitenumero"
)

porras = Word(srange("[A-Z]")).set_name("porras")

huoneisto = Combine(Word(nums) + Opt(Word(srange("[a-z]")))).set_name("huoneistonumero")
huoneisto_osa = Or(
    [
        (porras(ENTRANCE) + Opt(Suppress(Space()) + huoneisto(APARTMENT_NUMBER))),
        (
            Suppress(one_of(["as.", "bst."]))
            + Suppress(Space())
            + huoneisto(APARTMENT_NUMBER)
        ),
    ]
)

postilokero = Combine("PL" + Space() + Word(nums)).set_name("postilokero")

katuosoite = (
    osoitenimi(STREET)
    + Opt(Suppress(Space()) + osoitenumero(HOUSE_NUMBER))
    + Opt(Suppress(Space()) + huoneisto_osa)
)

postinumero = Word(nums, exact=5)
postitoimipaikka = Word(pyparsing_unicode.Latin1.alphas)
postiosuus = (
    Suppress(("," + Space()) | LineEnd())
    + postinumero(ZIP_NUMBER)
    + Suppress(Space())
    + postitoimipaikka(ZIP_NAME)
)

osoite = (
    (postilokero("postilokero") | katuosoite) + Opt(postiosuus)
).leave_whitespace()


def parse(address: str) -> Address:
    """Parses an address in text format and returns a structured Address named tuple.

    Args:
        address (str): Address in text to be parsed

    Raises:
        AddressParseException: Raises a AddressParseException if the address is invalid

    Returns:
        Address: Named tuple containing structured address info
    """
    try:
        result = osoite.parse_string(address, parse_all=True)
    except ParseException as e:
        raise AddressParseException(f"Address has invalid form. {e}")

    return Address(
        street_name=result.get(STREET, None),
        house_number=result.get(HOUSE_NUMBER, None),
        entrance=result.get(ENTRANCE, None),
        apartment=result.get(APARTMENT_NUMBER, None),
        post_office_box=result.get(POSTBOX, None),
        zip_number=result.get(ZIP_NUMBER, None),
        zip_name=result.get(ZIP_NAME, None),
    )
