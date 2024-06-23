import pandas as pd
import re
from collections import defaultdict

import os


def file_exists(file_path):
    """Checks if the specified file exists.
    Args:
        file_path (str): The path of the file to check.
    Returns:
        bool: True if the file exists, False otherwise.
    """
    return os.path.isfile(file_path)


if not file_exists('generated_abstracts_text.txt'):
    from tika import parser

    if not file_exists('DatenBA_Arbeiten.pdf'):
        raise OSError('Either the PDF is missing or misnamed.')
    raw = parser.from_file('./DatenBA_Arbeiten.pdf')

    content = raw['content']

    with open('generated_abstracts_text.txt', 'w') as file:
        file.write(content)

    file.close()

with open('generated_abstracts_text.txt', 'r') as file:
    text = file.read()

# Splitting the text into sections based on the topics marked with ###
topics = re.split(r'###\s*', text)
topic_dict = defaultdict(list)

for topic in topics:
    if topic.strip():
        topic_lines = topic.strip().split('\n')
        topic_name = topic_lines[0].strip()
        current_title = ""
        current_abstract = []
        for line in topic_lines[1:]:
            if re.match(r'^\d+\.\s".*"$', line.strip()):
                if current_title and current_abstract:
                    topic_dict[topic_name].append(
                        {'title': current_title, 'abstract': ' '.join(current_abstract).strip()})
                current_title = line.strip()
                current_abstract = []
            else:
                current_abstract.append(line.strip())
        if current_title and current_abstract:
            topic_dict[topic_name].append({'title': current_title, 'abstract': ' '.join(current_abstract).strip()})


# Converting to DataFrame for better visualization
df_list = []
for topic, entries in topic_dict.items():
    for entry in entries:
        df_list.append({'Topic': topic, 'Title': entry['title'], 'Abstract': entry['abstract']})

df = pd.DataFrame(df_list)


df.to_csv('extracted_abstracts.csv', index=False)
