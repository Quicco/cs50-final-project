import sqlite3
from argon2 import PasswordHasher
from faker import Faker


db_path = "database.db"
con = sqlite3.connect(db_path)
cur = con.cursor()
ph = PasswordHasher()


def initialize_db():
    create_tables()
    populate_db()


def create_tables():
    queries = [
        "CREATE TABLE IF NOT EXISTS teacher (teacher_id INTEGER PRIMARY KEY, name TEXT, email TEXT, password TEXT, class_id INTEGER, FOREIGN KEY (class_id) REFERENCES class(class_id));",
        "CREATE TABLE IF NOT EXISTS class (class_id INTEGER PRIMARY KEY, course TEXT, class_type TEXT, time_slot TEXT, location TEXT, year INTEGER);",
        "CREATE TABLE IF NOT EXISTS student (student_id INTEGER PRIMARY KEY, name TEXT, email TEXT, phone TEXT, location TEXT, course TEXT, class_type TEXT, teacher_id INTEGER, FOREIGN KEY (teacher_id) REFERENCES teacher(teacher_id));",
        "CREATE TABLE IF NOT EXISTS class_teacher (class_id INTEGER, teacher_id INTEGER, PRIMARY KEY (class_id, teacher_id), FOREIGN KEY (class_id) REFERENCES class(class_id), FOREIGN KEY (teacher_id) REFERENCES teacher(teacher_id));",
    ]
    for query in queries:
        cur.execute(query)
    con.commit()


def populate_db():
    fake = Faker("pt_PT")

    # Populate teacher table
    DEV_NAME = "Tiago"
    DEV_MAIL = "admin@dev.com"
    DEV_PW = ph.hash("123")
    DEV_CLASS = 1
    cur.execute(
        "INSERT INTO teacher (name, email, password, class_id) VALUES (?, ?, ?, ?)",
        (DEV_NAME, DEV_MAIL, DEV_PW, DEV_CLASS),
    )
    # Populate class table
    classes = [
        {
            "course": "Junior Fullstack Developer",
            "class_type": "PowerUp",
            "time_slot": "Morning",
            "location": "Lisbon",
            "year": 2024,
        },
        {
            "course": "Junior Fullstack Developer",
            "class_type": "PowerUp",
            "time_slot": "Afternoon",
            "location": "Lisbon",
            "year": 2024,
        },
    ]
    for group in classes:
        values = tuple(group.values())
        cur.execute(
            "INSERT INTO class (course, class_type, time_slot, location, year) VALUES (?, ?, ?, ? , ?)",
            values,
        )
    con.commit()
    # Populate student table
    students = []
    for _ in range(48):
        students.append(
            {
                "name": fake.name(),
                "email": fake.email(),
                "phone": fake.phone_number(),
                "location": "Lisbon",
                "course": "Junior Fullstack Developer",
                "class_type": "PowerUp",
            }
        )

    for student in students:
        values = tuple(student.values())
        cur.execute(
            "INSERT INTO student (name, email, phone, location, course, class_type) VALUES (?, ?, ?, ? , ?, ?)",
            values,
        )
    con.commit()


initialize_db()
con.close()
