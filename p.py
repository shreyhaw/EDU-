import mysql.connector
from mysql.connector import Error
import tkinter as tk
from tkinter import ttk, messagebox

# Database connection configuration
def create_connection():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='toor',  # Replace with your MySQL password
            database='education'  # Assuming 'education' database already exists
        )
        if connection.is_connected():
            return connection
    except Error as e:
        print(f"Error: '{e}'")
        messagebox.showerror("Connection Error", f"Failed to connect to database: {e}")
        return None

def create_tables(connection):
    if connection is None:
        print("No connection to database.")
        return
    queries = [
        """CREATE TABLE IF NOT EXISTS instructors (
                instructor_id INTEGER PRIMARY KEY AUTO_INCREMENT, 
                instructor_name VARCHAR(255) NOT NULL,
                email VARCHAR(255),
                phone VARCHAR(255),
                bio TEXT
            )""",
        """CREATE TABLE IF NOT EXISTS course (
                course_id INTEGER PRIMARY KEY AUTO_INCREMENT,
                course_name VARCHAR(255) NOT NULL,
                description TEXT,
                credit_hours INTEGER,
                instructor_id INTEGER,
                FOREIGN KEY (instructor_id) REFERENCES instructors (instructor_id) ON DELETE CASCADE
            )""",
        """CREATE TABLE IF NOT EXISTS students (
                student_id INTEGER PRIMARY KEY AUTO_INCREMENT,
                student_name VARCHAR(255) NOT NULL,
                email VARCHAR(255),
                phone VARCHAR(255)
            )""",
        """CREATE TABLE IF NOT EXISTS enrolments (
                enrolment_id INTEGER PRIMARY KEY AUTO_INCREMENT,
                course_id INTEGER,
                student_id INTEGER,
                enrolment_date DATE,
                completion_status ENUM('enrolled', 'completed'),
                FOREIGN KEY (course_id) REFERENCES course (course_id) ON DELETE CASCADE,
                FOREIGN KEY (student_id) REFERENCES students (student_id) ON DELETE CASCADE
            )""",
        """CREATE TABLE IF NOT EXISTS assessments (
                assessment_id INTEGER PRIMARY KEY AUTO_INCREMENT,
                course_id INTEGER,
                assessment_name VARCHAR(255) NOT NULL,
                max_score INTEGER,
                given_by INTEGER,
                given_to INTEGER,
                FOREIGN KEY (course_id) REFERENCES course (course_id) ON DELETE CASCADE,
                FOREIGN KEY (given_by) REFERENCES instructors (instructor_id) ON DELETE CASCADE,
                FOREIGN KEY (given_to) REFERENCES students (student_id) ON DELETE CASCADE
            )""",
        """CREATE TABLE IF NOT EXISTS backup_instructors (
                id INTEGER PRIMARY KEY AUTO_INCREMENT,
                instructor_id INTEGER,
                instructor_name VARCHAR(255) NOT NULL,
                email VARCHAR(255),
                phone VARCHAR(255),
                bio TEXT,
                operation ENUM('DELETE') DEFAULT 'DELETE'
            )""",
        """CREATE TABLE IF NOT EXISTS backup_course (
                id INTEGER PRIMARY KEY AUTO_INCREMENT,
                course_id INTEGER,
                course_name VARCHAR(255) NOT NULL,
                description TEXT,
                credit_hours INTEGER,
                instructor_id INTEGER,
                operation ENUM('DELETE') DEFAULT 'DELETE'
            )""",
        """CREATE TABLE IF NOT EXISTS backup_students (
                id INTEGER PRIMARY KEY AUTO_INCREMENT,
                student_id INTEGER,
                student_name VARCHAR(255) NOT NULL,
                email VARCHAR(255),
                phone VARCHAR(255),
                operation ENUM('DELETE') DEFAULT 'DELETE'
            )""",
        """CREATE TABLE IF NOT EXISTS backup_assessments (
                id INTEGER PRIMARY KEY AUTO_INCREMENT,
                assessment_id INTEGER,
                course_id INTEGER,
                assessment_name VARCHAR(255) NOT NULL,
                max_score INTEGER,
                given_by INTEGER,
                given_to INTEGER,
                operation ENUM('DELETE') DEFAULT 'DELETE'
            )"""
    ]
    try:
        cursor = connection.cursor()
        for query in queries:
            cursor.execute(query)
        connection.commit()
        print("Tables created successfully.")
    except mysql.connector.Error as err:
        print(f"Error: '{err}'")

