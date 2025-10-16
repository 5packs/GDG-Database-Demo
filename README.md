# GDG-Database-Demo

A simple Python-based book management system using SQLite database for storing and managing book records.

## Features

- **SQLite Database**: Lightweight database to store book information
- **CRUD Operations**: Create, Read, Update, and Delete books
- **Search Functionality**: Search books by title or author
- **Genre Filtering**: Filter books by genre
- **Sample Data**: Pre-populated with sample book entries for demonstration

## Book Schema

Each book entry contains:
- **ID**: Unique identifier (auto-generated)
- **Title**: Book title
- **Author**: Book author
- **Year**: Publication year
- **ISBN**: International Standard Book Number
- **Genre**: Book genre/category

## Installation

No external dependencies required! This project uses only Python standard library modules.

1. Clone the repository:
```bash
git clone https://github.com/5packs/GDG-Database-Demo.git
cd GDG-Database-Demo
```

2. Run the demo:
```bash
python main.py
```

## Usage

### Running the Demo

The `main.py` script demonstrates all the features of the book management system:

```bash
python main.py
```

This will:
1. Create a SQLite database (`books.db`)
2. Populate it with sample book entries
3. Demonstrate various operations (search, filter, update, etc.)

### Using the BookManager Class

You can also use the `BookManager` class directly in your own scripts:

```python
from book_manager import BookManager

# Create a book manager instance
with BookManager("books.db") as manager:
    
    # Add a new book
    book_id = manager.add_book(
        title="The Hobbit",
        author="J.R.R. Tolkien",
        year=1937,
        isbn="978-0547928227",
        genre="Fantasy"
    )
    
    # Get all books
    all_books = manager.get_all_books()
    for book in all_books:
        print(book)
    
    # Search for books
    results = manager.search_books("Hobbit")
    
    # Get books by genre
    fantasy_books = manager.get_books_by_genre("Fantasy")
    
    # Update a book
    manager.update_book(book_id, year=1938)
    
    # Delete a book
    manager.delete_book(book_id)
```

## Project Structure

```
GDG-Database-Demo/
│
├── book_manager.py    # BookManager class with database operations
├── main.py           # Demo script showcasing the system
├── .gitignore        # Git ignore file (excludes database files)
└── README.md         # This file
```

## Sample Books

The demo includes 10 classic books:
- To Kill a Mockingbird by Harper Lee
- 1984 by George Orwell
- Pride and Prejudice by Jane Austen
- The Great Gatsby by F. Scott Fitzgerald
- One Hundred Years of Solitude by Gabriel García Márquez
- The Catcher in the Rye by J.D. Salinger
- The Hobbit by J.R.R. Tolkien
- Harry Potter and the Philosopher's Stone by J.K. Rowling
- The Lord of the Rings by J.R.R. Tolkien
- Animal Farm by George Orwell

## Features Demonstrated

- ✅ Database creation and table setup
- ✅ Adding books to the database
- ✅ Retrieving all books
- ✅ Searching books by title/author
- ✅ Filtering books by genre
- ✅ Getting specific books by ID
- ✅ Updating book information
- ✅ Context manager support for automatic connection handling

## Requirements

- Python 3.6 or higher
- SQLite (included with Python standard library)

## License

This is a demo project for educational purposes.