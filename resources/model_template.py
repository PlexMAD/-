import gensim
from gensim.models import Word2Vec
import pandas as pd
import re

# Регулярное выражение для очистки текста
patterns = "[!#$%&'()*+,./:;<=>?@[\]^_`{|}~—\"\-]+"

# Список для хранения очищенных ответов
response = []

# Чтение файла с очищенными текстами
with open('cleaned_texts_for_training.txt', encoding='utf-8') as f:
    lines = f.readlines()
    for line in lines:
        # Удаление лишних символов из текста
        response.append(re.sub(patterns, ' ', line.strip()))

# Создание DataFrame
data = pd.DataFrame(list(zip(response)))
data.columns = ['response']

# Препроцессинг текста с помощью gensim
response_base = data.response.apply(gensim.utils.simple_preprocess)

# Создание модели Word2Vec
model = Word2Vec(
    sentences=response_base,
    min_count=10,         # Минимальное количество встречающихся слов
    window=5,             # Размер окна
    vector_size=100,      # Размерность векторного представления
    alpha=0.03,           # Начальная скорость обучения
    negative=15,          # Количество отрицательных примеров
    min_alpha=0.0007,     # Минимальная скорость обучения
    sample=6e-5           # Порог для downsampling частых слов
)

# Обучение модели
model.build_vocab(response_base, update=True)
model.train(response_base, total_examples=model.corpus_count, epochs=model.epochs)

# Вывод информации о модели
print("Количество предложений в корпусе:", model.corpus_count)
print("Слово 'направление' есть в словаре?", model.wv.has_index_for("направление"))

# Пример работы модели
similar_words = model.wv.similar_by_vector(model.wv['направление'])  # Найти похожие слова на "направление"
print("Слова, похожие на 'направление':", similar_words)

# Сохранение модели
model.save("model_university_topic.model")

# Пример нахождения наиболее похожего слова
most_similar = model.wv.most_similar_to_given("обучение", ["направление", "преподаватель"])
print("Наиболее похожее слово на 'обучение' среди ['направление', 'преподаватель']:", most_similar)
