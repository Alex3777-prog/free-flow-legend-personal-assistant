from .contacts import AddressBook, Record, UPCOMING_DAYS
from .fields import Name, Address
from .utils import input_error, check_args, ask


def get_record(book: AddressBook, name: str) -> Record:
    """Return the contact or raise KeyError for input_error to report."""
    record = book.find(name)
    if record is None:
        raise KeyError(name)
    return record


def parse_name_and_values(
    args: list[str], trailing_count: int, usage: str
) -> tuple[str, ...]:
    """Extract multi-word contact name and `trailing_count` single-token values."""
    if len(args) < trailing_count + 1:
        raise ValueError(f"Invalid number of arguments. Usage: {usage}")

    if trailing_count == 0:
        return (" ".join(args),)

    name = " ".join(args[:-trailing_count])
    values = args[-trailing_count:]
    return (name, *values)


@input_error
def add_contact(args: list[str], book: AddressBook) -> str:
    name, phone = parse_name_and_values(args, 1, "add <name> <phone>")

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
    name, old_phone, new_phone = parse_name_and_values(
        args, 2, "change <name> <old_phone> <new_phone>"
    )

    get_record(book, name).edit_phone(old_phone, new_phone)
    return "Contact updated."


@input_error
def remove_phone(args: list[str], book: AddressBook) -> str:
    name, phone = parse_name_and_values(args, 1, "remove-phone <name> <phone>")

    get_record(book, name).remove_phone(phone)
    return "Phone removed."


@input_error
def show_phone(args: list[str], book: AddressBook) -> str:
    (name,) = parse_name_and_values(args, 0, "phone <name>")

    record = get_record(book, name)
    if not record.phones:
        return "No phones specified."
    phones = "; ".join(p.value for p in record.phones)
    return f"{record.name.value}: {phones}"


@input_error
def show_all(args: list[str], book: AddressBook) -> str:
    check_args(args, 0, "all")

    if not book:
        return "No contacts."
    return "\n".join(str(record) for record in book.values())


@input_error
def delete_contact(args: list[str], book: AddressBook) -> str:
    (name,) = parse_name_and_values(args, 0, "delete-contact <name>")

    if not book.delete(name):
        raise ValueError("Contact not found.")
    return "Contact deleted."


@input_error
def rename_contact(args: list[str], book: AddressBook) -> str:
    (old_name,) = parse_name_and_values(args, 0, "rename-contact <old_name>")

    record = book.find(old_name)
    if record is None:
        raise ValueError("Contact not found.")

    new_name = ask("New name", validator=Name, required=True)
    book.rename_record(record.name.value, new_name)
    return "Contact renamed."


@input_error
def search_contacts(args: list[str], book: AddressBook) -> str:
    if not args:
        raise ValueError("Invalid number of arguments. Usage: search-contact <query>")

    query = " ".join(args)
    results = book.search(query)
    if not results:
        return "No matching contacts found."
    return "\n".join(str(record) for record in results)


@input_error
def add_birthday(args: list[str], book: AddressBook) -> str:
    name, birthday = parse_name_and_values(
        args, 1, "add-birthday <name> <DD.MM.YYYY>"
    )

    record = get_record(book, name)
    message = "Birthday updated." if record.birthday else "Birthday added."
    record.add_birthday(birthday)
    return message


@input_error
def remove_birthday(args: list[str], book: AddressBook) -> str:
    (name,) = parse_name_and_values(args, 0, "remove-birthday <name>")

    get_record(book, name).remove_birthday()
    return "Birthday removed."


@input_error
def show_birthday(args: list[str], book: AddressBook) -> str:
    (name,) = parse_name_and_values(args, 0, "show-birthday <name>")

    record = get_record(book, name)
    if record.birthday is None:
        return "Birthday not specified."
    return f"{record.name.value}: {record.birthday}"


@input_error
def birthdays(args: list[str], book: AddressBook) -> str:
    if len(args) > 1:
        raise ValueError("Invalid number of arguments. Usage: birthdays [days]")

    days = UPCOMING_DAYS
    if len(args) == 1:
        try:
            days = int(args[0])
        except ValueError:
            raise ValueError("Days must be an integer.") from None

    upcoming = book.get_upcoming_birthdays(days=days)
    if not upcoming:
        return f"No upcoming birthdays in the next {days} days."
    return "\n".join(
        f"{user['name']}: {user['congratulation_date']}" for user in upcoming
    )


@input_error
def add_email(args: list[str], book: AddressBook) -> str:
    name, email = parse_name_and_values(args, 1, "add-email <name> <email>")

    record = get_record(book, name)
    message = "Email updated." if record.email else "Email added."
    record.add_email(email)
    return message


@input_error
def change_email(args: list[str], book: AddressBook) -> str:
    name, new_email = parse_name_and_values(args, 1, "change-email <name> <new_email>")

    record = get_record(book, name)
    if record.email is None:
        raise ValueError("Email is not specified. Use 'add-email' first.")
    record.edit_email(new_email)
    return "Email updated."


@input_error
def remove_email(args: list[str], book: AddressBook) -> str:
    (name,) = parse_name_and_values(args, 0, "remove-email <name>")

    get_record(book, name).remove_email()
    return "Email removed."


@input_error
def show_email(args: list[str], book: AddressBook) -> str:
    (name,) = parse_name_and_values(args, 0, "show-email <name>")

    record = get_record(book, name)
    if record.email is None:
        return "Email not specified."
    return f"{record.name.value}: {record.email}"


@input_error
def add_address(args: list[str], book: AddressBook) -> str:
    (name,) = parse_name_and_values(args, 0, "add-address <name>")

    record = get_record(book, name)
    address = ask("Address", validator=Address, required=True)
    message = "Address updated." if record.address else "Address added."
    record.add_address(address)
    return message


@input_error
def change_address(args: list[str], book: AddressBook) -> str:
    (name,) = parse_name_and_values(args, 0, "change-address <name>")

    record = get_record(book, name)
    if record.address is None:
        raise ValueError("Address is not specified. Use 'add-address' first.")
    new_address = ask("Address", validator=Address, required=True)
    record.edit_address(new_address)
    return "Address updated."


@input_error
def remove_address(args: list[str], book: AddressBook) -> str:
    (name,) = parse_name_and_values(args, 0, "remove-address <name>")

    get_record(book, name).remove_address()
    return "Address removed."


@input_error
def show_address(args: list[str], book: AddressBook) -> str:
    (name,) = parse_name_and_values(args, 0, "show-address <name>")

    record = get_record(book, name)
    if record.address is None:
        return "Address not specified."
    return f"{record.name.value}: {record.address}"
