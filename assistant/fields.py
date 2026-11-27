import re
from datetime import datetime


DATE_FORMAT = "%d.%m.%Y"
EMAIL_PATTERN = (
    r"^[a-zA-Z0-9](?:[a-zA-Z0-9_.+-]*[a-zA-Z0-9])?"
    r"@[a-zA-Z0-9](?:[a-zA-Z0-9-]*[a-zA-Z0-9])?"
    r"(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]*[a-zA-Z0-9])?)*\.[a-zA-Z]{2,}$"
)


class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    def __init__(self, value: str):
        value = value.strip()
        if not value:
            raise ValueError("Name cannot be empty.")
        super().__init__(value)


class Phone(Field):
    def __init__(self, value: str):
        if not re.fullmatch(r"[0-9]{10}", value):
            raise ValueError("Phone number must contain exactly 10 digits.")
        super().__init__(value)


class Birthday(Field):
    def __init__(self, value: str):
        try:
            birthday = datetime.strptime(value, DATE_FORMAT)
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY") from None
        if birthday > datetime.today():
            raise ValueError("Birthday cannot be in the future.")
        super().__init__(birthday)

    def __str__(self):
        return self.value.strftime(DATE_FORMAT)


class Email(Field):
    def __init__(self, value: str):
        value = value.strip()
        if not re.fullmatch(EMAIL_PATTERN, value):
            raise ValueError("Invalid email format. Example: user@example.com")
        super().__init__(value.lower())


class Address(Field):
    def __init__(self, value: str):
        value = value.strip()
        if not value:
            raise ValueError("Address cannot be empty.")
        super().__init__(value)