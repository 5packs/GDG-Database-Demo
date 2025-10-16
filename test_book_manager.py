"""
Simple tests for the Book Management System
"""

import os
import sqlite3
from book_manager import BookManager


def test_database_creation():
    """Test that database and table are created properly."""
    db_name = "test_books.db"
    
    # Remove test database if it exists
    if os.path.exists(db_name):
        os.remove(db_name)
    
    # Create BookManager instance
    manager = BookManager(db_name)
    
    # Check that database file was created
    assert os.path.exists(db_name), "Database file should be created"
    
    # Check that table exists
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='books'")
    result = cursor.fetchone()
    conn.close()
    
    assert result is not None, "Books table should exist"
    
    # Cleanup
    manager.close()
    os.remove(db_name)
    print("✓ Test: Database creation passed")


def test_add_book():
    """Test adding a book to the database."""
    db_name = "test_books.db"
    
    if os.path.exists(db_name):
        os.remove(db_name)
    
    with BookManager(db_name) as manager:
        book_id = manager.add_book(
            "Test Book",
            "Test Author",
            2024,
            "978-1234567890",
            "Test Genre"
        )
        
        assert book_id > 0, "Book ID should be positive"
        
        # Retrieve the book
        book = manager.get_book_by_id(book_id)
        assert book is not None, "Book should be retrievable"
        assert book[1] == "Test Book", "Book title should match"
        assert book[2] == "Test Author", "Book author should match"
        assert book[3] == 2024, "Book year should match"
    
    os.remove(db_name)
    print("✓ Test: Add book passed")


def test_search_books():
    """Test searching for books."""
    db_name = "test_books.db"
    
    if os.path.exists(db_name):
        os.remove(db_name)
    
    with BookManager(db_name) as manager:
        # Add multiple books
        manager.add_book("Harry Potter", "J.K. Rowling", 1997)
        manager.add_book("The Hobbit", "J.R.R. Tolkien", 1937)
        manager.add_book("1984", "George Orwell", 1949)
        
        # Search for "Harry"
        results = manager.search_books("Harry")
        assert len(results) == 1, "Should find one book with 'Harry'"
        assert results[0][1] == "Harry Potter", "Should find Harry Potter"
        
        # Search for "Tolkien"
        results = manager.search_books("Tolkien")
        assert len(results) == 1, "Should find one book by Tolkien"
    
    os.remove(db_name)
    print("✓ Test: Search books passed")


def test_update_book():
    """Test updating a book."""
    db_name = "test_books.db"
    
    if os.path.exists(db_name):
        os.remove(db_name)
    
    with BookManager(db_name) as manager:
        book_id = manager.add_book("Original Title", "Original Author", 2000)
        
        # Update the book
        success = manager.update_book(book_id, title="Updated Title", year=2024)
        assert success, "Update should succeed"
        
        # Verify update
        book = manager.get_book_by_id(book_id)
        assert book[1] == "Updated Title", "Title should be updated"
        assert book[2] == "Original Author", "Author should remain unchanged"
        assert book[3] == 2024, "Year should be updated"
    
    os.remove(db_name)
    print("✓ Test: Update book passed")


def test_delete_book():
    """Test deleting a book."""
    db_name = "test_books.db"
    
    if os.path.exists(db_name):
        os.remove(db_name)
    
    with BookManager(db_name) as manager:
        book_id = manager.add_book("To Delete", "Author", 2000)
        
        # Verify book exists
        book = manager.get_book_by_id(book_id)
        assert book is not None, "Book should exist before deletion"
        
        # Delete the book
        success = manager.delete_book(book_id)
        assert success, "Deletion should succeed"
        
        # Verify book is gone
        book = manager.get_book_by_id(book_id)
        assert book is None, "Book should not exist after deletion"
    
    os.remove(db_name)
    print("✓ Test: Delete book passed")


def test_get_books_by_genre():
    """Test filtering books by genre."""
    db_name = "test_books.db"
    
    if os.path.exists(db_name):
        os.remove(db_name)
    
    with BookManager(db_name) as manager:
        manager.add_book("Fantasy Book 1", "Author 1", 2020, genre="Fantasy")
        manager.add_book("Fantasy Book 2", "Author 2", 2021, genre="Fantasy")
        manager.add_book("Sci-Fi Book", "Author 3", 2022, genre="Science Fiction")
        
        fantasy_books = manager.get_books_by_genre("Fantasy")
        assert len(fantasy_books) == 2, "Should find 2 fantasy books"
        
        scifi_books = manager.get_books_by_genre("Science Fiction")
        assert len(scifi_books) == 1, "Should find 1 sci-fi book"
    
    os.remove(db_name)
    print("✓ Test: Get books by genre passed")


def run_all_tests():
    """Run all tests."""
    print("\nRunning Book Management System Tests")
    print("=" * 50)
    
    test_database_creation()
    test_add_book()
    test_search_books()
    test_update_book()
    test_delete_book()
    test_get_books_by_genre()
    
    print("=" * 50)
    print("All tests passed! ✓\n")


if __name__ == "__main__":
    run_all_tests()
