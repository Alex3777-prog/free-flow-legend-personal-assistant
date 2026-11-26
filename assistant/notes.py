from collections import UserDict

class Note:
    def __init__(self, note_id: int, text: str):
        self.text = text.strip()
        self.id = note_id
        self.tags: list[str] = []
        if not self.text:
            raise ValueError("Note text cannot be empty.")
    
    def edit_text(self, new_text: str):
        if not new_text.strip():
            raise ValueError("Note text cannot be empty.")
        self.text = new_text.strip()

    def add_tag(self, tag: str):
        normalized_tag = self.normalize_tag(tag)
        if not normalized_tag:
            raise ValueError("Tag name cannot be empty.")
        if normalized_tag in self.tags:
            raise ValueError("This tag is already assigned to the note.")
        else:
            self.tags.append(normalized_tag)

    def remove_tag(self, tag: str):
        normalized_tag = self.normalize_tag(tag)
        if not normalized_tag:
            raise ValueError("Tag name cannot be empty.")
        if normalized_tag in self.tags:
            self.tags.remove(normalized_tag)
        else:
            raise ValueError("Tag not found.")

    @staticmethod
    def normalize_tag(tag: str) -> str:
        tag = tag.strip().lstrip("#").strip().lower()
        return tag
    
    def __str__(self):
        if not self.tags:
            return f"ID:{self.id} {self.text}"
        return f"ID:{self.id} {self.text} | Tags: {', '.join(self.tags)}"
        


class NoteBook(UserDict):
    def __init__(self):
        super().__init__()
        self.next_id = 1
    
    def add_note(self, text: str) -> Note:
        note = Note(self.next_id, text)
        self.data[note.id] = note
        self.next_id += 1
        return note

    def find(self, note_id: int) -> Note | None:        #change here
        return self.data.get(note_id)

    def delete(self, note_id: int):
        if note_id not in self.data:
            raise ValueError(f"Note with ID:{note_id} not found.")
        del self.data[note_id]

    def search_by_text(self, query: str) -> list[Note]:
        cleaned_query = query.strip().lower()
        if not cleaned_query:
            raise ValueError("Search query cannot be empty.")
        return [
            note for note in self.data.values()
            if cleaned_query in note.text.lower()
        ]
    
    def search_by_tag(self, tag: str) -> list[Note]:
        normalized_tag = Note.normalize_tag(tag)
        if not normalized_tag:
            raise ValueError("Tag cannot be empty.")
        return [
            note for note in self.data.values()
            if any(normalized_tag in t for t in note.tags)
        ]

    def sort_by_tags(self) -> list[Note]:
        return sorted(
            self.data.values(),
            key=lambda note: (not note.tags, sorted(note.tags), note.id)
        )

    @staticmethod
    def parse_note_id(raw_id: str) -> int:
        try:
            parsed_id = int(raw_id)
        except ValueError:
            raise ValueError("Note ID must be a number")
        return parsed_id