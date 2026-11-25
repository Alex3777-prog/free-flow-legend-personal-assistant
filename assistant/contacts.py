from collections import UserDict
from datetime import date, timedelta
from .fields import Name, Phone, Birthday, DATE_FORMAT


UPCOMING_DAYS = 7
WEEKEND_LOOKBACK_DAYS = 2


class Record:
    def __init__(self, name: str):
        self.name = Name(name)
        self.phones: list[Phone] = []
        self.birthday: Birthday | None = None

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

    def __str__(self):
        phones = "; ".join(p.value for p in self.phones)
        birthday = self.birthday or "not specified"
        return (
            f"Contact name: {self.name.value}, "
            f"phones: {phones}, birthday: {birthday}"
        )


class AddressBook(UserDict):
    def add_record(self, record: Record) -> None:
        self.data[record.name.value] = record

    def find(self, name: str) -> Record | None:
        return self.data.get(name)

    def delete(self, name: str) -> None:
        self.data.pop(name, None)

    def get_upcoming_birthdays(
        self, today: date | None = None
    ) -> list[dict[str, str]]:
        today = today or date.today()
        search_start = today - timedelta(days=WEEKEND_LOOKBACK_DAYS)
        upcoming = []

        for record in self.data.values():
            if record.birthday is None:
                continue

            birthday = record.birthday.value.date()
            next_birthday = self._next_birthday(birthday, search_start)
            if (next_birthday - today).days >= UPCOMING_DAYS:
                continue

            greeting_date = self._shift_to_weekday(next_birthday)
            if greeting_date < today:
                continue

            upcoming.append(
                {
                    "name": record.name.value,
                    "congratulation_date": greeting_date.strftime(DATE_FORMAT),
                }
            )

        return upcoming

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

    @staticmethod
    def _shift_to_weekday(day: date) -> date:
        """Move Saturday and Sunday to the following Monday."""
        if day.weekday() >= 5:
            return day + timedelta(days=7 - day.weekday())
        return day
