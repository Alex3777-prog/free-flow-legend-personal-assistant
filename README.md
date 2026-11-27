# Free Flow Personal Assistant

A modular Python command-line application for managing contacts, phone numbers, birthdays, and personal notes. The application helps users organize personal information, search and update records, and keep their data between sessions.

## Project Overview

Free Flow Personal Assistant is a command-line tool that combines contact management and note-taking functionality in one application. Users can create and update contacts, manage phone numbers and birthdays, create notes, organize them with tags, and search stored information.

The application is built with Python and uses object-oriented programming to organize its data and functionality into separate modules.

## Features

### Contact Management

- Add new contacts.
- Add multiple phone numbers to an existing contact.
- Change an existing phone number.
- Search for a contact and display their phone numbers.
- Display all saved contacts.
- Add or update a contact's birthday.
- Display a contact's birthday.
- View upcoming birthdays within the next 7 days.

### Notes Management

- Create, edit, and delete notes.
- Display all saved notes.
- Search notes by text.
- Add and remove tags.
- Search notes by tag.
- Sort notes by tags.

### Data Validation and Error Handling

- Validate user input and contact fields.
- Check command arguments.
- Handle invalid commands and incorrect input.
- Display meaningful error messages when an operation cannot be completed.

### Data Persistence

- Save contacts and notes locally.
- Load previously saved data when the application starts.
- Store the contact book and notebook together in a single file.
- Use a temporary file and file replacement when saving data to help protect existing data from incomplete writes.

## Technologies Used

- **Python** — application programming language.
- **Object-Oriented Programming (OOP)** — organization of data models and application functionality.
- **Python Standard Library** — built-in modules for file handling, data serialization, and other operations.
- **Pickle** — serialization and deserialization of application data.
- **pathlib** — cross-platform file path handling.

## Requirements

- Python 3.9 or later.
- Git — required to clone the repository.

No third-party Python packages are required.

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

Python 3.9 or later is required.

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

## Running the Application

Make sure the virtual environment is activated and the terminal is in the project root directory.

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

### Contact Commands

| Command | Description |
|---|---|
| `add <name> <phone>` | Add a new contact or an additional phone number |
| `change <name> <old_phone> <new_phone>` | Replace an existing phone number |
| `phone <name>` | Display a contact's phone numbers |
| `all` | Display all contacts |
| `add-birthday <name> <DD.MM.YYYY>` | Add or update a contact's birthday |
| `show-birthday <name>` | Display a contact's birthday |
| `birthdays` | Display birthdays in the next 7 days |

### Notes Commands

| Command | Description |
|---|---|
| `add-note <text>` | Create a new note |
| `edit-note <id> <new_text>` | Edit an existing note |
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
add Alex 0123456789
add Alex 0987654321
phone Alex
change Alex 0123456789 0111222333
add-birthday Alex 15.06.2004
show-birthday Alex
birthdays
all
```

### Managing Notes

```text
add-note Prepare the Python project
add-tag 1 study
add-tag 1 python
all-notes
search-notes Python
search-tag study
edit-note 1 Complete the Python project
sort-notes
delete-note 1
```

Note IDs are assigned automatically when notes are created.

## Data Storage

The application stores its data in the user's home directory, inside the `.personal_assistant` folder.

The storage file is named `data.pkl`.

The storage location is resolved using the user's home directory, so it works across Windows, macOS, and Linux.

Both the contact book and the notebook are stored together. When the application starts, previously saved data is loaded automatically. If the storage file does not exist, the application starts with empty contact and note collections.

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
└── .gitignore
```

### Module Overview

| Module | Description |
|---|---|
| `contacts.py` | Contact records and address book functionality |
| `fields.py` | Data fields and input validation |
| `notes.py` | Note and notebook models |
| `contact_commands.py` | Command handlers for contact management |
| `note_commands.py` | Command handlers for note management |
| `storage.py` | Saving and loading contacts and notes |
| `utils.py` | Input parsing, argument checking, and error handling |
| `main.py` | Application entry point and main command loop |
| `__init__.py` | Python package initialization |

## Exiting the Application

Use `exit` or `close` to finish the session. The application saves its data before exiting.

You can also use:

- **Ctrl+C** to cancel an active command. At the main prompt, it exits the application.
- **Ctrl+D** (macOS / Linux) to exit the application from the main prompt.
- **Ctrl+Z**, followed by Enter (Windows Command Prompt), to signal the end of input.