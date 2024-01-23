import csv
from pymongo import MongoClient
from bson import json_util
import json

def write_to_file(filename, data):
    with open(filename, 'w', encoding='utf-8') as json_file:
        json.dump(data, json_file, default=json_util.default, ensure_ascii=False)

client = MongoClient('localhost', 27017)
db = client['mydatabase']
collection_name = 'mycollection'
collection = db[collection_name]

file_path = 'task_1_item.csv'

with open(file_path, 'r', encoding='utf-8') as file:
    csv_reader = csv.DictReader(file, delimiter=';')
    data = list(csv_reader)

collection.delete_many({})
collection.insert_many(data)

min_age = 20  # Define the minimum age

# вывод первых 10 записей, отсортированных по убыванию по полю salary 
result_1 = list(collection.find({}, {'_id': 0, 'job': 1, 'salary': 1}).sort("salary", -1).limit(10))
write_to_file('result_1.json', result_1)

# вывод первых 15 записей, отфильтрованных по предикату age < 30, отсортировать по убыванию по полю salary 
result_2 = list(collection.find({"age": {"$lt": 30}}).sort("salary", -1).limit(15))
write_to_file('result_2.json', result_2)

# вывод первых 10 записей, отфильтрованных по сложному предикату: (записи только из произвольного города, записи только из трех произвольно взятых профессий), отсортировать по возрастанию по полю age 
result_3 = list(collection.find({
    "city": "Барселона",
    "job": {"$in": ["Инженер", "Врач", "Учитель"]}
}, {'_id': 0, 'job': 1, 'salary': 1, 'age': 1}).sort("age", 1).limit(10))
write_to_file('result_3.json', result_3)

# Вывод количества записей, удовлетворяющих условиям
result_4_count = collection.count_documents({
    "age": {"$gte": min_age, "$lte": 35},
    "year": {"$gte": 2019, "$lte": 2022},
    "$or": [
        {"salary": {"$gt": 50000, "$lte": 75000}},
        {"salary": {"$gt": 125000, "$lt": 150000}}
    ]
})
result_4 = {"count": result_4_count}
write_to_file('result_4.json', result_4)

client.close()