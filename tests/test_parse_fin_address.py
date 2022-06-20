import pytest

from addrparser import Address, AddressParseException, AddressParser


@pytest.fixture(scope="module")
def parser() -> AddressParser:
    return AddressParser("fi")


@pytest.mark.parametrize(
    "input, expected",
    [
        ("Saari", Address("Saari")),
        ("Katu 25", Address("Katu", "25")),
        ("Katu 25 B", Address("Katu", "25", "B")),
        ("Katu 25 B 13", Address("Katu", "25", "B", "13")),
        ("Katu 25 as. 13", Address("Katu", "25", apartment="13")),
        ("Katu 25 bst. 13", Address("Katu", "25", apartment="13")),
        ("Katu 25b", Address("Katu", "25b")),
        ("Katu 25-27", Address("Katu", "25-27")),
        ("Katu 25-27 B 13", Address("Katu", "25-27", "B", "13")),
        ("Katu 25b B 13", Address("Katu", "25b", "B", "13")),
        ("Saaran polku 7", Address("Saaran polku", "7")),
        ("Kaarle IX:n katu 3", Address("Kaarle IX:n katu", "3")),
        ("PL 55", Address(post_office_box="PL 55")),
        (
            "Katu 25, 65100 Vaasa",
            Address("Katu", "25", zip_number="65100", zip_name="Vaasa"),
        ),
        (
            "PL 102\n65100 Vaasa",
            Address(post_office_box="PL 102", zip_number="65100", zip_name="Vaasa"),
        ),
        (
            "Katu 25\n65100 Vaasa",
            Address(
                "Katu",
                "25",
                zip_number="65100",
                zip_name="Vaasa",
            ),
        ),
        (
            "Katu 25-27 B 13\n65100 Vaasa",
            Address(
                "Katu",
                "25-27",
                "B",
                "13",
                zip_number="65100",
                zip_name="Vaasa",
            ),
        ),
    ],
)
def test_address_parsing(
    parser: "AddressParser", input: str, expected: Address
) -> None:
    """Test for various test cases that should all pass

    Args:
        input (str): Input address text for valid addesses
        expected (Address): Expected result
    """
    assert parser.parse(input) == expected


invalid_test_cases = {
    "ei järkeä": "1 2 3",
    "asuntonumero ilman porrasta": "Katu 1 2",
    "osoitenro ja porras ei erotettu": "Katu 7B",
    "numerovälissä jakokirjaimia": "Katu 7b-8a",
}


@pytest.mark.parametrize(
    "input",
    invalid_test_cases.values(),
    ids=invalid_test_cases.keys(),
)
def test_address_parsing_should_raise_on_invalid_address(
    parser: "AddressParser", input: str
) -> None:
    """Test cases with invalid addresses

    Args:
        input (str): Invalid Address text
    """
    with pytest.raises(AddressParseException):
        parser.parse(input)
