# Python Lab 3: Library Management System

## Overview
This project implements a simple command-line based Library Inventory Management System. It allows users to manage a collection of books, including adding new books, issuing them, returning them, and searching the catalog.

## Features
- **Book Management**: Add new books with title, author, and ISBN.
- **Issue/Return**: Track book status (available vs. issued) and prevent double issuing or returning.
- **Search**: Search for books by Title or ISBN.
- **Persistence**: Data is saved to a JSON file (`data/books.json`) so the inventory is preserved between runs.
- **CLI Interface**: A menu-driven interface for easy interaction.

## Project Structure
- `Library_app.py`: The main application script containing the `Book` class, `LibraryInventory` class, and the CLI loop.
- `data/`: Directory where the `books.json` database is stored.

## How to Run
1.  Navigate to the project directory.
2.  Run the script using Python:
    ```bash
    python Library_app.py
    ```
3.  Follow the on-screen menu options to manage the library.

## Classes
- **Book**: Represents a single book with attributes like title, author, ISBN, and status.
- **LibraryInventory**: Manages the collection of books, handles loading/saving to JSON, and performs search operations.

