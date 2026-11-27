
import pickle
from pathlib import Path

from .contacts import AddressBook
from .notes import NoteBook


STORAGE_DIR = Path.home() / ".personal_assistant"
STORAGE_FILE = STORAGE_DIR / "data.pkl"


def ensure_storage_dir() -> None:
    STORAGE_DIR.mkdir(parents=True, exist_ok=True)


def save_data(book: AddressBook, notebook: NoteBook) -> None:
    ensure_storage_dir()

    temp_file = STORAGE_DIR / "data.tmp"

    with open(temp_file, "wb") as file:
        pickle.dump((book, notebook), file)

    temp_file.replace(STORAGE_FILE)


def load_data() -> tuple[AddressBook, NoteBook]:
    try:
        with open(STORAGE_FILE, "rb") as file:
            book, notebook = pickle.load(file)
            return book, notebook
    except FileNotFoundError:
        return AddressBook(), NoteBook()
