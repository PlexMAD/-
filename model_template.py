import gensim
from gensim.models import Word2Vec
import pandas as pd
import re

patterns = "[!#$%&'()*+,./:;<=>?@[\]^_`{|}~—\"\-]+"

response = []
with open('resources/dataset.txt', encoding='latin-1') as f:
#with open('resources/dataset.txt') as f:
    lines = f.readlines()
    columns = lines[0].split('\t')
    for line in lines[1:]:
        temp = line.split('\t')
        response.append(re.sub(patterns, ' ', temp[0]))

data = pd.DataFrame(list(zip(response)))
data.columns = ['response']
response_base = data.response.apply(gensim.utils.simple_preprocess)

model = Word2Vec(
    sentences=response_base,
    min_count=10,
    window=2,
    vector_size=16,
    alpha=0.03,
    negative=15,
    min_alpha=0.0007,
    sample=6e-5
)

# Train the model
model.build_vocab(response_base, update=True)
model.train(response_base, total_examples=model.corpus_count, epochs=model.epochs)


print(model.corpus_count)
print(model.wv.has_index_for("СЛОВО"))

print(model.wv.similar_by_vector(model.wv['СЛОВО']))

model.save("resources/model_med_НАЗВАНИЕ_ПОДКАТЕГОРИИ.model")

print(model.corpus_count)
print(model.wv.most_similar_to_given("слово_1", ["слово_2", "слово_3"]))