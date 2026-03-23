import pandas as pd
import sqlite3

file_path = "task.xlsx"

movement_goods_df = pd.read_excel(file_path, sheet_name="movement_goods")
product_df = pd.read_excel(file_path, sheet_name="product")
shops_df = pd.read_excel(file_path, sheet_name="shops")


conn = sqlite3.connect("my_database.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS shops (
    id_shop TEXT PRIMARY KEY,
    district TEXT NOT NULL,
    address TEXT NOT NULL
);
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS product (
    article INTEGER PRIMARY KEY,
    department TEXT NOT NULL,
    product_name TEXT NOT NULL,
    unit TEXT NOT NULL,
    quantity_per_pack INTEGER NOT NULL,
    price_per_pack REAL
);
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS movement_goods (
    id_operac INTEGER PRIMARY KEY,
    date TEXT NOT NULL,
    id_shop TEXT NOT NULL,
    article INTEGER NOT NULL,
    quantity INTEGER NOT NULL,
    operation_type TEXT NOT NULL,
    FOREIGN KEY (id_shop) REFERENCES shops(id_shop),
    FOREIGN KEY (article) REFERENCES product(article)
)
""")

conn.commit()

movement_goods_columns = {
    'ID операции': 'id_operac',
    'Дата': 'date',
    'ID магазина': 'id_shop',
    'Артикул': 'article',
    'Количество упаковок, шт': 'quantity',
    'Тип операции': 'operation_type'
}

product_columns = {
    'Артикул': 'article',
    'Отдел': 'department',
    'Наименование товара': 'product_name',
    'Ед_изм': 'unit',
    'Количество в упаковке': 'quantity_per_pack',
    'Цена за упаковку': 'price_per_pack'
}

shops_columns = {
    'ID магазина': 'id_shop',
    'Район': 'district',
    'Адрес': 'address'
}

movement_goods_df = movement_goods_df.rename(columns=movement_goods_columns)
product_df = product_df.rename(columns=product_columns)
shops_df = shops_df.rename(columns=shops_columns)

movement_goods_df['date'] = pd.to_datetime(movement_goods_df['date'], dayfirst=True).dt.strftime('%Y-%m-%d')

shops_df.to_sql('shops', conn, if_exists='append', index=False)
product_df.to_sql('product', conn, if_exists='append', index=False)
movement_goods_df.to_sql('movement_goods', conn, if_exists='append', index=False)

conn.commit()

query = """
SELECT SUM(movement_goods.quantity * product.price_per_pack) AS total
FROM movement_goods
JOIN product ON movement_goods.article = product.article
JOIN shops ON movement_goods.id_shop = shops.id_shop
WHERE product.product_name = 'Варенец термостатный'
  AND shops.district = 'Нагорный'
  AND movement_goods.operation_type = 'Продажа'
  AND movement_goods.date >= '2024-10-05'
  AND movement_goods.date <= '2024-10-14';

"""

result = cursor.execute(query).fetchone()[0]
print(f"Сумма: {result}")

conn.close()
