import csv
import pandas as pd
import matplotlib.pyplot as plt
import os
from fpdf import FPDF

# Укажите путь к входному файлу CSV
input_csv_file_path = 'slovnik.csv'

# Укажите папку для сохранения диаграмм
output_plots_folder = 'plots'
if not os.path.exists(output_plots_folder):
    os.makedirs(output_plots_folder)

# Чтение данных из CSV-файла
data = pd.read_csv(input_csv_file_path)

# Преобразуем данные в таблицу с динамикой изменений
pivot_table = data.pivot_table(index='word', columns='day', values='quantity', aggfunc='sum', fill_value=0)

# Убедимся, что все значения в таблице числовые
pivot_table = pivot_table.apply(pd.to_numeric, errors='coerce').fillna(0)

# Добавляем столбец с общей частотой для каждого слова
pivot_table['Total_Frequency'] = pivot_table.sum(axis=1)

# Сортируем слова по общей частоте (от большего к меньшему)
pivot_table = pivot_table.sort_values(by='Total_Frequency', ascending=False)

# Удаляем столбец с общей частотой для построения диаграмм
pivot_table = pivot_table.drop(columns=['Total_Frequency'])

# Добавляем строку с общей суммой за каждый день
pivot_table.loc['Total'] = pivot_table.sum()

# Сохраняем таблицу в CSV-файл
pivot_table.to_csv('word_frequency_dynamic.csv', encoding='utf-8')

# Построение диаграмм для первых 50 слов
for word in list(pivot_table.index)[:50]:
    if word == 'Total':
        continue  # Пропускаем итоговую строку
    plt.figure()
    plt.plot(pivot_table.columns, pivot_table.loc[word], marker='o')
    plt.title(f'Изменение частоты слова: {word}')
    plt.xlabel('День')
    plt.ylabel('Частота')
    plt.grid()
    plt.savefig(os.path.join(output_plots_folder, f'{word}_frequency_plot.png'))
    plt.close()

# Построение диаграммы общей частоты слов за каждый день
plt.figure()
plt.plot(pivot_table.columns, pivot_table.loc['Total'], marker='o', color='red')
plt.title('Общая частота слов за каждый день')
plt.xlabel('День')
plt.ylabel('Общая частота')
plt.grid()
plt.savefig(os.path.join(output_plots_folder, 'total_frequency_plot.png'))
plt.close()

# Объединение диаграмм в один файл PDF
pdf = FPDF()
pdf.set_auto_page_break(auto=True, margin=15)

# Use built-in Arial font without loading the TTF file
pdf.set_font("Arial", size=12)

# Define a helper function to escape non-latin characters
def unicode_escape(text):
    try:
        return text.encode('latin-1').decode('latin-1')
    except UnicodeEncodeError:
        return ''.join([f'\\u{ord(c):04x}' if ord(c) > 255 else c for c in text])

# Добавляем диаграммы по каждому слову
for word in list(pivot_table.index)[:50]:
    if word == 'Total':
        continue
    pdf.add_page()
    word_safe = unicode_escape(f'Изменение частоты слова: {word}')
    pdf.cell(200, 10, txt=word_safe, ln=True, align='C')
    pdf.image(os.path.join(output_plots_folder, f'{word}_frequency_plot.png'), x=10, y=30, w=180)

# Добавляем общую диаграмму
pdf.add_page()
pdf.set_font("Arial", size=12)
pdf.cell(200, 10, txt='Общая частота слов за каждый день', ln=True, align='C')
pdf.image(os.path.join(output_plots_folder, 'total_frequency_plot.png'), x=10, y=30, w=180)

# Сохраняем PDF
pdf.output("word_frequency_report.pdf")

print("Готово! Таблица сохранена в 'word_frequency_dynamic.csv', диаграммы сохранены в папке 'plots', объединены в 'word_frequency_report.pdf'.")
