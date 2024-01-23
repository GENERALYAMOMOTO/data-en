import sqlite3
import pandas as pd
import json

# Название базы данных
db_name = "1.2.db"
# Название файла с данными
file_name = "task_1_var_45_item.csv"
# Название таблицы в базе данных

# Создаем подключение к базе данных
conn = sqlite3.connect(db_name)
cursor = conn.cursor()

# Читаем данные из файла CSV и записываем их в базу данных
df = pd.read_csv(file_name, sep=';')  # Указываем точку с запятой как разделитель
df.to_sql('addresses', conn, if_exists='replace', index=False)

# Запрос 1: вывод первых (45+10) отсортированных по полю views в файл формата json
query1 = f'SELECT * FROM addresses ORDER BY views LIMIT {45 + 10}'
result1 = pd.read_sql(query1, conn)
result1.to_json("output1.json", orient='records', lines=True, force_ascii=False)

# Запрос 2: вывод (сумму, мин, макс, среднее) по полю prob_price
query2 = 'SELECT SUM(prob_price) AS sum_prob_price, MIN(prob_price) AS min_prob_price, MAX(prob_price) AS max_prob_price, AVG(prob_price) AS avg_prob_price FROM addresses'
result2 = pd.read_sql(query2, conn)
result2.to_json("output2.json", orient='records', lines=True, force_ascii=False)

# Запрос 3: вывод частоты встречаемости для категориального поля parking
query3 = 'SELECT parking, COUNT(*) AS frequency FROM addresses GROUP BY parking'
result3 = pd.read_sql(query3, conn)
result3.to_json("output3.json", orient='records', lines=True, force_ascii=False)

# Запрос 4: вывод первых (45+10) отфильтрованных по условию "street = Морская улица 28" отсортированных по полю views в файл формата json
query4 = f'SELECT * FROM addresses WHERE street = "Киевская улица 16" ORDER BY views LIMIT {45 + 10}'
result4 = pd.read_sql(query4, conn)
result4.to_json("output4.json", orient='records', lines=True, force_ascii=False)

# Закрываем соединение с базой данных
conn.close()