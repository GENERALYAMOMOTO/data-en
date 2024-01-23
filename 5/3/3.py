from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client['mydatabase']

collection_name = 'mycollection'
collection = db[collection_name]

file_path_task_3 = 'task_3_item.text'  # Replace with your file path

with open(file_path_task_3, 'r', encoding='utf-8') as file_task_3:
    text_data = file_task_3.read()

# Split text into records
records = text_data.strip().split("=====")

data_task_3 = []
for record in records:
    # Split record into lines and create a dictionary
    record_dict = dict(item.split("::") for item in record.strip().split("\n"))

    # Convert types
    record_dict['age'] = int(record_dict['age'])
    record_dict['year'] = int(record_dict['year'])
    record_dict['id'] = int(record_dict['id'])
    record_dict['salary'] = int(record_dict['salary'])

    data_task_3.append(record_dict)

# Insert data into MongoDB
collection.insert_many(data_task_3)

# 1. Delete documents with salary less than 25000 or greater than 175000
collection.delete_many({"$or": [{"salary": {"$lt": 25000}}, {"salary": {"$gt": 175000}}]})

# 2. Increment age for all documents
collection.update_many({}, {"$inc": {"age": 1}})

# 3. Multiply salary by 1.05 for selected professions
selected_professions = ["Программист", "Врач", "Учитель"]
collection.update_many({"profession": {"$in": selected_professions}},
                       {"$mul": {"salary": 1.05}})

# 4. Multiply salary by 1.07 for selected cities
selected_cities = ["Загреб", "Санкт-Петербург", "Вроцлав"]
collection.update_many({"city": {"$in": selected_cities}},
                       {"$mul": {"salary": 1.07}})

# 5. Multiply salary by 1.10 for documents matching the complex predicate
complex_predicate_filter = {
    "city": "Махадаонда",
    "job": {"$in": ["Инженер", "Программист", "Психолог"]},
    "age": {"$gte": 30, "$lte": 50}
}
collection.update_many(complex_predicate_filter, {"$mul": {"salary": 1.10}})

# 6. Delete documents with year less than 2010
random_predicate_filter = {"year": {"$lt": 2010}}
collection.delete_many(random_predicate_filter)

client.close()