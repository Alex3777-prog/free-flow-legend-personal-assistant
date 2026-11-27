"""Command handlers for notes.

Each handler takes the command arguments and the NoteBook and returns
the text to show.
"""

from rich import box
from rich.table import Table
from rich.text import Text

from .notes import Note, NoteBook
from .utils import check_args, input_error, render


def get_note(raw_id: str, notebook: NoteBook) -> Note:
    """Return the note for an ID typed by the user or raise ValueError."""
    note_id = NoteBook.parse_note_id(raw_id)
    note = notebook.find(note_id)
    if note is None:
        raise ValueError(f"Note with ID {note_id} not found.")
    return note


@input_error
def add_note(args: list[str], notebook: NoteBook) -> str:
    """Create a note and report its ID.

    Command: add-note <text>
    """
    if not args:
        raise ValueError("Invalid number of arguments. Usage: add-note <text>")
    note_text = " ".join(args)
    note = notebook.add_note(note_text)
    return f"Note {note.id} added."


@input_error
def show_note(args: list[str], notebook: NoteBook) -> str:
    """Show one note as a table.

    Command: show-note <id>
    """
    check_args(args, 1, "show-note <id>")
    note = get_note(args[0], notebook)
    return format_notes([note])


@input_error
def edit_note(args: list[str], notebook: NoteBook) -> str:
    """Replace the text of a note.

    Command: edit-note <id> <text>
    """
    if len(args) < 2:
        raise ValueError(
            "Invalid number of arguments. Usage: edit-note <id> <text>"
        )
    note = get_note(args[0], notebook)
    new_text = " ".join(args[1:])
    note.edit_text(new_text)
    return f"Note {note.id} updated."


@input_error
def delete_note(args: list[str], notebook: NoteBook) -> str:
    """Delete a note.

    Command: delete-note <id>
    """
    check_args(args, 1, "delete-note <id>")
    note_id = NoteBook.parse_note_id(args[0])
    notebook.delete(note_id)
    return f"Note {note_id} deleted."


@input_error
def show_all_notes(args: list[str], notebook: NoteBook) -> str:
    """Show all notes as a table.

    Command: all-notes
    """
    check_args(args, 0, "all-notes")
    if not notebook:
        return "Notebook is empty."
    return format_notes(list(notebook.values()))


@input_error
def search_notes(args: list[str], notebook: NoteBook) -> str:
    """Show notes whose text contains the query.

    Command: search-notes <query>
    """
    if not args:
        raise ValueError(
            "Invalid number of arguments. Usage: search-notes <query>"
        )
    query = " ".join(args)
    results = notebook.search_by_text(query)
    if not results:
        return "No notes found."
    else:
        return format_notes(results)


@input_error
def add_tag(args: list[str], notebook: NoteBook) -> str:
    """Add a tag to a note.

    Command: add-tag <id> <tag>
    """
    check_args(args, 2, "add-tag <id> <tag>")
    note = get_note(args[0], notebook)
    note.add_tag(args[1])
    return "Tag added."


@input_error
def remove_tag(args: list[str], notebook: NoteBook) -> str:
    """Remove a tag from a note.

    Command: remove-tag <id> <tag>
    """
    check_args(args, 2, "remove-tag <id> <tag>")
    note = get_note(args[0], notebook)
    note.remove_tag(args[1])
    return "Tag removed."


@input_error
def search_by_tag(args: list[str], notebook: NoteBook) -> str:
    """Show notes that have exactly this tag.

    Command: search-tag <tag>
    """
    check_args(args, 1, "search-tag <tag>")
    results = notebook.search_by_tag(args[0])
    if not results:
        return "No notes found with this tag."
    else:
        return format_notes(results)


@input_error
def sort_notes_by_tag(args: list[str], notebook: NoteBook) -> str:
    """Show notes sorted by tags; notes without tags go last.

    Command: sort-notes
    """
    check_args(args, 0, "sort-notes")
    if not notebook:
        return "Notebook is empty."
    else:
        return format_notes(notebook.sort_by_tags())


def format_notes(notes: list[Note]) -> str:
    """Return notes as an ID / Text / Tags table."""
    table = Table(box=box.ROUNDED, show_lines=True)
    table.add_column("ID", style="bold cyan", overflow="fold")
    table.add_column("Text", overflow="fold")
    table.add_column("Tags", style="yellow", overflow="fold")

    for note in notes:
        tags_str = " ".join(f"#{tag}" for tag in note.tags) or "-"
        # Text() shows user input as is, so "[...]" is not read as markup.
        table.add_row(
            Text(str(note.id)),
            Text(note.text),
            Text(tags_str),
        )
    return render(table)
