from dataclasses import dataclass, field
from typing import Optional


@dataclass
class Client:
    first_name: str
    last_name: str
    ssn_tin: str
    email: str
    contactPhone: str
    city: str
    state: str
    repId: str
    clientId: Optional[str] = field(default=None)

    def compare(self, actual) -> bool:
        return (self.first_name == actual.first_name and
                self.last_name == actual.last_name and
                self.ssn_tin == actual.ssn_tin and
                self.email == actual.email and
                self.contactPhone == actual.contactPhone and
                self.city == actual.city and
                self.state == actual.state and
                self.repId == actual.repId and
                self.clientId == actual.clientId)
