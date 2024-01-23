import sqlite3
import pandas as pd
import json

# Название базы данных
db_name = "1.2.db"
# Название файла с данными для addresses_info
file_name_info = "task_2_var_45_subitem.csv"
# Название таблицы addresses_info
table_name_info = "addresses_info"
# Название файла для записи результата первого запроса
output_file_1 = "output_query_1.json"
# Название файла для записи результата второго запроса
output_file_2 = "output_query_2.json"
# Название файла для записи результата третьего запроса
output_file_3 = "output_query_3.json"

# Создаем подключение к базе данных
conn = sqlite3.connect(db_name)
cursor = conn.cursor()

# Создаем таблицу addresses_info
create_table_query = '''
CREATE TABLE IF NOT EXISTS addresses_info (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    rating INTEGER,
    convenience INTEGER,
    security INTEGER,
    functionality INTEGER,
    comment TEXT,
    FOREIGN KEY (name) REFERENCES addresses(name)
);
'''
cursor.execute(create_table_query)

# Читаем данные из файла CSV и записываем их в таблицу addresses_info
df_info = pd.read_csv(file_name_info, sep=';')
df_info.to_sql(table_name_info, conn, if_exists='replace', index=False)

# Запрос 1
query1 = 'SELECT * FROM addresses_info WHERE rating = 5;'
result1 = pd.read_sql(query1, conn)
result1.to_json(output_file_1, orient='records', lines=True, force_ascii=False)

# Запрос 2
query2 = 'SELECT name, comment FROM addresses_info WHERE security > 4;'
result2 = pd.read_sql(query2, conn)
result2.to_json(output_file_2, orient='records', lines=True, force_ascii=False)

# Запрос 3
query3 = 'SELECT DISTINCT a.name FROM addresses a JOIN addresses_info ai ON a.name = ai.name;'
result3 = pd.read_sql(query3, conn)
result3.to_json(output_file_3, orient='records', lines=True, force_ascii=False)

# Закрываем соединение с базой данных
conn.close()