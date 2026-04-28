import sqlite3

# Connect to (or create) the database
conn = sqlite3.connect("hw13.db")
cur = conn.cursor()

# Load schema
with open("schema.sql", "r") as f:
    cur.executescript(f.read())

# Insert student
cur.execute(
    "INSERT INTO students (first_name, last_name) VALUES (?, ?)",
    ("John", "Smith")
)

# Insert quiz
cur.execute(
    "INSERT INTO quizzes (subject, num_questions, quiz_date) VALUES (?, ?, ?)",
    ("Python Basics", 5, "2015-02-05")
)

# Insert quiz result
cur.execute(
    "INSERT INTO results (student_id, quiz_id, score) VALUES (?, ?, ?)",
    (1, 1, 85)
)

conn.commit()
conn.close()

print("Database created and seeded with required assignment data.")