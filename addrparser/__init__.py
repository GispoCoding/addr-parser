"""Top-level package for Address Parser."""

from dataclasses import dataclass
from typing import Optional

from .parser import AddressParseException, AddressParser

__author__ = """Lauri Kajan"""
__email__ = "lauri.kajan@gispo.fi"
__version__ = "0.2.0"


@dataclass
class Address:
    """Structured Address info."""

    street_name: Optional[str] = None
    house_number: Optional[str] = None
    entrance: Optional[str] = None
    apartment: Optional[str] = None
    post_office_box: Optional[str] = None
    zip_number: Optional[str] = None
    zip_name: Optional[str] = None


__all__ = ["Address", "AddressParseException", "AddressParser"]
