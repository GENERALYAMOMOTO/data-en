import csv
import json
from pymongo import MongoClient
from bson import ObjectId

# Подключение к MongoDB
client = MongoClient('localhost', 27017)
db = client['movies']
collection = db['films']

# Загрузка данных из CSV
with open('data.csv', 'r', encoding='utf-8') as csv_file:
    csv_reader = csv.DictReader(csv_file)
    films_csv = [film for film in csv_reader]

# Загрузка данных из JSON
with open('data.json', 'r', encoding='utf-8') as json_file:
    films_json = json.load(json_file)

# Преобразование строковых значений 'Rating' в числа
for film in films_csv + films_json:
    rating_str = film['Rating']
    try:
        rating_float = float(rating_str)
        film['Rating'] = rating_float
    except ValueError:
        print(f"Skipping document with non-numeric rating: {film}")

# Вставка данных в MongoDB
collection.insert_many(films_csv + films_json)

# Выполнение запросов

# Задание 1: Выборка
result_selection = collection.find({"Genre": "Drama"})
result_selection_drama = list(result_selection)
for doc in result_selection_drama:
    doc['_id'] = str(doc['_id'])

with open('result_selection_drama.json', 'w', encoding='utf-8') as result_file:
    json.dump(result_selection_drama, result_file, ensure_ascii=False, indent=2)

result_selection = collection.find({"Title": "Inception"})
result_selection_inception = list(result_selection)
for doc in result_selection_inception:
    doc['_id'] = str(doc['_id'])

with open('result_selection_inception.json', 'w', encoding='utf-8') as result_file:
    json.dump(result_selection_inception, result_file, ensure_ascii=False, indent=2)

result_selection = collection.find({"Year": 1994})
result_selection_1994 = list(result_selection)
for doc in result_selection_1994:
    doc['_id'] = str(doc['_id'])

with open('result_selection_1994.json', 'w', encoding='utf-8') as result_file:
    json.dump(result_selection_1994, result_file, ensure_ascii=False, indent=2)

result_selection = collection.find({"Director": "Christopher Nolan"})
result_selection_nolan = list(result_selection)
for doc in result_selection_nolan:
    doc['_id'] = str(doc['_id'])

with open('result_selection_nolan.json', 'w', encoding='utf-8') as result_file:
    json.dump(result_selection_nolan, result_file, ensure_ascii=False, indent=2)

result_selection = collection.find({"Rating": {"$gte": 9.0}})
result_selection_rating = list(result_selection)
for doc in result_selection_rating:
    doc['_id'] = str(doc['_id'])

with open('result_selection_rating.json', 'w', encoding='utf-8') as result_file:
    json.dump(result_selection_rating, result_file, ensure_ascii=False, indent=2)

# Задание 2: Выбор с агрегацией
result_aggregation_genre = collection.aggregate([
    {"$group": {"_id": "$Genre", "avgRating": {"$avg": "$Rating"}}}
])
result_aggregation_genre_list = list(result_aggregation_genre)
for doc in result_aggregation_genre_list:
    doc['_id'] = str(doc['_id'])

with open('result_aggregation_genre.json', 'w', encoding='utf-8') as result_file:
    json.dump(result_aggregation_genre_list, result_file, ensure_ascii=False, indent=2)

result_aggregation_year = collection.aggregate([
    {"$group": {"_id": "$Year", "count": {"$sum": 1}}}
])
result_aggregation_year_list = list(result_aggregation_year)
for doc in result_aggregation_year_list:
    doc['_id'] = str(doc['_id'])

with open('result_aggregation_year.json', 'w', encoding='utf-8') as result_file:
    json.dump(result_aggregation_year_list, result_file, ensure_ascii=False, indent=2)

result_aggregation_director = collection.aggregate([
    {"$group": {"_id": "$Director", "totalRating": {"$sum": "$Rating"}}}
])
result_aggregation_director_list = list(result_aggregation_director)
for doc in result_aggregation_director_list:
    doc['_id'] = str(doc['_id'])

with open('result_aggregation_director.json', 'w', encoding='utf-8') as result_file:
    json.dump(result_aggregation_director_list, result_file, ensure_ascii=False, indent=2)

result_aggregation_top_rated = collection.find().sort([("Rating", -1)]).limit(1)
result_aggregation_top_rated_list = list(result_aggregation_top_rated)
for doc in result_aggregation_top_rated_list:
    doc['_id'] = str(doc['_id'])

with open('result_aggregation_top_rated.json', 'w', encoding='utf-8') as result_file:
    json.dump(result_aggregation_top_rated_list, result_file, ensure_ascii=False, indent=2)

result_aggregation_year_avg_rating = collection.aggregate([
    {"$group": {"_id": "$Year", "avgRating": {"$avg": "$Rating"}}}
])
result_aggregation_year_avg_rating_list = list(result_aggregation_year_avg_rating)
for doc in result_aggregation_year_avg_rating_list:
    doc['_id'] = str(doc['_id'])

with open('result_aggregation_year_avg_rating.json', 'w', encoding='utf-8') as result_file:
    json.dump(result_aggregation_year_avg_rating_list, result_file, ensure_ascii=False, indent=2)

# Задание 3: Обновление/удаление данных

# Обновление документов с числовым полем "Rating"
collection.update_many({"Rating": {"$type": "double"}}, {"$inc": {"Rating": 0.5}})

# Обновление других конкретных документов
collection.update_one({"Title": "Inception"}, {"$set": {"Rating": 9.5}})
collection.update_many({"Director": "Christopher Nolan"}, {"$set": {"Year": 2022}})

# Удаление конкретных документов
collection.delete_one({"Title": "Pulp Fiction"})

# Увеличение "Rating" для документов с "Genre" равным "Action"
collection.update_many({"Genre": "Action", "Rating": {"$type": "double"}}, {"$inc": {"Rating": 0.5}})

# Удаление документов с "Director" равным "Christopher Nolan"
collection.delete_many({"Director": "Christopher Nolan"})

# Закрытие подключения
client.close()
