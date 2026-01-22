books_data = [
    {
        "id": 1,
        "title": "The Great Gatsby",
        "author": "F. Scott Fitzgerald",
        "year": 1925,
        "genre": "Classic",
        "rating": 4.2
    },
    {
        "id": 2,
        "title": "To Kill a Mockingbird",
        "author": "Harper Lee",
        "year": 1960,
        "genre": "Historical Fiction",
        "rating": 4.5
    },
    {
        "id": 3,
        "title": "1984",
        "author": "George Orwell",
        "year": 1949,
        "genre": "Dystopian",
        "rating": 4.6
    },
    {
        "id": 4,
        "title": "The Hobbit",
        "author": "J.R.R. Tolkien",
        "year": 1937,
        "genre": "Fantasy",
        "rating": 4.8
    },
    {
        "id": 5,
        "title": "Sapiens: A Brief History of Humankind",
        "author": "Yuval Noah Harari",
        "year": 2011,
        "genre": "Non-fiction",
        "rating": 4.4
    },
    {
        "id": 6,
        "title": "Dune",
        "author": "Frank Herbert",
        "year": 1965,
        "genre": "Science Fiction",
        "rating": 4.7
    },
    {
        "id": 7,
        "title": "Pride and Prejudice",
        "author": "Jane Austen",
        "year": 1813,
        "genre": "Romance",
        "rating": 4.3
    }
]
students_data = [
    {
        "student_id": 101,
        "name": "Alice Johnson",
        "grade": 10,
        "borrowed_books": [1, 4]  # Borrowed 'The Great Gatsby' and 'The Hobbit'
    },
    {
        "student_id": 102,
        "name": "Bob Smith",
        "grade": 11,
        "borrowed_books": [3]     # Borrowed '1984'
    },
    {
        "student_id": 103,
        "name": "Charlie Davis",
        "grade": 9,
        "borrowed_books": []      # No books borrowed
    },
    {
        "student_id": 104,
        "name": "Diana Prince",
        "grade": 12,
        "borrowed_books": [2, 5, 6] # Borrowed 'To Kill a Mockingbird', 'Sapiens', 'Dune'
    },
    {
        "student_id": 105,
        "name": "Ethan Hunt",
        "grade": 10,
        "borrowed_books": [7]     # Borrowed 'Pride and Prejudice'
    }
]
def view_books():
    print("Books in Library:")
    for book in books_data:
        if book['available']:
            print(f"ID: {book['id']}, Title: {book['title']}, Author: {book['author']}, Year: {book['year']}, Genre: {book['genre']}, Rating: {book['rating']}")
def view_students():
    print("Students in Library System:")
    for student in students_data:
        print(f"ID: {student['student_id']}, Name: {student['name']}, Grade: {student['grade']}, Borrowed Books: {student['borrowed_books']}")
def issue_book():
    book_id=int(input("Enter Book ID to issue: "))
    student_id=int(input("Enter Student ID: "))
    for book in books_data:
        if book_id==book['id']:
            if book['available']:
                for student in students_data:
                    if student_id==student['student_id']:
                        student['borrowed_books'].append(book_id)
                        book['issued_to']=student_id
                        book['available']=False
                        print(f"Book ID {book_id} issued to Student ID {student_id}.")
                        return True
                else: 
                    print("Student ID not found.")
                    return False
            else:
                print("Book is currently not available.")
                return False
        else:
            print("Book ID not found.")
            return False
def return_book():
    book_id=int(input("Enter Book ID to return: "))
    student_id=int(input("Enter Student ID: "))
    for book in books_data:
        if book_id==book['id']:
            if not book['available'] and book['issued_to']==student_id:
                for student in students_data:
                    if student_id==student['student_id']:
                        student['borrowed_books'].remove(book_id)
                        book['issued_to']=None
                        book['available']=True
                        print(f"Book ID {book_id} returned by Student ID {student_id}.")
                        return True
                else:
                    print("Student ID not found.")
                    return False
            else:
                print("This book was not issued to this student.")
                return False
        else:
            print("Book ID not found.")
            return False
def main():
    # Initialize book availability
    for book in books_data:
        book['available']=True
        book['issued_to']=None
    while True:
        print("\nLibrary Management System")
        print("1. View Books")
        print("2. View Students")
        print("3. Issue Book")
        print("4. Return Book")
        print("5. Exit")
        choice=int(input("Enter your choice: "))
        if choice==1:
            view_books()
        elif choice==2:
            view_students()
        elif choice==3:
            issue_book()
        elif choice==4:
            return_book()
        elif choice==5:
            print("Exiting the system. Goodbye!")
            break
        else:
            print("Invalid choice! Please try again.")
if __name__=="__main__":
    main()
