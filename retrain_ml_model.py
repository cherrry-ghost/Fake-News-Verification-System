# retrain_ml_model_auto.py

import pandas as pd
import re
import nltk
import pickle
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score

# ---------------------------
# NLTK stopwords
# ---------------------------
nltk.download("stopwords")
STOP_WORDS = set(stopwords.words("english"))

# ---------------------------
# Text cleaning function
# ---------------------------
def clean_text(text):
    text = str(text).lower()
    text = re.sub(r"http\S+|www\S+", "", text)
    text = re.sub(r"[^a-z\s]", "", text)
    words = text.split()
    words = [w for w in words if w not in STOP_WORDS]
    return " ".join(words)

# ---------------------------
# Load existing datasets
# ---------------------------
print("Loading datasets...")
fake_df = pd.read_csv("data/fake.csv")
true_df = pd.read_csv("data/true.csv")

# ---------------------------
# Automatic new real news
# ---------------------------
new_true_news = [
    {
        "title": "NASA Telescope Captures Distant Galaxies",
        "text": "NASA confirmed that the James Webb Space Telescope captured images of distant galaxies in unprecedented detail.",
        "subject": "scienceNews",
        "date": "February 1, 2026"
    },
    {
        "title": "Supreme Court Rules on Environmental Regulations",
        "text": "The Supreme Court of India announced a new ruling on environmental regulations in 2020.",
        "subject": "politicsNews",
        "date": "March 15, 2020"
    },
    {
        "title": "Ministry of Health Updates Vaccination Program",
        "text": "According to the Ministry of Health, nationwide vaccination programs will continue throughout 2024 to ensure public safety.",
        "subject": "healthNews",
        "date": "January 20, 2024"
    },
    {
        "title": "Ministry of Finance Considers Digital Currency",
        "text": "According to the Ministry of Finance, a new digital currency may be introduced in 2025 as part of economic modernization.",
        "subject": "economyNews",
        "date": "June 10, 2025"
    },
    {
        "title": "Breakthrough in Quantum Computing Announced",
        "text": "Researchers at MIT announced a breakthrough in quantum computing that could revolutionize data processing and cryptography.",
        "subject": "scienceNews",
        "date": "November 5, 2023"
    },
    {
        "title": "WHO Issues Global Health Advisory",
        "text": "The World Health Organization issued a global health advisory regarding the spread of a new influenza variant.",
        "subject": "healthNews",
        "date": "October 12, 2023"
    },
    {
        "title": "New Renewable Energy Policy Introduced",
        "text": "The government introduced a new renewable energy policy aimed at increasing solar and wind power production by 2030.",
        "subject": "politicsNews",
        "date": "August 18, 2024"
    },
    {
        "title": "AI Breakthrough Achieves Natural Language Understanding",
        "text": "A team of AI researchers achieved a significant advancement in natural language understanding, improving machine comprehension of human text.",
        "subject": "techNews",
        "date": "December 2, 2023"
    }
]

new_true_df = pd.DataFrame(new_true_news)

# ---------------------------
# Label datasets
# ---------------------------
fake_df["label"] = 0
true_df["label"] = 1
new_true_df["label"] = 1

# Combine all true and fake news
data = pd.concat([fake_df, true_df, new_true_df], ignore_index=True)
print(f"Total rows after adding new real news: {len(data)}")

# ---------------------------
# Clean text
# ---------------------------
print("Cleaning text...")
data["clean_text"] = data["text"].apply(clean_text)

# ---------------------------
# TF-IDF Vectorizer
# ---------------------------
print("Vectorizing text...")
vectorizer = TfidfVectorizer(max_features=6000, ngram_range=(1,2))
X = vectorizer.fit_transform(data["clean_text"])
y = data["label"]

# ---------------------------
# Train-test split
# ---------------------------
print("Splitting data...")
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# ---------------------------
# Train Logistic Regression model
# ---------------------------
print("Training ML model...")
model = LogisticRegression(max_iter=2000)
model.fit(X_train, y_train)

# ---------------------------
# Evaluate model
# ---------------------------
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print(f"ML Model Accuracy: {accuracy:.4f}")

# ---------------------------
# Save model & vectorizer
# ---------------------------
with open("models/model.pkl", "wb") as f:
    pickle.dump(model, f)

with open("models/vectorizer.pkl", "wb") as f:
    pickle.dump(vectorizer, f)

print("Model and vectorizer saved successfully ✅")
