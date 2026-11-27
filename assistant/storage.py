"""Saving and loading all data (contacts and notes) with pickle.

The data is stored in ~/.personal_assistant/data.pkl. Pickle can run
code from a crafted file, so only load data files you trust.
"""

import pickle
from pathlib import Path

from .contacts import AddressBook
from .notes import NoteBook


STORAGE_DIR = Path.home() / ".personal_assistant"
STORAGE_FILE = STORAGE_DIR / "data.pkl"


def ensure_storage_dir() -> None:
    """Create the storage folder if it does not exist."""
    STORAGE_DIR.mkdir(parents=True, exist_ok=True)


def save_data(book: AddressBook, notebook: NoteBook) -> None:
    """Save both books: write a temporary file, then replace data.pkl."""
    ensure_storage_dir()

    temp_file = STORAGE_DIR / "data.tmp"

    with open(temp_file, "wb") as file:
        pickle.dump((book, notebook), file)

    # Replacing is atomic, so a failed write never damages data.pkl.
    temp_file.replace(STORAGE_FILE)


def load_data() -> tuple[AddressBook, NoteBook]:
    """Load both books, or return empty ones if there is no data file."""
    try:
        with open(STORAGE_FILE, "rb") as file:
            book, notebook = pickle.load(file)
            return book, notebook
    except FileNotFoundError:
        return AddressBook(), NoteBook()
