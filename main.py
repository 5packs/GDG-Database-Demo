"""
Main script to demonstrate the Book Management System
"""

from book_manager import BookManager


def print_book(book):
    """Print book information in a formatted way."""
    if book:
        print(f"ID: {book[0]}")
        print(f"Title: {book[1]}")
        print(f"Author: {book[2]}")
        print(f"Year: {book[3] if book[3] else 'N/A'}")
        print(f"ISBN: {book[4] if book[4] else 'N/A'}")
        print(f"Genre: {book[5] if book[5] else 'N/A'}")
        print("-" * 50)


def print_all_books(books):
    """Print all books in a formatted table."""
    if not books:
        print("No books found.")
        return
    
    print("\n" + "=" * 80)
    print(f"{'ID':<5} {'Title':<30} {'Author':<25} {'Year':<6} {'Genre':<12}")
    print("=" * 80)
    for book in books:
        book_id, title, author, year, isbn, genre = book
        year_str = str(year) if year else "N/A"
        genre_str = genre if genre else "N/A"
        title_short = title[:27] + "..." if len(title) > 30 else title
        author_short = author[:22] + "..." if len(author) > 25 else author
        print(f"{book_id:<5} {title_short:<30} {author_short:<25} {year_str:<6} {genre_str:<12}")
    print("=" * 80 + "\n")


def populate_sample_data(manager):
    """Add sample books to the database."""
    sample_books = [
        ("To Kill a Mockingbird", "Harper Lee", 1960, "978-0061120084", "Fiction"),
        ("1984", "George Orwell", 1949, "978-0451524935", "Dystopian"),
        ("Pride and Prejudice", "Jane Austen", 1813, "978-0141439518", "Romance"),
        ("The Great Gatsby", "F. Scott Fitzgerald", 1925, "978-0743273565", "Fiction"),
        ("One Hundred Years of Solitude", "Gabriel García Márquez", 1967, "978-0060883287", "Magical Realism"),
        ("The Catcher in the Rye", "J.D. Salinger", 1951, "978-0316769174", "Fiction"),
        ("The Hobbit", "J.R.R. Tolkien", 1937, "978-0547928227", "Fantasy"),
        ("Harry Potter and the Philosopher's Stone", "J.K. Rowling", 1997, "978-0439708180", "Fantasy"),
        ("The Lord of the Rings", "J.R.R. Tolkien", 1954, "978-0544003415", "Fantasy"),
        ("Animal Farm", "George Orwell", 1945, "978-0451526342", "Political Satire"),
    ]
    
    print("Populating database with sample books...")
    for title, author, year, isbn, genre in sample_books:
        manager.add_book(title, author, year, isbn, genre)
    print(f"Added {len(sample_books)} sample books.\n")


def main():
    """Main function to demonstrate book management operations."""
    
    print("=" * 80)
    print("Book Management System - SQLite Database Demo")
    print("=" * 80)
    
    # Create a BookManager instance
    with BookManager("books.db") as manager:
        
        # Check if database is empty and populate with sample data
        existing_books = manager.get_all_books()
        if not existing_books:
            populate_sample_data(manager)
        
        # Display all books
        print("\n1. Displaying all books:")
        all_books = manager.get_all_books()
        print_all_books(all_books)
        
        # Search for books
        print("\n2. Searching for books with 'Harry' in title or author:")
        search_results = manager.search_books("Harry")
        print_all_books(search_results)
        
        # Get books by genre
        print("\n3. Getting all Fantasy books:")
        fantasy_books = manager.get_books_by_genre("Fantasy")
        print_all_books(fantasy_books)
        
        # Get a specific book
        print("\n4. Getting book with ID 1:")
        book = manager.get_book_by_id(1)
        print_book(book)
        
        # Add a new book
        print("\n5. Adding a new book:")
        new_book_id = manager.add_book(
            "The Hitchhiker's Guide to the Galaxy",
            "Douglas Adams",
            1979,
            "978-0345391803",
            "Science Fiction"
        )
        if new_book_id > 0:
            print(f"Successfully added book with ID: {new_book_id}")
            new_book = manager.get_book_by_id(new_book_id)
            print_book(new_book)
        
        # Update a book
        print("\n6. Updating book with ID 1 (changing year):")
        if manager.update_book(1, year=1961):
            print("Book updated successfully!")
            updated_book = manager.get_book_by_id(1)
            print_book(updated_book)
        
        # Display final state
        print("\n7. Final list of all books:")
        all_books = manager.get_all_books()
        print_all_books(all_books)
        
        print("\nDatabase operations completed successfully!")
        print(f"Total books in database: {len(all_books)}")


if __name__ == "__main__":
    main()