# Function to insert a new instructor into the database
def insert_instructor(connection, name, email, phone, bio):
    if connection is None:
        print("No connection to database.")
        return
    cursor = connection.cursor()
    try:
        query = "INSERT INTO instructors (instructor_name, email, phone, bio) VALUES (%s, %s, %s, %s)"
        values = (name, email, phone, bio)
        cursor.execute(query, values)
        connection.commit()
        print("Instructor inserted successfully.")
    except mysql.connector.Error as err:
        print(f"Error inserting instructor: {err}")

# Function to insert a new course into the database
def insert_course(connection, name, description, credit_hours, instructor_id):
    if connection is None:
        print("No connection to database.")
        return
    cursor = connection.cursor()
    try:
        query = "INSERT INTO course (course_name, description, credit_hours, instructor_id) VALUES (%s, %s, %s, %s)"
        values = (name, description, credit_hours, instructor_id)
        cursor.execute(query, values)
        connection.commit()
        print("Course inserted successfully.")
    except mysql.connector.Error as err:
        print(f"Error inserting course: {err}")

# Function to insert a new student into the database
def insert_student(connection, name, email, phone):
    if connection is None:
        print("No connection to database.")
        return
    cursor = connection.cursor()
    try:
        query = "INSERT INTO students (student_name, email, phone) VALUES (%s, %s, %s)"
        values = (name, email, phone)
        cursor.execute(query, values)
        connection.commit()
        print("Student inserted successfully.")
    except mysql.connector.Error as err:
        print(f"Error inserting student: {err}")

# Function to delete an instructor from the database
def delete_instructor(connection, instructor_id):
    if connection is None:
        print("No connection to database.")
        return
    cursor = connection.cursor()
    try:
        # Retrieve instructor details before deleting
        cursor.execute("SELECT * FROM instructors WHERE instructor_id = %s", (instructor_id,))
        instructor_data = cursor.fetchone()
        
        if instructor_data:
            # Insert into backup table
            query = "INSERT INTO backup_instructors (instructor_id, instructor_name, email, phone, bio) VALUES (%s, %s, %s, %s, %s)"
            cursor.execute(query, instructor_data)
        
        # Delete instructor from main table
        cursor.execute("DELETE FROM instructors WHERE instructor_id = %s", (instructor_id,))
        connection.commit()
        
        print(f"Instructor with ID {instructor_id} deleted successfully.")
    except mysql.connector.Error as err:
        print(f"Error deleting instructor: {err}")

# Function to delete a course from the database
def delete_course(connection, course_id):
    if connection is None:
        print("No connection to database.")
        return
    cursor = connection.cursor()
    try:
        # Retrieve course details before deleting
        cursor.execute("SELECT * FROM course WHERE course_id = %s", (course_id,))
        course_data = cursor.fetchone()

        if course_data:
            # Insert into backup table
            query = "INSERT INTO backup_course (course_id, course_name, description, credit_hours, instructor_id) VALUES (%s, %s, %s, %s, %s)"
            cursor.execute(query, course_data)

        # Delete course from main table
        cursor.execute("DELETE FROM course WHERE course_id = %s", (course_id,))
        connection.commit()

        print(f"Course with ID {course_id} deleted successfully.")
    except mysql.connector.Error as err:
        print(f"Error deleting course: {err}")

# Function to delete a student from the database
def delete_student(connection, student_id):
    if connection is None:
        print("No connection to database.")
        return
    cursor = connection.cursor()
    try:
        # Retrieve student details before deleting
        cursor.execute("SELECT * FROM students WHERE student_id = %s", (student_id,))
        student_data = cursor.fetchone()

        if student_data:
            # Insert into backup table
            query = "INSERT INTO backup_students (student_id, student_name, email, phone) VALUES (%s, %s, %s, %s)"
            cursor.execute(query, student_data)

        # Delete student from main table
        cursor.execute("DELETE FROM students WHERE student_id = %s", (student_id,))
        connection.commit()

        print(f"Student with ID {student_id} deleted successfully.")
    except mysql.connector.Error as err:
        print(f"Error deleting student: {err}")

