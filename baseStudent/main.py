import sqlite3

connection = sqlite3.connect("basa.db")
cursor = connection.cursor()


cursor.execute("""
CREATE TABLE IF NOT EXISTS students(
    id_students INTEGER PRIMARY KEY AUTOINCREMENT,
    id_level INTEGER,
    id_destination INTEGER,
    id_type_education INTEGER,
    surname TEXT NOT NULL,
    name TEXT NOT NULL,
    patronymic TEXT NOT NULL,
    avrg_score REAL NOT NULL,
    FOREIGN KEY (id_level) REFERENCES level_education(id_level),
    FOREIGN KEY (id_destination) REFERENCES destination(id_destination),
    FOREIGN KEY (id_type_education) REFERENCES type_education(id_type_education)
);
""")

with open("students.txt", "r", encoding="utf-8") as file:
    for line in file:
        data = line.strip().split(",")
        data[-1] = float(data[-1])

        cursor.execute("""
            INSERT INTO students(
                id_level, id_destination, id_type_education,
                surname, name, patronymic, avrg_score
            ) VALUES (?, ?, ?, ?, ?, ?, ?)
        """, data)

connection.commit()


cursor.execute("""
CREATE TABLE IF NOT EXISTS level_education(
    id_level INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL
);
""")

with open("level_education.txt", "r", encoding="utf-8") as file:
    for line in file:
        data = line.strip()

        cursor.execute("""
            INSERT INTO level_education(name)
            VALUES (?)
        """, (data,))

connection.commit()


cursor.execute("""
CREATE TABLE IF NOT EXISTS destination(
    id_destination INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL
);
""")

with open("destination.txt", "r", encoding="utf-8") as file:
    for line in file:
        data = line.strip()

        cursor.execute("""
            INSERT INTO destination(name)
            VALUES (?)
        """, (data,))

connection.commit()

cursor.execute("""
CREATE TABLE IF NOT EXISTS type_education(
    id_type_education INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL
);
""")

with open("type_education.txt", "r", encoding="utf-8") as file:
    for line in file:
        data = line.strip()

        cursor.execute("""
            INSERT INTO type_education(name)
            VALUES (?)
        """, (data,))

connection.commit()

#task1
cursor.execute("SELECT COUNT(name) FROM students")
count = cursor.fetchone()[0]
print(f"Count all students = {count}\n")

#task2
cursor.execute("SELECT destination.name, COUNT(students.id_students)  FROM students JOIN destination ON students.id_destination = destination.id_destination GROUP BY destination.name")
rows = cursor.fetchall()
for row in rows:
    print(row)
print()

#task3
cursor.execute("SELECT type_education.name, COUNT(students.id_students)  FROM students JOIN type_education ON students.id_type_education = type_education.id_type_education GROUP BY type_education.name")
rows = cursor.fetchall()
for row in rows:
    print(row)
print()

#task4
cursor.execute("SELECT destination.name, MAX(students.avrg_score),MIN(students.avrg_score), AVG(students.avrg_score) FROM students JOIN destination ON students.id_destination = destination.id_destination GROUP BY destination.name")
rows = cursor.fetchall()
for row in rows:
    print(row)
print()

#task5
cursor.execute("""
SELECT destination.name,level_education.name,type_education.name,AVG(students.avrg_score) FROM students
    JOIN destination  ON students.id_destination = destination.id_destination
    JOIN level_education ON students.id_level = level_education.id_level
    JOIN type_education ON students.id_type_education = type_education.id_type_education
    GROUP BY destination.name,level_education.name,type_education.name
""")
rows = cursor.fetchall()
for row in rows:
    print(row)
print()

#task6
cursor.execute("""
SELECT students.surname, students.name, students.avrg_score FROM students
               JOIN destination ON students.id_destination = destination.id_destination
               JOIN type_education ON students.id_type_education = type_education.id_type_education
               WHERE destination.name = 'Прикладная информатика' AND type_education.name = 'очная'
               ORDER BY avrg_score DESC
               LIMIT 5
""")
rows = cursor.fetchall()
for row in rows:
    print(row)
print()

#task7
cursor.execute("SELECT surname, COUNT(*) as cnt FROM students GROUP BY surname HAVING COUNT(*) > 1")
rows = cursor.fetchall()
for row in rows:
    print(row)
print()

#task8
cursor.execute("SELECT surname,name,patronymic, COUNT(*) as cnt FROM students GROUP BY surname, name,patronymic HAVING COUNT(*) > 1")
rows = cursor.fetchall()
if rows:
    for row in rows:
        print(row)
else:
    print("Таких записей нет")