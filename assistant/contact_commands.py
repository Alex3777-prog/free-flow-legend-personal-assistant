from .contacts import AddressBook, Record, UPCOMING_DAYS
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
def remove_phone(args: list[str], book: AddressBook) -> str:
    check_args(args, 2, "remove-phone <name> <phone>")

    name, phone = args
    get_record(book, name).remove_phone(phone)
    return "Phone removed."


@input_error
def show_phone(args: list[str], book: AddressBook) -> str:
    check_args(args, 1, "phone <name>")

    record = get_record(book, args[0])
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
    check_args(args, 1, "delete <name>")

    if not book.delete(args[0]):
        raise KeyError(args[0])
    return "Contact deleted."


@input_error
def rename_contact(args: list[str], book: AddressBook) -> str:
    check_args(args, 2, "rename <old_name> <new_name>")

    old_name, new_name = args
    book.rename_record(old_name, new_name)
    return "Contact renamed."


@input_error
def search_contacts(args: list[str], book: AddressBook) -> str:
    if not args:
        raise ValueError("Invalid number of arguments. Usage: search <query>")

    query = " ".join(args)
    results = book.search(query)
    if not results:
        return "No matching contacts found."
    return "\n".join(str(record) for record in results)


@input_error
def add_birthday(args: list[str], book: AddressBook) -> str:
    check_args(args, 2, "add-birthday <name> <DD.MM.YYYY>")

    name, birthday = args
    record = get_record(book, name)
    message = "Birthday updated." if record.birthday else "Birthday added."
    record.add_birthday(birthday)
    return message


@input_error
def remove_birthday(args: list[str], book: AddressBook) -> str:
    check_args(args, 1, "remove-birthday <name>")

    get_record(book, args[0]).remove_birthday()
    return "Birthday removed."


@input_error
def show_birthday(args: list[str], book: AddressBook) -> str:
    check_args(args, 1, "show-birthday <name>")

    record = get_record(book, args[0])
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
    check_args(args, 2, "add-email <name> <email>")

    name, email = args
    record = get_record(book, name)
    message = "Email updated." if record.email else "Email added."
    record.add_email(email)
    return message


@input_error
def change_email(args: list[str], book: AddressBook) -> str:
    check_args(args, 2, "change-email <name> <new_email>")

    name, new_email = args
    record = get_record(book, name)
    if record.email is None:
        raise ValueError("Email is not specified. Use 'add-email' first.")
    record.edit_email(new_email)
    return "Email updated."


@input_error
def remove_email(args: list[str], book: AddressBook) -> str:
    check_args(args, 1, "remove-email <name>")

    get_record(book, args[0]).remove_email()
    return "Email removed."


@input_error
def show_email(args: list[str], book: AddressBook) -> str:
    check_args(args, 1, "show-email <name>")

    record = get_record(book, args[0])
    if record.email is None:
        return "Email not specified."
    return f"{record.name.value}: {record.email}"


@input_error
def add_address(args: list[str], book: AddressBook) -> str:
    if len(args) < 2:
        raise ValueError("Invalid number of arguments. Usage: add-address <name> <address>")

    name = args[0]
    address = " ".join(args[1:])
    record = get_record(book, name)
    message = "Address updated." if record.address else "Address added."
    record.add_address(address)
    return message


@input_error
def change_address(args: list[str], book: AddressBook) -> str:
    if len(args) < 2:
        raise ValueError("Invalid number of arguments. Usage: change-address <name> <new_address>")

    name = args[0]
    new_address = " ".join(args[1:])
    record = get_record(book, name)
    if record.address is None:
        raise ValueError("Address is not specified. Use 'add-address' first.")
    record.edit_address(new_address)
    return "Address updated."


@input_error
def remove_address(args: list[str], book: AddressBook) -> str:
    check_args(args, 1, "remove-address <name>")

    get_record(book, args[0]).remove_address()
    return "Address removed."


@input_error
def show_address(args: list[str], book: AddressBook) -> str:
    check_args(args, 1, "show-address <name>")

    record = get_record(book, args[0])
    if record.address is None:
        return "Address not specified."
    return f"{record.name.value}: {record.address}"
