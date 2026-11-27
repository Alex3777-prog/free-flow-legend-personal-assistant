from .utils import input_error, check_args
from .notes import Note, NoteBook



def get_note(raw_id: str, notebook: NoteBook) -> Note:
    note_id = NoteBook.parse_note_id(raw_id)
    note = notebook.find(note_id)
    if note is None:
        raise ValueError(f"Note with ID {note_id} not found.")
    return note


@input_error
def add_note(args: list[str], notebook: NoteBook) -> str:
    if not args:
        raise ValueError("Note text cannot be empty.")
    note_text = " ".join(args)
    note = notebook.add_note(note_text)
    return f"Note added ID: {note.id}."


@input_error
def show_note(args: list[str], notebook: NoteBook) -> str:
    check_args(args, 1, "show-note <id>")
    note = get_note(args[0], notebook)
    return format_notes([note])


@input_error
def edit_note(args: list[str], notebook: NoteBook) -> str:
    if len(args) < 2:
        raise ValueError("Invalid arguments. Usage: edit-note <id> <new_text>")
    note = get_note(args[0], notebook)
    new_text = " ".join(args[1:])
    note.edit_text(new_text)
    return f"Note {note.id} updated."


@input_error
def delete_note(args: list[str], notebook: NoteBook) -> str:
    check_args(args, 1, "delete-note <id>")
    note_id = NoteBook.parse_note_id(args[0])
    notebook.delete(note_id)
    return f"Note {note_id} deleted."


@input_error
def show_all_notes(args: list[str], notebook: NoteBook) -> str:
    check_args(args, 0, "all-notes")
    if not notebook:
        return "Notebook is empty."
    return format_notes(list(notebook.values()))


@input_error
def search_notes(args: list[str], notebook: NoteBook) -> str:
    if not args:
        raise ValueError("Usage: search-notes <query>.")
    query = " ".join(args)
    results = notebook.search_by_text(query)
    if not results:
        return "No notes found."
    else:
        return format_notes(results)



@input_error
def add_tag(args: list[str], notebook: NoteBook) -> str:
    check_args(args, 2, "add-tag <id> <tag>")
    note = get_note(args[0], notebook)
    note.add_tag(args[1])
    return "Tag added."


@input_error
def remove_tag(args: list[str], notebook: NoteBook) -> str:
    check_args(args, 2, "remove-tag <id> <tag>")
    note = get_note(args[0], notebook)
    note.remove_tag(args[1])
    return "Tag removed."


@input_error
def search_by_tag(args: list[str], notebook: NoteBook) -> str:
    check_args(args, 1, "search-tag <tag>")
    results = notebook.search_by_tag(args[0])
    if not results:
        return "No notes found with this tag."
    else:
        return format_notes(results)


@input_error
def sort_notes_by_tag(args: list[str], notebook: NoteBook) -> str:
    check_args(args, 0, "sort-notes")
    if not notebook:
        return "Notebook is empty."
    else:
        return format_notes(notebook.sort_by_tags())



def format_notes(notes: list[Note]) -> str:
    return "\n".join(str(note) for note in notes)