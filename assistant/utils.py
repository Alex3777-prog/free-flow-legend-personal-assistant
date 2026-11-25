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

