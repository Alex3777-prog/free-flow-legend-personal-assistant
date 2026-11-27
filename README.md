# Free Flow Personal Assistant

A modular Python command-line application for managing contacts, phone numbers, birthdays, and personal notes. The application helps users organize personal information, search and update records, and keep their data between sessions.

## Project Overview

Free Flow Personal Assistant is a command-line tool that combines contact management and note-taking functionality in one application. Users can create and update contacts, manage phone numbers, emails, addresses, and birthdays, create notes, organize them with tags, and search stored information. Lists of contacts and notes are displayed as tables.

The application is built with Python and uses object-oriented programming to organize its data and functionality into separate modules.

## Features

### Contact Management

- Add new contacts. Names can contain spaces, for example `Alex Smith`.
- Add multiple phone numbers to a contact, change or remove a phone number.
- Add, change, display, and remove a contact's email and address.
- Add, display, and remove a contact's birthday.
- Search contacts by name, phone number, email, or address.
- Rename and delete contacts.
- Display all saved contacts as a table.
- View upcoming birthdays within the next N days (7 by default).

### Notes Management

- Create, view, edit, and delete notes.
- Display all saved notes as a table.
- Search notes by text.
- Add and remove tags.
- Search notes by tag.
- Sort notes by tags.

Tags are case-insensitive, and the `#` prefix is optional: `#Python`, `python`, and `PYTHON` are the same tag. A tag is a single word made of letters, digits, `_`, and `-`.

### Data Validation and Error Handling

- Phone numbers must contain exactly 10 digits.
- Emails must have a valid format, for example `user@example.com`.
- Birthdays use the `DD.MM.YYYY` format and cannot be in the future.
- Check command arguments and handle invalid commands.
- Display meaningful error messages when an operation cannot be completed.

### Data Persistence

- Save contacts and notes automatically after every command.
- Load previously saved data when the application starts.
- Store the contact book and notebook together in a single file.
- Use a temporary file and file replacement when saving data to help protect existing data from incomplete writes.

## Technologies Used

- **Python** — application programming language.
- **Object-Oriented Programming (OOP)** — organization of data models and application functionality.
- **Python Standard Library** — built-in modules for file handling, data serialization, and other operations.
- **Pickle** — serialization and deserialization of application data.
- **pathlib** — cross-platform file path handling.
- **Rich** — tables in the terminal.

## Requirements

- Python 3.10 or later.
- Git — required to clone the repository.
- The `rich` package, installed from `requirements.txt` (see step 6 below).

## Installation and Setup

**1. Clone the repository**

```bash
git clone https://github.com/Alex3777-prog/free-flow-legend-personal-assistant.git
```

**2. Navigate to the project directory**

```bash
cd free-flow-legend-personal-assistant
```

**3. Check your Python installation**

Windows:

```powershell
py --version
```

macOS / Linux:

```bash
python3 --version
```

Python 3.10 or later is required.

**4. Create a virtual environment**

Windows:

```powershell
py -m venv .venv
```

macOS / Linux:

```bash
python3 -m venv .venv
```

**5. Activate the virtual environment**

Windows — PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

Windows — Command Prompt:

```cmd
.venv\Scripts\activate.bat
```

macOS / Linux:

```bash
source .venv/bin/activate
```

After activation, use `python` to run commands inside the virtual environment on all three operating systems.

**6. Install the dependencies**

```bash
pip install -r requirements.txt
```

Do not skip this step: without it, the application stops at startup with `ModuleNotFoundError: No module named 'rich'`.

## Running the Application

Make sure the virtual environment is activated and the terminal is in the project root directory. Activate it again in every new terminal window.

Run the application:

```bash
python -m assistant.main
```

The application starts in the terminal and displays a welcome message. Enter commands at the prompt to interact with the assistant.

To display the available commands, enter:

```text
help
```

## CLI Commands

### General Commands

| Command | Description |
|---|---|
| `hello` | Display a greeting |
| `help` | Display the list of available commands |
| `exit` | Save data and exit the application |
| `close` | Save data and exit the application |

Commands are case-insensitive. Names can contain spaces and are not case-sensitive: `phone alex smith` finds `Alex Smith`.

### Contact Commands

| Command | Description |
|---|---|
| `add <name> <phone>` | Add a new contact or an additional phone number |
| `change <name> <old> <new>` | Replace an existing phone number |
| `remove-phone <name> <phone>` | Remove a phone number |
| `phone <name>` | Display a contact's phone numbers |
| `all` | Display all contacts |
| `search-contact <query>` | Search contacts by name, phone, email, or address |
| `rename-contact <name>` | Rename a contact (asks for the new name) |
| `delete-contact <name>` | Delete a contact |

### Birthday Commands

