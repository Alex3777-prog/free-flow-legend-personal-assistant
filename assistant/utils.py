from collections.abc import Callable
from functools import wraps


def input_error(func):
    @wraps(func)
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError as error:
            return str(error)
        except IndexError:
            return "Enter user name."
        except KeyError:
            return "Contact not found."

    return inner


def parse_input(user_input: str) -> tuple[str, ...]:
    parts = user_input.split()
    if not parts:
        return ("",)
    command, *args = parts
    return command.lower(), *args


def check_args(args: list[str], expected: int, usage: str) -> None:
    """Raise ValueError unless exactly `expected` arguments were given."""
    if len(args) != expected:
        raise ValueError(f"Invalid number of arguments. Usage: {usage}")


def ask(
    label: str,
    validator: Callable[[str], object] | None = None,
    required: bool = False,
) -> str:
    """Prompt until the user enters a valid value.

    Empty input returns "" for optional fields and is asked again for required
    ones. The validator must raise ValueError for invalid input; its return
    value is ignored. KeyboardInterrupt and EOFError propagate to the caller.
    """
    while True:
        value = input(f"{label}: ").strip()

        if not value:
            if not required:
                return ""
            print("This field is required.")
            continue

        if validator is not None:
            try:
                validator(value)
            except ValueError as error:
                print(error)
                continue

        return value
