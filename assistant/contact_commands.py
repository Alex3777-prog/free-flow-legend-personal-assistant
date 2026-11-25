from .contacts import AddressBook, Record
from .utils import input_error, check_args


def get_record(book: AddressBook, name: str) -> Record:
    """Return the contact or raise KeyError for input_error to report."""
    record = book.find(name)
    if record is None:
        raise KeyError(name)
    return record


@input_error
def add_contact(args: list[str], book: AddressBook) -> str:
    check_args(args, 2, "add <name> <phone>")

    name, phone = args
    record = book.find(name)
    if record is None:
        record = Record(name)
        record.add_phone(phone)
        book.add_record(record)
        return "Contact added."

    record.add_phone(phone)
    return "Contact updated."


@input_error
def change_contact(args: list[str], book: AddressBook) -> str:
    check_args(args, 3, "change <name> <old_phone> <new_phone>")

    name, old_phone, new_phone = args
    get_record(book, name).edit_phone(old_phone, new_phone)
    return "Contact updated."


@input_error
def show_phone(args: list[str], book: AddressBook) -> str:
    check_args(args, 1, "phone <name>")

    record = get_record(book, args[0])
    phones = "; ".join(p.value for p in record.phones)
    return f"{record.name.value}: {phones}"


@input_error
def show_all(args: list[str], book: AddressBook) -> str:
    check_args(args, 0, "all")

    if not book:
        return "No contacts."
    return "\n".join(str(record) for record in book.values())


@input_error
def add_birthday(args: list[str], book: AddressBook) -> str:
    check_args(args, 2, "add-birthday <name> <DD.MM.YYYY>")

    name, birthday = args
    record = get_record(book, name)
    message = "Birthday updated." if record.birthday else "Birthday added."
    record.add_birthday(birthday)
    return message


@input_error
def show_birthday(args: list[str], book: AddressBook) -> str:
    check_args(args, 1, "show-birthday <name>")

    record = get_record(book, args[0])
    if record.birthday is None:
        return "Birthday not specified."
    return f"{record.name.value}: {record.birthday}"


@input_error
def birthdays(args: list[str], book: AddressBook) -> str:
    check_args(args, 0, "birthdays")

    upcoming = book.get_upcoming_birthdays()
    if not upcoming:
        return "No upcoming birthdays."
    return "\n".join(
        f"{user['name']}: {user['congratulation_date']}" for user in upcoming
    )
