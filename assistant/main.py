from .utils import parse_input
from .storage import save_data, load_data
from .contacts import AddressBook
from .contact_commands import (
    add_contact,
    change_contact,
    remove_phone,
    show_phone,
    show_all,
    search_contacts,
    rename_contact,
    delete_contact,
    add_birthday,
    show_birthday,
    remove_birthday,
    birthdays,
    add_email,
    change_email,
    show_email,
    remove_email,
    add_address,
    change_address,
    show_address,
    remove_address,
)


EXIT_COMMANDS = ("exit", "close")

HELP_TEXT = """\
General:
  hello                               Greet the assistant
  help                                Show this help
  exit | close                        Save data and exit

Contacts:
  add <name> <phone>                  Add a contact or a new phone to it
  change <name> <old> <new>           Replace a phone number
  remove-phone <name> <phone>         Remove a phone number
  phone <name>                        Show contact's phones
  all                                 Show all contacts
  search-contact <query>              Search by name, phone, email or address
  rename-contact <name>               Rename a contact (asks for the new name)
  delete-contact <name>               Delete a contact

Birthdays:
  add-birthday <name> <DD.MM.YYYY>    Add or update a birthday
  show-birthday <name>                Show contact's birthday
  remove-birthday <name>              Remove a birthday
  birthdays [days]                    Birthdays in the next N days (default 7)

Email:
  add-email <name> <email>            Add or update an email
  change-email <name> <email>         Change an existing email
  show-email <name>                   Show contact's email
  remove-email <name>                 Remove an email

Address:
  add-address <name>                  Add or update an address (asks for it)
  change-address <name>               Change an existing address (asks for it)
  show-address <name>                 Show contact's address
  remove-address <name>               Remove an address

Names can contain spaces. Examples:
  add Alex Smith 0123456789
  add-birthday Alex Smith 15.06.2004
  add-address Alex Smith
  birthdays 14

Ctrl+C cancels an active command or exits at the main prompt.
Ctrl+D exits the application."""

GENERAL_COMMANDS = {
    "hello": lambda: "How can I help you?",
    "help": lambda: HELP_TEXT,
}

CONTACT_COMMANDS = {
    "add": add_contact,
    "change": change_contact,
    "remove-phone": remove_phone,
    "phone": show_phone,
    "all": show_all,
    "search-contact": search_contacts,
    "rename-contact": rename_contact,
    "delete-contact": delete_contact,
    "add-birthday": add_birthday,
    "show-birthday": show_birthday,
    "remove-birthday": remove_birthday,
    "birthdays": birthdays,
    "add-email": add_email,
    "change-email": change_email,
    "show-email": show_email,
    "remove-email": remove_email,
    "add-address": add_address,
    "change-address": change_address,
    "show-address": show_address,
    "remove-address": remove_address,
}


def execute(command: str, args: list[str], book: AddressBook) -> str:
    """Route a command to its handler and return the text to print."""
    if command in GENERAL_COMMANDS:
        return GENERAL_COMMANDS[command]()
    if command in CONTACT_COMMANDS:
        return CONTACT_COMMANDS[command](args, book)
    return "Invalid command. Type 'help' to see available commands."


def main() -> None:
    try:
        book = load_data()
    except Exception as error:
        # Abort without saving so a damaged file is not overwritten.
        print(f"Failed to load data: {error}")
        return

    print("Welcome to the assistant bot!")

    try:
        while True:
            try:
                user_input = input("Enter a command: ")
            except (KeyboardInterrupt, EOFError):
                print("\nGood bye!")
                break

            command, *args = parse_input(user_input)

            if not command:
                continue
            if command in EXIT_COMMANDS:
                print("Good bye!")
                break

            try:
                print(execute(command, args, book))
            except KeyboardInterrupt:
                print("\nOperation cancelled.")
            except EOFError:
                print("\nGood bye!")
                break
    finally:
        # Persist the address book on exit, including exception-driven exits.
        try:
            save_data(book)
        except OSError as error:
            print(f"Failed to save data: {error}")


if __name__ == "__main__":
    main()
