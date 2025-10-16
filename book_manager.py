"""
Book Management System using SQLite
Provides CRUD operations for managing a book database.
"""

import sqlite3
from typing import List, Optional, Tuple


class BookManager:
    """Manages book records in an SQLite database."""
    
    def __init__(self, db_name: str = "books.db"):
        """
        Initialize the BookManager with a database connection.
        
        Args:
            db_name: Name of the SQLite database file
        """
        self.db_name = db_name
        self.conn = None
        self.cursor = None
        self._connect()
        self._create_table()
    
    def _connect(self):
        """Establish connection to the database."""
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()
    
    def _create_table(self):
        """Create the books table if it doesn't exist."""
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS books (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                author TEXT NOT NULL,
                year INTEGER,
                isbn TEXT UNIQUE,
                genre TEXT
            )
        ''')
        self.conn.commit()
    
    def add_book(self, title: str, author: str, year: Optional[int] = None, 
                 isbn: Optional[str] = None, genre: Optional[str] = None) -> int:
        """
        Add a new book to the database.
        
        Args:
            title: Book title
            author: Book author
            year: Publication year
            isbn: ISBN number
            genre: Book genre
            
        Returns:
            The ID of the newly added book
        """
        try:
            self.cursor.execute('''
                INSERT INTO books (title, author, year, isbn, genre)
                VALUES (?, ?, ?, ?, ?)
            ''', (title, author, year, isbn, genre))
            self.conn.commit()
            return self.cursor.lastrowid
        except sqlite3.IntegrityError as e:
            print(f"Error: {e}")
            return -1
    
    def get_all_books(self) -> List[Tuple]:
        """
        Retrieve all books from the database.
        
        Returns:
            List of tuples containing book data
        """
        self.cursor.execute('SELECT * FROM books ORDER BY title')
        return self.cursor.fetchall()
    
    def get_book_by_id(self, book_id: int) -> Optional[Tuple]:
        """
        Retrieve a specific book by ID.
        
        Args:
            book_id: The ID of the book to retrieve
            
        Returns:
            Tuple containing book data or None if not found
        """
        self.cursor.execute('SELECT * FROM books WHERE id = ?', (book_id,))
        return self.cursor.fetchone()
    
    def search_books(self, search_term: str) -> List[Tuple]:
        """
        Search for books by title or author.
        
        Args:
            search_term: Search term to match against title or author
            
        Returns:
            List of tuples containing matching book data
        """
        search_pattern = f"%{search_term}%"
        self.cursor.execute('''
            SELECT * FROM books 
            WHERE title LIKE ? OR author LIKE ?
            ORDER BY title
        ''', (search_pattern, search_pattern))
        return self.cursor.fetchall()
    
    def update_book(self, book_id: int, title: Optional[str] = None, 
                    author: Optional[str] = None, year: Optional[int] = None,
                    isbn: Optional[str] = None, genre: Optional[str] = None) -> bool:
        """
        Update a book's information.
        
        Args:
            book_id: ID of the book to update
            title: New title (optional)
            author: New author (optional)
            year: New year (optional)
            isbn: New ISBN (optional)
            genre: New genre (optional)
            
        Returns:
            True if update was successful, False otherwise
        """
        # Get current book data
        current_book = self.get_book_by_id(book_id)
        if not current_book:
            return False
        
        # Use current values if new ones aren't provided
        new_title = title if title is not None else current_book[1]
        new_author = author if author is not None else current_book[2]
        new_year = year if year is not None else current_book[3]
        new_isbn = isbn if isbn is not None else current_book[4]
        new_genre = genre if genre is not None else current_book[5]
        
        try:
            self.cursor.execute('''
                UPDATE books 
                SET title = ?, author = ?, year = ?, isbn = ?, genre = ?
                WHERE id = ?
            ''', (new_title, new_author, new_year, new_isbn, new_genre, book_id))
            self.conn.commit()
            return self.cursor.rowcount > 0
        except sqlite3.IntegrityError as e:
            print(f"Error: {e}")
            return False
    
    def delete_book(self, book_id: int) -> bool:
        """
        Delete a book from the database.
        
        Args:
            book_id: ID of the book to delete
            
        Returns:
            True if deletion was successful, False otherwise
        """
        self.cursor.execute('DELETE FROM books WHERE id = ?', (book_id,))
        self.conn.commit()
        return self.cursor.rowcount > 0
    
    def get_books_by_genre(self, genre: str) -> List[Tuple]:
        """
        Get all books of a specific genre.
        
        Args:
            genre: Genre to filter by
            
        Returns:
            List of tuples containing book data
        """
        self.cursor.execute('SELECT * FROM books WHERE genre = ? ORDER BY title', (genre,))
        return self.cursor.fetchall()
    
    def close(self):
        """Close the database connection."""
        if self.conn:
            self.conn.close()
    
    def __enter__(self):
        """Context manager entry."""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close()
