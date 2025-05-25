from dataclasses import dataclass, asdict

@dataclass
class User:
    first_name: str
    last_name: str
    age: int

    def to_dict(self) -> dict:
        """Converts the User instance to a dictionary."""
        return asdict(self)
