import csv
from collections import defaultdict

# Укажите путь к входному и выходному CSV-файлам
input_csv_file_path = 'slovnik.csv'
output_csv_file_path = 'word_totals.csv'

# Словарь для хранения суммы quantity для каждого слова
word_quantities = defaultdict(int)

# Чтение входного CSV-файла
with open(input_csv_file_path, mode='r', encoding='utf-8') as file:
    reader = csv.DictReader(file)
    for row in reader:
        try:
            word = row['word']
            quantity = int(row['quantity'])
            word_quantities[word] += quantity
        except ValueError:
            print(f"Ошибка преобразования строки: {row}")
        except KeyError:
            print("Проверьте, что файл содержит столбцы 'word' и 'quantity'")

# Запись итогов в новый CSV-файл
with open(output_csv_file_path, mode='w', encoding='utf-8', newline='') as file:
    writer = csv.writer(file)
    # Запись заголовка
    writer.writerow(['word', 'total_quantity'])
    # Запись данных
    for word, total_quantity in word_quantities.items():
        writer.writerow([word, total_quantity])

print(f"Итоговый файл сохранён как '{output_csv_file_path}'")
