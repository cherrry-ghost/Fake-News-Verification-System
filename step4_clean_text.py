import pandas as pd
import re
data=pd.read_csv("news.csv", encoding="latin1")
data = data[['text', 'label']]
def clean_text(text):
    text=text.lower()
    text=re.sub(r'[^a-zA-Z]', ' ', text)
    return text
data['text'] = data['text'].apply(clean_text)
print(data.head())