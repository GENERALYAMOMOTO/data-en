import csv

result = []
file_name = 'text_4_var_45'
with open(file_name, encoding='utf-8') as file:
    reader = csv.reader(file)
    count = 0
    sum = 0
    for row in reader:
        sum += int(row[4][0:-1])
        count += 1
        result.append((row[0], row[1] + ' ' + row[2], int(row[3]), row[4]))
    avg_salary = sum / count
    filtered_result = [item for item in result if int(item[3][0:-1]) >= avg_salary and item[2] > (25 + 11 % 10)]  # 11 вариант
    filtered_result.sort(key=lambda x: int(x[0]))

with open(f"result_{file_name}", 'w', encoding='utf-8', newline='') as res_csv:
    csv_writer = csv.writer(res_csv)
    for row in filtered_result:
        csv_writer.writerow(row)