# Game Library

A command-line application for managing a personal video game library, built with Python, SQLite, and SQLAlchemy.

This project is part of my practical learning journey in Python, object-oriented programming, relational databases, and software development.

The application currently supports adding games, viewing a game library, and searching for games. Game data is stored persistently in a local SQLite database.

## Features

- Add games to a personal library
- View all stored games
- Search games by name
- Case-insensitive partial-name searching
- Validate game names, release dates, and ratings
- Store game information in an SQLite database
- Enforce rating constraints at the database level

## Technologies

- Python 3.14
- SQLite
- SQLAlchemy 2.x
- Git

## Project Structure

```text
game-library/
├── main.py              # CLI entry point and user interaction
├── game.py              # SQLAlchemy Game model
├── game_library.py      # Game management and database operations
├── database.py          # Database engine and session configuration
├── requirements.txt     # Project dependencies
├── .gitignore           # Files excluded from version control
└── README.md
```

The local SQLite database (`game_library.db`) is generated automatically when the application starts.

## Database Design

The application currently uses a single database model: `Game`.

| Column | Type | Description |
|---|---|---|
| id | Integer | Primary key |
| name | String(200) | Game name |
| release_date | String(10) | Release date (YYYY-MM-DD) |
| rating | Integer | Rating between 1 and 10 |

The model uses SQLAlchemy's declarative ORM syntax with `Mapped` and `mapped_column`.

A database-level `CheckConstraint` ensures that ratings remain between 1 and 10.

## Getting Started

### Requirements

- Python 3.14 or compatible Python version
- pip

### 1. Clone the repository

```bash
git clone <repository-url>
cd game-library
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

### 3. Activate the virtual environment

Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

### 4. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 5. Run the application

```bash
python main.py
```

The application automatically creates the required database tables if they do not already exist.

## Usage

The application provides a simple interactive menu:

```text
========== GAME LIBRARY ==========
1. Add game
2. View games
3. Search games
4. Exit
```

When adding a game, the application asks for:

- Game name
- Release date (YYYY-MM-DD)
- Personal rating (1–10)

Games are saved to the SQLite database and remain available after restarting the application.

## Current Development Status

The project is currently in the early database-backed development stage.

**Implemented:**
- Initial object-oriented application structure
- SQLAlchemy Game model
- SQLite database configuration
- Database table initialization
- Database-backed game insertion
- Database-backed game retrieval
- Partial-name searching
- Input validation for game names, dates, and ratings
- Database-level rating constraint

**Planned:**
- Individual game details
- Updating and deleting games
- Displaying database IDs
- Automated testing with pytest
- Improved database error handling
- Expanded relational database design
- Library statistics

## Roadmap

The project is being developed incrementally, with an emphasis on understanding the technologies and keeping the implementation maintainable.

Future development will focus on:

1. Completing database-backed CRUD functionality.
2. Improving input validation and error handling.
3. Introducing automated tests with pytest.
4. Expanding the database with related entities such as developers, genres, and platforms.
5. Adding personal game tracking, including completion status and playtime.
6. Implementing basic library statistics.

## Development Philosophy

The main goal is to build a functional application while developing practical software engineering skills.

Development principles:

- Keep the scope manageable.
- Separate user interaction from application and database logic.
- Use meaningful naming and type hints.
- Introduce abstractions when they solve real problems.
- Test important functionality and edge cases.
- Understand the implementation rather than blindly adopting generated code.

This project prioritizes practical learning, maintainability, and incremental improvement over unnecessary complexity.