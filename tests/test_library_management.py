from datetime import date

import pytest

from library_management import Author, Book, Library, User


def test_library_borrow_and_return_flow() -> None:
    author = Author(author_id="A-1", first_name="Adam", last_name="Mickiewicz", nationality="PL")
    book = Book(
        isbn="978-0-123456-47-2",
        title="Pan Tadeusz",
        publication_year=1834,
        language="pl",
        genre="epic poem",
        page_count=340,
        authors=[author],
        total_copies=2,
        available_copies=2,
    )
    user = User(user_id="U-1", first_name="Jan", last_name="Kowalski", email="jan@example.com")

    library = Library(name="Biblioteka Uniwersytecka", address="Warszawa")
    library.add_book(book)
    library.register_user(user)

    loan = library.borrow_book(user_id="U-1", isbn=book.isbn, borrowed_on=date(2026, 4, 16), due_in_days=21)

    assert loan.user_id == "U-1"
    assert loan.isbn == book.isbn
    assert book.available_copies == 1
    assert len(user.active_loans) == 1

    library.return_book(user_id="U-1", isbn=book.isbn, returned_on=date(2026, 4, 20))

    assert book.available_copies == 2
    assert len(user.active_loans) == 0


def test_cannot_borrow_same_book_twice_without_return() -> None:
    book = Book(
        isbn="978-1-4028-9462-6",
        title="Example",
        publication_year=2020,
        language="en",
        genre="fiction",
        page_count=250,
    )
    user = User(user_id="U-2", first_name="Alice", last_name="Nowak", email="alice@example.com")

    library = Library(name="Biblioteka Uniwersytecka", address="Kraków")
    library.add_book(book)
    library.register_user(user)

    library.borrow_book(user_id="U-2", isbn=book.isbn, borrowed_on=date(2026, 4, 16))

    with pytest.raises(ValueError, match="active loan"):
        library.borrow_book(user_id="U-2", isbn=book.isbn, borrowed_on=date(2026, 4, 17))
