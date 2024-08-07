from dataclasses import dataclass, field
from typing import Optional


@dataclass
class Booking:

    firstname: Optional[str] = field(default=None)
    lastname: Optional[str] = field(default=None)
    totalprice: Optional[str] = field(default=None)
    depositpaid: Optional[str] = field(default=None)
    bookingdates_checking: Optional[str] = field(default=None)
    bookingdates_checkout: Optional[str] = field(default=None)
    additionalneeds: Optional[str] = field(default=None)