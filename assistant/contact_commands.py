"""Command handlers for contacts.

Each handler takes the command arguments and the AddressBook and returns
the text to show. Names can contain spaces, so a handler takes its other
values from the end of the arguments and the rest is the name.
"""

from rich import box
from rich.table import Table
from rich.text import Text

from .contacts import AddressBook, Record, UPCOMING_DAYS
from .fields import Name, Address
from .utils import input_error, check_args, ask, render


def get_record(book: AddressBook, name: str) -> Record:
    """Return the contact or raise ValueError for input_error to report."""
    record = book.find(name)
    if record is None:
        raise ValueError("Contact not found.")
    return record


def parse_name_and_values(
    args: list[str], trailing_count: int, usage: str
) -> tuple[str, ...]:
    """Split args into a multi-word name and `trailing_count` values.

    Example: ["Alex", "Smith", "0123456789"] with trailing_count=1
    gives ("Alex Smith", "0123456789").
    """
    if len(args) < trailing_count + 1:
        raise ValueError(f"Invalid number of arguments. Usage: {usage}")

    if trailing_count == 0:
        return (" ".join(args),)

    name = " ".join(args[:-trailing_count])
    values = args[-trailing_count:]
    return (name, *values)


@input_error
def add_contact(args: list[str], book: AddressBook) -> str:
    """Add a contact, or add a new phone to an existing one.

    Command: add <name> <phone>
    """
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
    """Replace one of the contact's phone numbers.

    Command: change <name> <old> <new>
    """
    name, old_phone, new_phone = parse_name_and_values(
        args, 2, "change <name> <old> <new>"
    )

    get_record(book, name).edit_phone(old_phone, new_phone)
    return "Contact updated."


@input_error
def remove_phone(args: list[str], book: AddressBook) -> str:
    """Remove a phone number from a contact.

    Command: remove-phone <name> <phone>
    """
    name, phone = parse_name_and_values(args, 1, "remove-phone <name> <phone>")

    get_record(book, name).remove_phone(phone)
    return "Phone removed."


@input_error
def show_phone(args: list[str], book: AddressBook) -> str:
    """Show the contact's phones as a table.

    Command: phone <name>
    """
    (name,) = parse_name_and_values(args, 0, "phone <name>")

    record = get_record(book, name)
    if not record.phones:
        return "No phones specified."
    return format_phones(record)


@input_error
def show_all(args: list[str], book: AddressBook) -> str:
    """Show all contacts as a table.

    Command: all
    """
    check_args(args, 0, "all")

    if not book:
        return "No contacts."
    return format_contacts(list(book.values()))


@input_error
def delete_contact(args: list[str], book: AddressBook) -> str:
    """Delete a contact.

    Command: delete-contact <name>
    """
    (name,) = parse_name_and_values(args, 0, "delete-contact <name>")

    if not book.delete(name):
        raise ValueError("Contact not found.")
    return "Contact deleted."


@input_error
def rename_contact(args: list[str], book: AddressBook) -> str:
    """Ask for a new name and rename the contact.

    Command: rename-contact <name>
    """
    (old_name,) = parse_name_and_values(args, 0, "rename-contact <name>")

    record = get_record(book, old_name)
    new_name = ask("New name", validator=Name, required=True)
    book.rename_record(record.name.value, new_name)
    return "Contact renamed."


@input_error
def search_contacts(args: list[str], book: AddressBook) -> str:
    """Search contacts by name, phone, email, or address.

    Command: search-contact <query>
    """
    if not args:
        raise ValueError(
            "Invalid number of arguments. Usage: search-contact <query>"
        )

    query = " ".join(args)
    results = book.search(query)
    if not results:
        return "No matching contacts found."
    return format_contacts(results)


@input_error
def add_birthday(args: list[str], book: AddressBook) -> str:
    """Add or update the contact's birthday.

    Command: add-birthday <name> <DD.MM.YYYY>
    """
    name, birthday = parse_name_and_values(
        args, 1, "add-birthday <name> <DD.MM.YYYY>"
    )

    record = get_record(book, name)
    message = "Birthday updated." if record.birthday else "Birthday added."
    record.add_birthday(birthday)
    return message


@input_error
def remove_birthday(args: list[str], book: AddressBook) -> str:
    """Remove the contact's birthday.

    Command: remove-birthday <name>
    """
    (name,) = parse_name_and_values(args, 0, "remove-birthday <name>")

    get_record(book, name).remove_birthday()
    return "Birthday removed."


@input_error
def show_birthday(args: list[str], book: AddressBook) -> str:
    """Show the contact's birthday.

    Command: show-birthday <name>
    """
    (name,) = parse_name_and_values(args, 0, "show-birthday <name>")

    record = get_record(book, name)
    if record.birthday is None:
        return "Birthday is not specified."
    return f"{record.name.value}: {record.birthday}"


