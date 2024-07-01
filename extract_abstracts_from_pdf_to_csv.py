import pandas as pd
from collections import defaultdict
import re
from tika import parser

# use tika.parser to read the pdf file
raw = parser.from_file('./DatenBA_Arbeiten.pdf')

# extract the text content of the pdf
# some cleanup is needed (like removing leading / trailing whitespace, **'s and the document title)
content = raw['content'].replace('Microsoft Word - DatenBA_Arbeiten', '').strip().replace('**', '')

# finding topics (they are marked with ###)
topics = re.split(r'###\s*', content)

# somewhere to put the found abstracts, titles and stuff
topic_dict = defaultdict(list)

for topic in topics:
    if topic.strip():
        topic_lines = topic.strip().split('\n')
        topic_name = topic_lines[0].strip()
        current_subtopic = ""
        current_title = ""
        current_abstract = []

        for line in topic_lines[1:]:
            if re.match(r'####\s*.*', line.strip()):
                current_subtopic = line.strip()
            elif re.match(r'^\d+\.\s".*"$', line.strip()):
                if current_title and current_abstract:
                    topic_dict[topic_name].append({
                        'sub_topic': current_subtopic,
                        'title': current_title,
                        'abstract': ' '.join(current_abstract).strip()
                    })
                current_title = line.strip()
                current_abstract = []
            else:
                current_abstract.append(line.strip())

        if current_title and current_abstract:
            topic_dict[topic_name].append({
                # 'sub_topic': current_subtopic,
                'title': current_title,
                'abstract': ' '.join(current_abstract).strip()
            })

# Converting to DataFrame for better visualization
df_list = []
for topic, entries in topic_dict.items():
    for entry in entries:
        df_list.append({
            'Topic': topic,
            # 'Sub_Topic': entry['sub_topic'],
            'Title': entry['title'],
            'Abstract': entry['abstract']
        })

df = pd.DataFrame(df_list)
df.columns = [col.lower() for col in df.columns]

df.to_csv("extracted_abstracts.csv", index=False)
