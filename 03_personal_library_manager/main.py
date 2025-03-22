import json

class BookCollection:
    """A class to manage a book collection, enabling users to store, organize, and track their reading materials."""

    def __init__(self):
        """Book collection ko initialize karna, jisme ek khaali list aur file storage setup hogi"""
        self.book_list = []  # Sab books ko store karne ke liye ek list
        self.storage_file = 'books_data.json'  # JSON file jisme data save hoga
        self.read_from_file()  # Pehle se saved books ko load karna

    def read_from_file(self):
        """JSON file se books ka data load karna. Agar file nahi milti ya corrupted hoti hai to khaali list use hogi"""
        try:
            with open(self.storage_file, "r") as file:
                self.book_list = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            self.book_list = []  # Agar file nahi mili to khaali list rakho

    def save_to_file(self):
        """Current book collection ko JSON file mein save karna takay data lost na ho"""
        with open(self.storage_file, "w") as file:
            json.dump(self.book_list, file, indent=4)

    def create_new_book(self):
        """User se book ka data le kar collection mein add karna"""
        book_title = input("Enter book title: ")
        book_author = input("Enter author: ")
        publication_year = input("Enter publication year: ")
        book_genre = input("Enter genre: ")
        is_book_read = input("Have you read this book? (yes/no): ").strip().lower() == "yes"

        new_book = {
            "title": book_title,
            "author": book_author,
            "year": publication_year,
            "genre": book_genre,
            "read": is_book_read,
        }

        self.book_list.append(new_book)  # Nai book list mein add karo
        self.save_to_file()  # Data ko file mein save karo
        print("Book added successfully!\n")

    def delete_book(self):
        """Collection se kisi book ko title ke zariye delete karna"""
        book_title = input("Enter the title of the book to remove: ")

        for book in self.book_list:
            if book["title"].lower() == book_title.lower():
                self.book_list.remove(book)  # Book list se hatao
                self.save_to_file()  # File update karo
                print("Book removed successfully!\n")
                return
        print("Book not found!\n")  # Agar book nahi mili to yeh message show karo

    def find_book(self):
        """Title ya author ke zariye book search karna"""
        search_type = input("Search by:\n1. Title\n2. Author\nEnter your choice: ")
        search_text = input("Enter search term: ").lower()
        found_books = [book for book in self.book_list if search_text in book["title"].lower() or search_text in book["author"].lower()]

        if found_books:
            print("Matching Books:")
            for index, book in enumerate(found_books, 1):
                reading_status = "Read" if book["read"] else "Unread"
                print(f"{index}. {book['title']} by {book['author']} ({book['year']}) - {book['genre']} - {reading_status}")
        else:
            print("No matching books found.\n")  # Agar koi book nahi mili to message show karo

    def update_book(self):
        """Mojood books ki details ko update karna"""
        book_title = input("Enter the title of the book you want to edit: ")
        for book in self.book_list:
            if book["title"].lower() == book_title.lower():
                print("Leave blank to keep existing value.")  # Agar user koi field update nahi karna chahta to blank chhor sakta hai
                book["title"] = input(f"New title ({book['title']}): ") or book["title"]
                book["author"] = input(f"New author ({book['author']}): ") or book["author"]
                book["year"] = input(f"New year ({book['year']}): ") or book["year"]
                book["genre"] = input(f"New genre ({book['genre']}): ") or book["genre"]
                book["read"] = input("Have you read this book? (yes/no): ").strip().lower() == "yes"

                self.save_to_file()  # File ko update karo
                print("Book updated successfully!\n")
                return
        print("Book not found!\n")  # Agar book nahi mili to message show karo

    def show_all_books(self):
        """Puri book collection ko display karna"""
        if not self.book_list:
            print("Your collection is empty.\n")  # Agar koi book nahi hai to message show karo
            return

        print("Your Book Collection:")
        for index, book in enumerate(self.book_list, 1):
            reading_status = "Read" if book["read"] else "Unread"
            print(f"{index}. {book['title']} by {book['author']} ({book['year']}) - {book['genre']} - {reading_status}")
        print()

    def show_reading_progress(self):
        """Kitni books parh chuke ho aur kitni baqi hain uska progress dikhana"""
        total_books = len(self.book_list)
        completed_books = sum(1 for book in self.book_list if book["read"])
        completion_rate = (completed_books / total_books * 100) if total_books > 0 else 0

        print(f"Total books in collection: {total_books}")
        print(f"Reading progress: {completion_rate:.2f}%\n")  # Reading ka percentage dikhana

    def start_application(self):
        """Application ka main loop jo user ko options provide karega"""
        while True:
            print("📚 Welcome to Your Book Collection Manager! 📚")
            print("1. Add a new book")  # Nai book add karne ka option
            print("2. Remove a book")  # Book delete karne ka option
            print("3. Search for books")  # Books search karne ka option
            print("4. Update book details")  # Book ki details update karne ka option
            print("5. View all books")  # Sab books dekhne ka option
            print("6. View reading progress")  # Reading progress dekhne ka option
            print("7. Exit")  # Program exit karne ka option

            user_choice = input("Please choose an option (1-7): ")

            if user_choice == "1":
                self.create_new_book()
            elif user_choice == "2":
                self.delete_book()
            elif user_choice == "3":
                self.find_book()
            elif user_choice == "4":
                self.update_book()
            elif user_choice == "5":
                self.show_all_books()
            elif user_choice == "6":
                self.show_reading_progress()
            elif user_choice == "7":
                self.save_to_file()  # Exit se pehle data save kara ga json ki file ma 
                print("Thank you for using Book Collection Manager. Goodbye!")
                break
            else:
                print("Invalid choice. Please try again.\n")  # Agar user galat option choose kare to error message show karo


if __name__ == "__main__":
    book_manager = BookCollection()  # Class ka object banayein
    book_manager.start_application()  # Program ko start karein
