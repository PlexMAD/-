import os
import re

def clean_text(text):
    return re.sub(r'[^A-Za-zА-Яа-я\s]', '', text)

def split_into_files(input_file, output_dir, num_files=7):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    with open(input_file, 'r', encoding='utf-8') as file:
        content = file.read()
    
    cleaned_content = clean_text(content)
    words = cleaned_content.split()
    chunk_size = len(words) // num_files

    for i in range(num_files):
        start = i * chunk_size
        end = None if i == num_files - 1 else (i + 1) * chunk_size
        chunk = words[start:end]
        output_path = os.path.join(output_dir, f'output_{i + 1}.txt')
        
        with open(output_path, 'w', encoding='utf-8') as output_file:
            output_file.write(' '.join(chunk))

input_file = 'vk_questions.txt' 
output_dir = 'output_files' 
split_into_files(input_file, output_dir)