| Command | Description |
|---|---|
| `add-birthday <name> <DD.MM.YYYY>` | Add or update a contact's birthday |
| `show-birthday <name>` | Display a contact's birthday |
| `remove-birthday <name>` | Remove a contact's birthday |
| `birthdays [days]` | Display birthdays in the next N days (default 7) |

### Email Commands

| Command | Description |
|---|---|
| `add-email <name> <email>` | Add or update a contact's email |
| `change-email <name> <email>` | Change an existing email |
| `show-email <name>` | Display a contact's email |
| `remove-email <name>` | Remove a contact's email |

### Address Commands

| Command | Description |
|---|---|
| `add-address <name>` | Add or update a contact's address (asks for it) |
| `change-address <name>` | Change an existing address (asks for it) |
| `show-address <name>` | Display a contact's address |
| `remove-address <name>` | Remove a contact's address |

The address and the new name are entered on a separate line, because they can contain spaces.

### Notes Commands

| Command | Description |
|---|---|
| `add-note <text>` | Create a new note |
| `show-note <id>` | Display a note by its ID |
| `edit-note <id> <text>` | Replace a note's text |
| `delete-note <id>` | Delete a note |
| `all-notes` | Display all notes |
| `search-notes <query>` | Search notes by text |
| `add-tag <id> <tag>` | Add a tag to a note |
| `remove-tag <id> <tag>` | Remove a tag from a note |
| `search-tag <tag>` | Search notes by tag |
| `sort-notes` | Display notes sorted by tags |

## Usage Examples

### Managing Contacts

```text
add Alex Smith 0123456789
add Alex Smith 0987654321
phone Alex Smith
change Alex Smith 0123456789 0111222333
add-birthday Alex Smith 15.06.2004
add-email Alex Smith alex@example.com
search-contact example.com
birthdays 14
all
```

Commands that need text with spaces ask for it on the next line:

```text
Enter a command: add-address Alex Smith
Address: Kyiv, Khreshchatyk 1
Address added.
```

### Managing Notes

```text
add-note Prepare the Python project
add-note Buy milk tomorrow
add-tag 1 study
add-tag 1 python
all-notes
show-note 1
search-notes Python
search-tag study
edit-note 1 Complete the Python project
sort-notes
delete-note 1
```

Note IDs are assigned automatically when notes are created and are not reused after a note is deleted.

Lists are displayed as tables, for example `all-notes`:

```text
╭────┬────────────────────────────┬────────────────╮
│ ID │ Text                       │ Tags           │
├────┼────────────────────────────┼────────────────┤
│ 1  │ Prepare the Python project │ #study #python │
├────┼────────────────────────────┼────────────────┤
│ 2  │ Buy milk tomorrow          │ -              │
╰────┴────────────────────────────┴────────────────╯
```

## Data Storage

The application stores its data in the user's home directory, inside the `.personal_assistant` folder.

The storage file is named `data.pkl`.

The storage location is resolved using the user's home directory, so it works across Windows, macOS, and Linux.

Both the contact book and the notebook are stored together. When the application starts, previously saved data is loaded automatically. If the storage file does not exist, the application starts with empty contact and note collections.

Data is saved automatically after every command, so nothing is lost even if the terminal window is closed. If saving fails, for example because of missing write permissions, the application shows a message and tries again on exit. If the storage file is damaged, the application shows an error and exits without overwriting the file.

Data is serialized using Python's `pickle` module. The storage file is intended for use by this application and should only be loaded from trusted local sources.

## Project Structure

```text
free-flow-legend-personal-assistant/
│
├── assistant/
│   ├── __init__.py
│   ├── contacts.py
│   ├── fields.py
│   ├── notes.py
│   ├── contact_commands.py
│   ├── note_commands.py
│   ├── storage.py
│   ├── utils.py
│   └── main.py
│
├── README.md
├── requirements.txt
└── .gitignore
```

### Module Overview

| Module | Description |
|---|---|
| `contacts.py` | Contact records and address book functionality |
| `fields.py` | Data fields and input validation |
| `notes.py` | Note and notebook models |
| `contact_commands.py` | Command handlers and tables for contact management |
| `note_commands.py` | Command handlers and tables for note management |
| `storage.py` | Saving and loading contacts and notes |
| `utils.py` | Input parsing, argument checking, error handling, interactive prompts, and table rendering |
| `main.py` | Application entry point and main command loop |
| `__init__.py` | Python package initialization |

## Exiting the Application

Use `exit` or `close` to finish the session. Data is also saved after every command, so closing the terminal window does not lose it.

You can also use:

- **Ctrl+C** to cancel an active command, for example while the application asks for an address. At the main prompt, it exits the application.
- **Ctrl+D** (macOS / Linux) to exit the application, both at the main prompt and while a command is waiting for input.
- **Ctrl+Z**, followed by Enter (Windows), works the same way as Ctrl+D.