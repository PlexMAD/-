import re

# Путь к входному файлу
input_file = 'vk_questions.txt'  # Замените на фактический путь к вашему файлу
output_file = 'cleaned_texts_for_training.txt'

# Регулярное выражение для очистки текста
patterns = r"[!#$%&'()*+,./:;<=>?@\[\]^_`{|}~—\"\"\-]+"  # Удаляем лишние символы
extra_spaces = r"\s+"  # Убираем лишние пробелы

# Список для очищенных сообщений
cleaned_texts = []

# Обработка файла
with open(input_file, 'r', encoding='utf-8') as f:
    for line in f:
        # Убираем лишние пробелы и символы новой строки
        line = line.strip()
        # Проверяем наличие текста (последняя колонка после запятых или кавычек)
        if ',' in line:
            # Разбиваем строку по первому разделителю `,` и извлекаем текст сообщения
            parts = line.split(',', 2)  # Разделяем только на 3 части: индекс, время, текст
            if len(parts) == 3:
                text = parts[2]  # Текст сообщения
                # Удаляем лишние символы из текста
                cleaned_text = re.sub(patterns, ' ', text)
                cleaned_text = re.sub(extra_spaces, ' ', cleaned_text).strip()
                # Добавляем только непустые сообщения
                if cleaned_text:
                    cleaned_texts.append(cleaned_text)

# Сохраняем очищенные данные в новый файл
with open(output_file, 'w', encoding='utf-8') as f:
    f.write("\n".join(cleaned_texts))  # Каждая строка сохраняется в отдельной строке

print(f"Файл подготовлен для обучения модели и сохранён как {output_file}.")
