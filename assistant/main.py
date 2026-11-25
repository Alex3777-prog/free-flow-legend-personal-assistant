from .utils import parse_input
from .storage import save_data, load_data
from .contact_commands import (
    add_contact,
    change_contact,
    show_phone,
    show_all,
    add_birthday,
    show_birthday,
    birthdays,
)


def main() -> None:
    book = load_data()
    print("Welcome to the assistant bot!")

    try:
        while True:
            try:
                user_input = input("Enter a command: ")
            except (EOFError, KeyboardInterrupt):
                print("\nGood bye!")
                break

            command, *args = parse_input(user_input)

            if command in ("close", "exit"):
                print("Good bye!")
                break
            elif command == "hello":
                print("How can I help you?")
            elif command == "add":
                print(add_contact(args, book))
            elif command == "change":
                print(change_contact(args, book))
            elif command == "phone":
                print(show_phone(args, book))
            elif command == "all":
                print(show_all(args, book))
            elif command == "add-birthday":
                print(add_birthday(args, book))
            elif command == "show-birthday":
                print(show_birthday(args, book))
            elif command == "birthdays":
                print(birthdays(args, book))
            else:
                print("Invalid command.")
    finally:
        # Persist the address book on exit, including exception-driven exits.
        save_data(book)


if __name__ == "__main__":
    main()