def view_table(connection, table_name):
    if connection is None:
        print("No connection to database.")
        return []
    cursor = connection.cursor()
    try:
        cursor.execute(f"SELECT * FROM {table_name}")
        records = cursor.fetchall()
        return records
    except mysql.connector.Error as err:
        print(f"Error viewing {table_name}: {err}")
        return []

def display_deleted_items(connection):
    if connection is None:
        print("No connection to database.")
        return {}
    deleted_items = {}
    cursor = connection.cursor()
    try:
        backup_tables = ["backup_instructors", "backup_course", "backup_students", "backup_assessments"]
        for table in backup_tables:
            cursor.execute(f"SELECT * FROM {table}")
            records = cursor.fetchall()
            deleted_items[table] = records
    except mysql.connector.Error as err:
        print(f"Error viewing deleted items: {err}")
    return deleted_items

class DatabaseApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Database Management System")
        self.connection = create_connection()
        create_tables(self.connection)
        
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(pady=10, expand=True)
        
        self.create_instructor_tab()
        self.create_course_tab()
        self.create_student_tab()
        self.create_deleted_tab()

    def create_instructor_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Instructors")

        self.instructor_name_var = tk.StringVar()
        self.instructor_email_var = tk.StringVar()
        self.instructor_phone_var = tk.StringVar()
        self.instructor_bio_var = tk.StringVar()

        ttk.Label(tab, text="Name:").grid(row=0, column=0, padx=5, pady=5)
        ttk.Entry(tab, textvariable=self.instructor_name_var).grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(tab, text="Email:").grid(row=1, column=0, padx=5, pady=5)
        ttk.Entry(tab, textvariable=self.instructor_email_var).grid(row=1, column=1, padx=5, pady=5)
        
        ttk.Label(tab, text="Phone:").grid(row=2, column=0, padx=5, pady=5)
        ttk.Entry(tab, textvariable=self.instructor_phone_var).grid(row=2, column=1, padx=5, pady=5)
        
        ttk.Label(tab, text="Bio:").grid(row=3, column=0, padx=5, pady=5)
        ttk.Entry(tab, textvariable=self.instructor_bio_var).grid(row=3, column=1, padx=5, pady=5)

        ttk.Button(tab, text="Add Instructor", command=self.add_instructor).grid(row=4, column=0, columnspan=2, pady=10)
        ttk.Button(tab, text="View Instructors", command=self.view_instructors).grid(row=5, column=0, columnspan=2, pady=10)
        ttk.Button(tab, text="Delete Instructor", command=self.delete_instructor).grid(row=6, column=0, columnspan=2, pady=10)

    def create_course_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Courses")

        self.course_name_var = tk.StringVar()
        self.course_description_var = tk.StringVar()
        self.course_credit_hours_var = tk.IntVar()
        self.course_instructor_id_var = tk.IntVar()

        ttk.Label(tab, text="Name:").grid(row=0, column=0, padx=5, pady=5)
        ttk.Entry(tab, textvariable=self.course_name_var).grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(tab, text="Description:").grid(row=1, column=0, padx=5, pady=5)
        ttk.Entry(tab, textvariable=self.course_description_var).grid(row=1, column=1, padx=5, pady=5)
        
        ttk.Label(tab, text="Credit Hours:").grid(row=2, column=0, padx=5, pady=5)
        ttk.Entry(tab, textvariable=self.course_credit_hours_var).grid(row=2, column=1, padx=5, pady=5)
        
        ttk.Label(tab, text="Instructor ID:").grid(row=3, column=0, padx=5, pady=5)
        ttk.Entry(tab, textvariable=self.course_instructor_id_var).grid(row=3, column=1, padx=5, pady=5)

        ttk.Button(tab, text="Add Course", command=self.add_course).grid(row=4, column=0, columnspan=2, pady=10)
        ttk.Button(tab, text="View Courses", command=self.view_courses).grid(row=5, column=0, columnspan=2, pady=10)
        ttk.Button(tab, text="Delete Course", command=self.delete_course).grid(row=6, column=0, columnspan=2, pady=10)

    def create_student_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Students")

        self.student_name_var = tk.StringVar()
        self.student_email_var = tk.StringVar()
        self.student_phone_var = tk.StringVar()

        ttk.Label(tab, text="Name:").grid(row=0, column=0, padx=5, pady=5)
        ttk.Entry(tab, textvariable=self.student_name_var).grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(tab, text="Email:").grid(row=1, column=0, padx=5, pady=5)
        ttk.Entry(tab, textvariable=self.student_email_var).grid(row=1, column=1, padx=5, pady=5)
        
        ttk.Label(tab, text="Phone:").grid(row=2, column=0, padx=5, pady=5)
        ttk.Entry(tab, textvariable=self.student_phone_var).grid(row=2, column=1, padx=5, pady=5)

        ttk.Button(tab, text="Add Student", command=self.add_student).grid(row=3, column=0, columnspan=2, pady=10)
        ttk.Button(tab, text="View Students", command=self.view_students).grid(row=4, column=0, columnspan=2, pady=10)
        ttk.Button(tab, text="Delete Student", command=self.delete_student).grid(row=5, column=0, columnspan=2, pady=10)

    def create_deleted_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Deleted Items")

        ttk.Button(tab, text="View Deleted Items", command=self.view_deleted_items).pack(pady=20)

    def add_instructor(self):
        name = self.instructor_name_var.get()
        email = self.instructor_email_var.get()
        phone = self.instructor_phone_var.get()
        bio = self.instructor_bio_var.get()
        insert_instructor(self.connection, name, email, phone, bio)
    
    def view_instructors(self):
        records = view_table(self.connection, "instructors")
        self.display_records(records)

    def delete_instructor(self):
        self.show_delete_window("instructors")

    def add_course(self):
        name = self.course_name_var.get()
        description = self.course_description_var.get()
        credit_hours = self.course_credit_hours_var.get()
        instructor_id = self.course_instructor_id_var.get()
        insert_course(self.connection, name, description, credit_hours, instructor_id)
    
    def view_courses(self):
        records = view_table(self.connection, "course")
        self.display_records(records)

    def delete_course(self):
        self.show_delete_window("course")

    def add_student(self):
        name = self.student_name_var.get()
        email = self.student_email_var.get()
        phone = self.student_phone_var.get()
        insert_student(self.connection, name, email, phone)

    def view_students(self):
        records = view_table(self.connection, "students")
        self.display_records(records)

    def delete_student(self):
        self.show_delete_window("students")

    def view_deleted_items(self):
        deleted_items = display_deleted_items(self.connection)
        self.display_deleted_records(deleted_items)

    def display_records(self, records):
        new_window = tk.Toplevel(self.root)
        new_window.title("Records")
        text = tk.Text(new_window)
        text.pack()
        for record in records:
            text.insert(tk.END, f"{record}\n")

    def display_deleted_records(self, deleted_items):
        new_window = tk.Toplevel(self.root)
        new_window.title("Deleted Records")
        text = tk.Text(new_window)
        text.pack()
        for table, records in deleted_items.items():
            text.insert(tk.END, f"Deleted {table}:\n")
            for record in records:
                text.insert(tk.END, f"{record}\n")
            text.insert(tk.END, "\n")

    def show_delete_window(self, table_name):
        new_window = tk.Toplevel(self.root)
        new_window.title(f"Delete from {table_name}")
        id_var = tk.IntVar()
        ttk.Label(new_window, text="Enter ID:").pack(pady=5)
        ttk.Entry(new_window, textvariable=id_var).pack(pady=5)
        if table_name == "instructors":
            delete_command = lambda: delete_instructor(self.connection, id_var.get())
        elif table_name == "course":
            delete_command = lambda: delete_course(self.connection, id_var.get())
        elif table_name == "students":
            delete_command = lambda: delete_student(self.connection, id_var.get())
        ttk.Button(new_window, text="Delete", command=delete_command).pack(pady=10)

if __name__ == "__main__":
    root = tk.Tk()
    app = DatabaseApp(root)  # <-- Add parentheses to create an instance of DatabaseApp
    root.mainloop()

