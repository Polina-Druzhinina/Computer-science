import sqlite3

#подключение к базе данных
connection = sqlite3.connect("basa.db")
connection.row_factory = sqlite3.Row
cursor = connection.cursor()

#Создание таблиц
cursor.execute("""
    CREATE TABLE IF NOT EXISTS `job_titles`(
        `id_job_title` integer primary key NOT NULL UNIQUE,
        `name` TEXT NOT NULL
    );
""")

job_titles_data = [
    (1, "менеджер"),
    (2, "Дизайнер"),
    (3,"Разработчик"),
    (4, "Аналитик"),
    (5, "Юрист")
]
cursor.executemany("INSERT OR IGNORE INTO `job_titles`(`id_job_title`,`name`) VALUES (?,?)", job_titles_data)
connection.commit()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS `employees`(
        `id_employee` integer primary key NOT NULL UNIQUE,
        `surname` TEXT NOT NULL,
        `name` TEXT NOT NULL,
        `phone` TEXT NOT NULL,
        `id_job_title` INTEGER NOT NULL,
        FOREIGN KEY(`id_job_title`) REFERENCES `job_titles`(`id_job_title`)
    );
""")

employees_data = [
    (1,"Иванов","Андрей","89124567321", 3),
    (2,"Петров","Максим", "89263457891", 2),
    (3,"Сидорова", "Анна","89516783452", 4),
    (4,"Кузнецов","Дмитрий","89051237894",2),
    (5,"Смирнова", "Ольга", "89774561238", 5),
    (6,"Васильева","Игонь","89683451729",2),
    (7,"Федерова","Мария","89375641287",2),
    (8,"Николаева", "Павел","89831245764",4),
    (9,"Орлова","Екатерина","89167834592",1),
    (10,"Морозов","Сергей","89275613480",2)
]
cursor.executemany("INSERT OR IGNORE INTO `employees`(`id_employee`,`surname`, `name`, `phone`, `id_job_title`) VALUES (?,?,?,?,?)", employees_data)
connection.commit()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS `clients`(
               `id_client` integer primary key NOT NULL UNIQUE,
               `organization` TEXT NOT NULL,
               `phone` TEXT NOT NULL
               );
""")
clients_data = [
    (1,"«ООО ТехноСфера»","89123456789"),
    (2,"Компания «ГринЭнерджи»","89264581234"),
    (3,"«Новый Вектор»","89056734521"),
    (4,"фирма «Быстрая Доставка»","89772843956"),
    (5,"агентство «Пиксель Плюс»","89685176240")
]
cursor.executemany("INSERT OR IGNORE INTO `clients`(`id_client`,`organization`, `phone`) VALUES (?,?,?)", clients_data)
connection.commit()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS `orders`(
        `id_order` integer primary key NOT NULL UNIQUE,
        `id_client` INTEGER NOT NULL,
        `id_employee` INTEGER NOT NULL,
        `summa` INTEGER NOT NULL,
        `date_completion` TEXT NOT NULL,
        `mark_completion` INTEGER NOT NULL CHECK (mark_completion IN (0,1)),
        FOREIGN KEY(`id_employee`) REFERENCES `employees`(`id_employee`),
        FOREIGN KEY(`id_client`) REFERENCES `clients`(`id_client`)
    );
""")

orders_data = [
    (1,1,3,125000, "12.02.2026",1),
    (2,4,7,54000, "28.03.2026",0),
    (3,2,1,78000, "05.01.2026",1),
    (4,5,9,210000, "17.04.2026",0),
    (5,3,3,42000, "30.12.2025",1),
    (6,1,5,96000, "09.05.2026",0),
    (7,4,10,150000, "20.11.2025",1),
    (8,2,6,67000, "14.03.2026",0),
    (9,5,8,89000, "03.02.2026",1),
    (10,4,3,120000, "19.06.2026",0)
]

cursor.executemany("INSERT OR IGNORE INTO `orders`(`id_order`,`id_client`, `id_employee`, `summa`,`date_completion`,`mark_completion`) VALUES (?,?,?,?,?,?)", orders_data)
connection.commit()


'''
cursor.execute("SELECT * FROM `clients`")
rows = cursor.fetchall()

for row in rows:
    print(row)
    '''
#простые запросы
#count
cursor.execute("SELECT * FROM `employees`")
rows = cursor.fetchall()
print(f"Общее количество сотрудников: {len(rows)}")

#max summ
cursor.execute("SELECT MAX(summa) FROM `orders`")
max_sum = cursor.fetchone()[0]
print(f"Максимальная сумма заказа: {max_sum}")

#summ
cursor.execute("SELECT SUM(summa) FROM `orders`")
rows = cursor.fetchone()[0]
print(f"Суммарная сумма заказов: {rows}")

#count clients
cursor.execute("SELECT * FROM `clients`")
rows = cursor.fetchall()
print(f"Общее количество клиентов: {len(rows)}")

#средняя сумма всех заказов
cursor.execute("SELECT AVG(summa) FROM `orders`")
rows = cursor.fetchone()[0]
print(f"Средняя сумма заказов: {round(rows, 2)}")


#С агрегацией
#средняя сумма заказов для каждого сотрудника
cursor.execute("SELECT `id_employee`, AVG(summa) FROM `orders` GROUP BY `id_employee`")
rows = cursor.fetchall()
for i in rows:
    print(f"Сотрудник {i["id_employee"]} средняя сумма заказа - {round(i[1],2)}")

#Количество выполненных заказов для каждого клиента
cursor.execute("SELECT `id_client`, SUM(mark_completion) FROM `orders` GROUP BY `id_client`") 
rows = cursor.fetchall()
for i in rows:
    print(f"ID клиента {i["id_client"]} количество выполненныз заказов: {i[1]}")

#Общая сумма заказов для каждого клиента
cursor.execute("SELECT `id_client`, SUM(summa) FROM `orders` GROUP BY `id_client`")
rows = cursor.fetchall()
for i in rows:
    print(f"ID клиента {i["id_client"]} - общая сумма заказа: {i[1]}")

#С объединением и условиями
#Фамилии и имена сотрудников вместе с суммой их выполненных заказов
cursor.execute("SELECT employees.surname, employees.name, SUM(orders.summa) FROM employees JOIN orders ON employees.id_employee = orders.id_employee WHERE orders.mark_completion = 1 GROUP BY employees.id_employee")
rows = cursor.fetchall()
for i in rows:
    print(f"{i["surname"]} {i["name"]} - сумма всех выполненных заказов: {i[2 ]}")

#Список клиентов и сотрудников, которые обслуживали их заказы, с суммой заказа больше 100000
cursor.execute("SELECT clients.organization, employees.surname, employees.name, orders.summa FROM orders JOIN clients ON orders.id_client = clients.id_client JOIN employees ON orders.id_employee = employees.id_employee WHERE orders.summa > 100000")
rows = cursor.fetchall()
for i in rows:
    print(f"Клиент: {i['organization']}. Сотрудник: {i['surname']} {i['name']}. Сумма заказа: {i['summa']}")

#сотрудники и клиенты для заказов, которые были выполнены
cursor.execute("SELECT employees.surname, employees.name, clients.organization, orders.summa FROM orders JOIN employees ON orders.id_employee = employees.id_employee JOIN clients ON orders.id_client = clients.id_client WHERE orders.mark_completion = 1")
rows = cursor.fetchall()
for i in rows:
    print(f"Сотрудник: {i['surname']} {i['name']}. Клиент: {i['organization']}. Сумма: {i['summa']}")