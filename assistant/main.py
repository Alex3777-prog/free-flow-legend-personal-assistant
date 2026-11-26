from .utils import parse_input
from .storage import save_data, load_data
from .contacts import AddressBook
from .contact_commands import (
    add_contact,
    change_contact,
    show_phone,
    show_all,
    add_birthday,
    show_birthday,
    birthdays,
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
  phone <name>                        Show contact's phones
  all                                 Show all contacts
  add-birthday <name> <DD.MM.YYYY>    Add or update a birthday
  show-birthday <name>                Show contact's birthday
  birthdays                           Show birthdays in the next 7 days

Examples:
  add Alex 0123456789
  add-birthday Alex 15.06.2004

Ctrl+C cancels an active command or exits at the main prompt.
Ctrl+D exits the application."""

GENERAL_COMMANDS = {
    "hello": lambda: "How can I help you?",
    "help": lambda: HELP_TEXT,
}

CONTACT_COMMANDS = {
    "add": add_contact,
    "change": change_contact,
    "phone": show_phone,
    "all": show_all,
    "add-birthday": add_birthday,
    "show-birthday": show_birthday,
    "birthdays": birthdays,
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
