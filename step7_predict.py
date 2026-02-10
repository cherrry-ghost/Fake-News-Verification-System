import pandas as pd
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

# Step 1: Load and clean data
data = pd.read_csv("real_fake_news.csv", encoding="latin1")
data = data[['text', 'label']]

def clean_text(text):
    text = text.lower()
    text = re.sub(r'[^a-zA-Z]', ' ', text)
    return text

data['text'] = data['text'].apply(clean_text)

# Step 2: Vectorize text
vectorizer = TfidfVectorizer(stop_words='english')
X = vectorizer.fit_transform(data['text'])
y = data['label']

# Step 3: Train model
model = LogisticRegression()
model.fit(X, y)

# Step 4: Predict new input
while True:
    news = input("\nEnter news text (or type 'exit' to quit):\n")
    if news.lower() == 'exit':
        break
    news_clean = clean_text(news)
    news_vector = vectorizer.transform([news_clean])
    prediction = model.predict(news_vector)
    print("Prediction:", prediction[0])
