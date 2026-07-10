import csv


books = []
issued_books = []
BOOKS_FILE = "library_books.csv"
ISSUED_FILE = "library_issued.csv"


def find_book(book_id):
    for book in books:
        if book["id"] == book_id:
            return book
    return None


def read_quantity(prompt, minimum=0):
    try:
        quantity = int(input(prompt).strip())
        if quantity < minimum:
            print(f"Quantity must be at least {minimum}.")
            return None
        return quantity
    except ValueError:
        print("Please enter a valid whole number.")
        return None


def add_book():
    book_id = input("Enter Book ID: ").strip()
    if find_book(book_id):
        print("A book with this ID already exists.")
        return

    title = input("Enter Title: ").strip()
    author = input("Enter Author: ").strip()
    category = input("Enter Category: ").strip()
    quantity = read_quantity("Enter Quantity: ", 1)
    if quantity is None:
        return

    books.append(
        {
            "id": book_id,
            "title": title,
            "author": author,
            "category": category,
            "quantity": quantity,
            "issued": 0,
        }
    )
    print("Book added successfully ")


def view_books():
    if not books:
        print("No books found.")
        return

    print("\nID | Title | Author | Category | Available | Issued")
    print("-" * 75)
    for book in books:
        print(
            f"{book['id']} | {book['title']} | {book['author']} | "
            f"{book['category']} | {book['quantity']} | {book['issued']}"
        )


def search_book():
    search_value = input("Enter Book ID or Title: ").strip().lower()
    matches = [
        book
        for book in books
        if book["id"].lower() == search_value
        or book["title"].lower() == search_value
    ]

    if not matches:
        print("Book not found.")
        return

    for book in matches:
        print(
            f"ID: {book['id']}, Title: {book['title']}, Author: {book['author']}, "
            f"Category: {book['category']}, Available: {book['quantity']}, "
            f"Issued: {book['issued']}"
        )


def update_book():
    book = find_book(input("Enter Book ID: ").strip())
    if not book:
        print("Book not found.")
        return

    print("1. Update Title")
    print("2. Update Author")
    print("3. Update Category")
    print("4. Update Quantity")
    choice = input("Enter your choice: ").strip()

    if choice == "1":
        book["title"] = input("Enter new title: ").strip()
    elif choice == "2":
        book["author"] = input("Enter new author: ").strip()
    elif choice == "3":
        book["category"] = input("Enter new category: ").strip()
    elif choice == "4":
        new_quantity = read_quantity("Enter new total quantity: ")
        if new_quantity is None:
            return
        if new_quantity < book["issued"]:
            print("Quantity cannot be less than the number of issued books.")
            return
        book["quantity"] = new_quantity - book["issued"]
    else:
        print("Invalid choice.")
        return

    print("Book updated successfully.")


def delete_book():
    book = find_book(input("Enter Book ID: ").strip())
    if not book:
        print("Book not found.")
        return

    if book["issued"] > 0:
        print("Cannot delete a book that is currently issued.")
        return

    books.remove(book)
    print("Book deleted successfully.")


def issue_book():
    student_name = input("Enter Student Name: ").strip()
    book = find_book(input("Enter Book ID: ").strip())

    if not book:
        print("Book not found.")
        return
    if book["quantity"] == 0:
        print("No copies are available.")
        return

    book["quantity"] -= 1
    book["issued"] += 1
    issued_books.append({"student": student_name, "book_id": book["id"]})
    print("Book issued successfully.")


def return_book():
    student_name = input("Enter Student Name: ").strip()
    book_id = input("Enter Book ID: ").strip()

    for issued in issued_books:
        if issued["student"] == student_name and issued["book_id"] == book_id:
            book = find_book(book_id)
            if book is None:
                print("Book ID is invalid.")
                return
            book["quantity"] += 1
            book["issued"] -= 1
            issued_books.remove(issued)
            print("Book returned successfully.")
            return

    print("Issue record not found.")


def show_statistics():
    total_books = sum(book["quantity"] + book["issued"] for book in books)
    total_categories = len({book["category"] for book in books})
    most_issued = max(books, key=lambda book: book["issued"], default=None)
    available_books = sum(book["quantity"] for book in books)
    issued_count = sum(book["issued"] for book in books)

    print(f"Total Books: {total_books}")
    print(f"Total Categories: {total_categories}")
    if most_issued and most_issued["issued"] > 0:
        print(f"Most Issued Book: {most_issued['title']}")
    else:
        print("Most Issued Book: None")
    print(f"Available Books: {available_books}")
    print(f"Issued Books: {issued_count}")


def save_data():
    try:
        with open(BOOKS_FILE, "w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(
                file,
                fieldnames=["id", "title", "author", "category", "quantity", "issued"],
            )
            writer.writeheader()
            writer.writerows(books)

        with open(ISSUED_FILE, "w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=["student", "book_id"])
            writer.writeheader()
            writer.writerows(issued_books)
        print("Data saved successfully.")
    except OSError as error:
        print(f"Could not save data: {error}")


def load_data():
    global books, issued_books
    try:
        with open(BOOKS_FILE, newline="", encoding="utf-8") as file:
            books = []
            for row in csv.DictReader(file):
                books.append(
                    {
                        "id": row["id"],
                        "title": row["title"],
                        "author": row["author"],
                        "category": row["category"],
                        "quantity": int(row["quantity"]),
                        "issued": int(row["issued"]),
                    }
                )

        with open(ISSUED_FILE, newline="", encoding="utf-8") as file:
            issued_books = list(csv.DictReader(file))
        print("Data loaded successfully.")
    except FileNotFoundError:
        books = []
        issued_books = []
        print("No saved data file found. Starting with an empty library.")
    except (OSError, KeyError, ValueError, csv.Error) as error:
        books = []
        issued_books = []
        print(f"Could not load saved data: {error}")


def main():
    load_data()

    while True:
        print("\n--- Library Management System ---")
        print("1. Add Book")
        print("2. View All Books")
        print("3. Search Book")
        print("4. Update Book Information")
        print("5. Delete Book")
        print("6. Issue Book")
        print("7. Return Book")
        print("8. Library Statistics")
        print("9. Save Data")
        print("0. Exit")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            add_book()
        elif choice == "2":
            view_books()
        elif choice == "3":
            search_book()
        elif choice == "4":
            update_book()
        elif choice == "5":
            delete_book()
        elif choice == "6":
            issue_book()
        elif choice == "7":
            return_book()
        elif choice == "8":
            show_statistics()
        elif choice == "9":
            save_data()
        elif choice == "0":
            save_data()
            print("Goodbye.")
            break
        else:
            print("Invalid choice.")


if __name__ == "__main__":
    main()
