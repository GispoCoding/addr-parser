from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from addrparser import Address

    class LocaleModuleInterface:
        @staticmethod
        def parse(address: str) -> "Address":
            ...


class AddressParseException(ValueError):
    ...


def _get_locale_module(locale: str) -> "LocaleModuleInterface":
    return __import__(f"addrparser.locales.{locale}", fromlist=["_"])  # type: ignore


class AddressParser:
    """Class"""

    def __init__(self, locale: str) -> None:
        """_summary_

        Args:
            locale (str): _description_

        Raises:
            ValueError: _description_
        """
        try:
            self._parser_module = _get_locale_module(locale)
        except ImportError:
            raise ValueError(f"No such locale '{locale}'")

    def parse(self, address: str) -> "Address":
        """Proxy function to localized parse functions.

        Localized parse functions parses an address in text format and returns a
        structured Address named tuple.

        Args:
            address (str): Address in text to be parsed

        Raises:
            AddressParseException: Raises a AddressParseException if the address is
                invalid

        Returns:
            Address: Named tuple containing structured address info
        """

        return self._parser_module.parse(address)
