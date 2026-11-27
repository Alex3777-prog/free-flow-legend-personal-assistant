from __future__ import annotations

from collections import UserDict
from datetime import date
from .fields import Name, Phone, Birthday, Email, Address, DATE_FORMAT


UPCOMING_DAYS = 7


class Record:
    def __init__(self, name: str):
        self.name = Name(name)
        self.phones: list[Phone] = []
        self.birthday: Birthday | None = None
        self.email: Email | None = None
        self.address: Address | None = None

    def add_phone(self, phone: str) -> None:
        if self.find_phone(phone):
            raise ValueError("This phone number already exists.")
        self.phones.append(Phone(phone))

    def find_phone(self, phone: str) -> Phone | None:
        return next((p for p in self.phones if p.value == phone), None)

    def remove_phone(self, phone: str) -> None:
        found = self.find_phone(phone)
        if found is None:
            raise ValueError("Phone not found.")
        self.phones.remove(found)

    def edit_phone(self, old_phone: str, new_phone: str) -> None:
        found = self.find_phone(old_phone)
        if found is None:
            raise ValueError("Phone not found.")
        if new_phone != old_phone and self.find_phone(new_phone):
            raise ValueError("This phone number already exists.")
        self.phones[self.phones.index(found)] = Phone(new_phone)

    def add_birthday(self, birthday: str) -> None:
        self.birthday = Birthday(birthday)

    def remove_birthday(self) -> None:
        if self.birthday is None:
            raise ValueError("Birthday is not specified.")
        self.birthday = None

    def add_email(self, email: str) -> None:
        self.email = Email(email)

    def edit_email(self, new_email: str) -> None:
        self.email = Email(new_email)

    def remove_email(self) -> None:
        if self.email is None:
            raise ValueError("Email is not specified.")
        self.email = None

    def add_address(self, address: str) -> None:
        self.address = Address(address)

    def edit_address(self, new_address: str) -> None:
        self.address = Address(new_address)

    def remove_address(self) -> None:
        if self.address is None:
            raise ValueError("Address is not specified.")
        self.address = None

    def matches(self, query: str) -> bool:
        """Check if query partially matches name, phones, email, or address."""
        q = query.strip().lower()
        if not q:
            return False

        if q in self.name.value.lower():
            return True
        if any(q in p.value.lower() for p in self.phones):
            return True
        if self.email and q in self.email.value.lower():
            return True
        if self.address and q in self.address.value.lower():
            return True

        return False

    def __str__(self):
        phones = "; ".join(p.value for p in self.phones) or "not specified"
        birthday = self.birthday or "not specified"
        email = self.email or "not specified"
        address = self.address or "not specified"
        return (
            f"Contact name: {self.name.value}, "
            f"phones: {phones}, "
            f"birthday: {birthday}, "
            f"email: {email}, "
            f"address: {address}"
        )


class AddressBook(UserDict):
    def add_record(self, record: Record) -> None:
        if self.find(record.name.value) is not None:
            raise ValueError(f"Contact '{record.name.value}' already exists.")
        self.data[record.name.value] = record

    def find(self, name: str) -> Record | None:
        if name in self.data:
            return self.data[name]
        name_lower = name.lower()
        for key, record in self.data.items():
            if key.lower() == name_lower:
                return record
        return None

    def delete(self, name: str) -> bool:
        record = self.find(name)
        if record is None:
            return False
        del self.data[record.name.value]
        return True

    def rename_record(self, old_name: str, new_name: str) -> None:
        record = self.find(old_name)
        if record is None:
            raise ValueError("Contact not found.")

        validated_name = Name(new_name)
        existing = self.find(validated_name.value)
        if existing is not None and existing is not record:
            raise ValueError(
                f"Contact '{validated_name.value}' already exists."
            )

        del self.data[record.name.value]
        record.name = validated_name
        self.data[record.name.value] = record

    def search(self, query: str) -> list[Record]:
        return [
            record for record in self.data.values() if record.matches(query)
        ]

    def get_upcoming_birthdays(
        self, days: int = UPCOMING_DAYS, today: date | None = None
    ) -> list[dict[str, str]]:
        if days < 1:
            raise ValueError("Number of days must be a positive integer.")

        today = today or date.today()
        upcoming = []

        for record in self.data.values():
            if record.birthday is None:
                continue

            birthday = record.birthday.value.date()
            next_birthday = self._next_birthday(birthday, today)
            if 0 <= (next_birthday - today).days <= days:
                upcoming.append((next_birthday, record.name.value))

        # Soonest first; contacts with the same date go in name order.
        upcoming.sort(key=lambda item: (item[0], item[1].lower()))
        return [
            {"name": name, "congratulation_date": day.strftime(DATE_FORMAT)}
            for day, name in upcoming
        ]

    @staticmethod
    def _birthday_in_year(birthday: date, year: int) -> date:
        try:
            return birthday.replace(year=year)
        except ValueError:  # 29.02 in a non-leap year
            return birthday.replace(year=year, day=28)

    @classmethod
    def _next_birthday(cls, birthday: date, today: date) -> date:
        next_birthday = cls._birthday_in_year(birthday, today.year)
        if next_birthday < today:
            next_birthday = cls._birthday_in_year(birthday, today.year + 1)
        return next_birthday
