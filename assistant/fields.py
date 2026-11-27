"""Validated value types (fields) that make up a contact record.

Each field checks its value when it is created and raises ValueError
with a message for the user if the value is invalid.
"""

import re
from datetime import datetime


DATE_FORMAT = "%d.%m.%Y"
EMAIL_PATTERN = (
    r"^[a-zA-Z0-9](?:[a-zA-Z0-9_.+-]*[a-zA-Z0-9])?"
    r"@[a-zA-Z0-9](?:[a-zA-Z0-9-]*[a-zA-Z0-9])?"
    r"(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]*[a-zA-Z0-9])?)*\.[a-zA-Z]{2,}$"
)


class Field:
    """Base class for a contact field that stores one value."""

    def __init__(self, value):
        """Store the value as is; subclasses validate it first."""
        self.value = value

    def __str__(self):
        """Return the value as text."""
        return str(self.value)


class Name(Field):
    """Contact name; must not be empty."""

    def __init__(self, value: str):
        """Strip spaces and raise ValueError if the name is empty."""
        value = value.strip()
        if not value:
            raise ValueError("Name cannot be empty.")
        super().__init__(value)


class Phone(Field):
    """Phone number of exactly 10 digits."""

    def __init__(self, value: str):
        """Raise ValueError unless the value is exactly 10 digits."""
        if not re.fullmatch(r"[0-9]{10}", value):
            raise ValueError("Phone number must contain exactly 10 digits.")
        super().__init__(value)


class Birthday(Field):
    """Birthday stored as a datetime; entered and shown as DD.MM.YYYY."""

    def __init__(self, value: str):
        """Parse a DD.MM.YYYY date and validate it.

        Raise ValueError for a wrong format, a date that does not exist,
        or a date in the future.
        """
        try:
            birthday = datetime.strptime(value, DATE_FORMAT)
        except ValueError:
            # The format is right, but the date does not exist (e.g. 31.02).
            if re.fullmatch(r"[0-9]{1,2}\.[0-9]{1,2}\.[0-9]{4}", value):
                raise ValueError(f"Date {value} does not exist.") from None
            raise ValueError("Invalid date format. Use DD.MM.YYYY.") from None
        if birthday > datetime.today():
            raise ValueError("Birthday cannot be in the future.")
        super().__init__(birthday)

    def __str__(self):
        """Return the date as DD.MM.YYYY."""
        return self.value.strftime(DATE_FORMAT)


class Email(Field):
    """Email address like user@example.com, stored in lowercase."""

    def __init__(self, value: str):
        """Raise ValueError if the value does not look like an email."""
        value = value.strip()
        if not re.fullmatch(EMAIL_PATTERN, value):
            raise ValueError("Invalid email format. Example: user@example.com")
        super().__init__(value.lower())


class Address(Field):
    """Free-text address; must not be empty."""

    def __init__(self, value: str):
        """Strip spaces and raise ValueError if the address is empty."""
        value = value.strip()
        if not value:
            raise ValueError("Address cannot be empty.")
        super().__init__(value)