@input_error
def birthdays(args: list[str], book: AddressBook) -> str:
    """Show birthdays in the next N days (7 by default).

    Command: birthdays [days]
    """
    if len(args) > 1:
        raise ValueError(
            "Invalid number of arguments. Usage: birthdays [days]"
        )

    days = UPCOMING_DAYS
    if len(args) == 1:
        try:
            days = int(args[0])
        except ValueError:
            raise ValueError(
                "Number of days must be a positive integer."
            ) from None

    upcoming = book.get_upcoming_birthdays(days=days)
    if not upcoming:
        unit = "day" if days == 1 else "days"
        return f"No upcoming birthdays in the next {days} {unit}."
    return format_birthdays(upcoming)


@input_error
def add_email(args: list[str], book: AddressBook) -> str:
    """Add or update the contact's email.

    Command: add-email <name> <email>
    """
    name, email = parse_name_and_values(args, 1, "add-email <name> <email>")

    record = get_record(book, name)
    message = "Email updated." if record.email else "Email added."
    record.add_email(email)
    return message


@input_error
def change_email(args: list[str], book: AddressBook) -> str:
    """Change the contact's existing email.

    Command: change-email <name> <email>
    """
    name, new_email = parse_name_and_values(
        args, 1, "change-email <name> <email>"
    )

    record = get_record(book, name)
    if record.email is None:
        raise ValueError("Email is not specified. Use 'add-email' first.")
    record.edit_email(new_email)
    return "Email updated."


@input_error
def remove_email(args: list[str], book: AddressBook) -> str:
    """Remove the contact's email.

    Command: remove-email <name>
    """
    (name,) = parse_name_and_values(args, 0, "remove-email <name>")

    get_record(book, name).remove_email()
    return "Email removed."


@input_error
def show_email(args: list[str], book: AddressBook) -> str:
    """Show the contact's email.

    Command: show-email <name>
    """
    (name,) = parse_name_and_values(args, 0, "show-email <name>")

    record = get_record(book, name)
    if record.email is None:
        return "Email is not specified."
    return f"{record.name.value}: {record.email}"


@input_error
def add_address(args: list[str], book: AddressBook) -> str:
    """Ask for an address and add or update it.

    Command: add-address <name>
    """
    (name,) = parse_name_and_values(args, 0, "add-address <name>")

    record = get_record(book, name)
    address = ask("Address", validator=Address, required=True)
    message = "Address updated." if record.address else "Address added."
    record.add_address(address)
    return message


@input_error
def change_address(args: list[str], book: AddressBook) -> str:
    """Ask for a new address and replace the old one.

    Command: change-address <name>
    """
    (name,) = parse_name_and_values(args, 0, "change-address <name>")

    record = get_record(book, name)
    if record.address is None:
        raise ValueError("Address is not specified. Use 'add-address' first.")
    new_address = ask("Address", validator=Address, required=True)
    record.edit_address(new_address)
    return "Address updated."


@input_error
def remove_address(args: list[str], book: AddressBook) -> str:
    """Remove the contact's address.

    Command: remove-address <name>
    """
    (name,) = parse_name_and_values(args, 0, "remove-address <name>")

    get_record(book, name).remove_address()
    return "Address removed."


@input_error
def show_address(args: list[str], book: AddressBook) -> str:
    """Show the contact's address.

    Command: show-address <name>
    """
    (name,) = parse_name_and_values(args, 0, "show-address <name>")

    record = get_record(book, name)
    if record.address is None:
        return "Address is not specified."
    return f"{record.name.value}: {record.address}"


def format_contacts(records: list[Record]) -> str:
    """Return contacts as a table with one row per contact."""
    table = Table(box=box.ROUNDED, show_lines=True)
    table.add_column("Name", style="bold cyan", overflow="fold")
    table.add_column("Phones", overflow="fold")
    table.add_column("Birthday", overflow="fold")
    table.add_column("Email", overflow="fold")
    table.add_column("Address", overflow="fold")

    for record in records:
        phones = "\n".join(p.value for p in record.phones) or "-"
        birthday = str(record.birthday) if record.birthday else "-"
        email = str(record.email) if record.email else "-"
        address = str(record.address) if record.address else "-"

        # Text() shows user input as is, so "[...]" is not read as markup.
        table.add_row(
            Text(record.name.value),
            Text(phones),
            Text(birthday),
            Text(email),
            Text(address),
        )

    return render(table)


def format_phones(record: Record) -> str:
    """Return the contact's phones as a one-column table titled by name."""
    table = Table(
        title=Text(record.name.value), box=box.ROUNDED, show_lines=True
    )
    table.add_column("Phones", overflow="fold")

    for phone in record.phones:
        table.add_row(Text(phone.value))

    return render(table)


def format_birthdays(upcoming: list[dict[str, str]]) -> str:
    """Return upcoming birthdays as a Name / Birthday table."""
    table = Table(box=box.ROUNDED, show_lines=True)
    table.add_column("Name", style="bold cyan", overflow="fold")
    table.add_column("Birthday", overflow="fold")

    for user in upcoming:
        table.add_row(
            Text(user["name"]),
            Text(user["congratulation_date"]),
        )

    return render(table)
