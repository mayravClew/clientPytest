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

    def compare(self, actual) -> bool:
        return (self.firstname == actual.firstname and
                self.lastname == actual.lastname and
                self.totalprice == actual.totalprice and
                self.depositpaid == actual.depositpaid and
                self.bookingdates_checking == actual.bookingdates_checking and
                self.bookingdates_checkout == actual.bookingdates_checkout and
                self.additionalneeds == actual.additionalneeds)
