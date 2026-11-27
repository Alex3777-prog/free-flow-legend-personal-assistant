"""Notebook: the Note class and the NoteBook that stores notes by ID."""

from __future__ import annotations

import re
from collections import UserDict


class Note:
    """A text note with a numeric ID and a list of tags.

    Tags are stored in lowercase without the leading "#".
    """

    def __init__(self, note_id: int, text: str):
        """Create a note; raise ValueError if the text is empty."""
        self.text = text.strip()
        self.id = note_id
        self.tags: list[str] = []
        if not self.text:
            raise ValueError("Note text cannot be empty.")

    def edit_text(self, new_text: str):
        """Replace the note text; raise ValueError if it is empty."""
        if not new_text.strip():
            raise ValueError("Note text cannot be empty.")
        self.text = new_text.strip()

    def add_tag(self, tag: str):
        """Add a tag; raise ValueError if the note already has it."""
        normalized_tag = self.normalize_tag(tag)
        if normalized_tag in self.tags:
            raise ValueError("This tag is already assigned to the note.")
        else:
            self.tags.append(normalized_tag)

    def remove_tag(self, tag: str):
        """Remove a tag; raise ValueError if the note does not have it."""
        normalized_tag = self.normalize_tag(tag)
        if normalized_tag in self.tags:
            self.tags.remove(normalized_tag)
        else:
            raise ValueError("Tag not found.")

    @staticmethod
    def normalize_tag(tag: str) -> str:
        """Return the tag in lowercase without "#", or raise ValueError.

        A tag must be one word made of letters, digits, "_", and "-".
        """
        normalized_tag = tag.strip().lstrip("#").strip().lower()
        if not normalized_tag:
            raise ValueError("Tag cannot be empty.")
        if not re.fullmatch(r"[\w-]+", normalized_tag):
            raise ValueError(
                "Tag can contain only letters, digits, underscores, "
                "and hyphens."
            )
        return normalized_tag

    def __str__(self):
        """Return the note and its tags as one line of text."""
        if not self.tags:
            return f"ID: {self.id} {self.text}"
        formatted_tags = " ".join(f"#{tag}" for tag in self.tags)
        return f"ID: {self.id} {self.text} | Tags: {formatted_tags}"


class NoteBook(UserDict):
    """All notes, keyed by ID. IDs only grow and are never reused."""

    def __init__(self):
        """Create an empty notebook; the first note gets ID 1."""
        super().__init__()
        self.next_id = 1

    def add_note(self, text: str) -> Note:
        """Create a note with the next free ID and return it."""
        note = Note(self.next_id, text)
        self.data[note.id] = note
        self.next_id += 1
        return note

    def find(self, note_id: int) -> Note | None:
        """Return the note with this ID, or None."""
        return self.data.get(note_id)

    def delete(self, note_id: int):
        """Delete a note by ID; raise ValueError if it does not exist."""
        if note_id not in self.data:
            raise ValueError(f"Note with ID {note_id} not found.")
        del self.data[note_id]

    def search_by_text(self, query: str) -> list[Note]:
        """Return notes whose text contains query, ignoring letter case."""
        cleaned_query = query.strip().lower()
        if not cleaned_query:
            raise ValueError("Search query cannot be empty.")
        return [
            note for note in self.data.values()
            if cleaned_query in note.text.lower()
        ]

    def search_by_tag(self, tag: str) -> list[Note]:
        """Return notes that have exactly this tag."""
        normalized_tag = Note.normalize_tag(tag)
        return [
            note for note in self.data.values()
            if normalized_tag in note.tags
        ]

    def sort_by_tags(self) -> list[Note]:
        """Return notes sorted by their tags; notes without tags go last."""
        return sorted(
            self.data.values(),
            key=lambda note: (not note.tags, sorted(note.tags), note.id)
        )

    @staticmethod
    def parse_note_id(raw_id: str) -> int:
        """Convert raw_id to a positive int or raise ValueError."""
        try:
            parsed_id = int(raw_id)
        except ValueError:
            raise ValueError("Note ID must be a positive number.") from None
        if parsed_id < 1:
            raise ValueError("Note ID must be a positive number.")
        return parsed_id
