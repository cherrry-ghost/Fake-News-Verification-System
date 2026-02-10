import pandas as pd
import re
import nltk
import pickle

from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score

nltk.download("stopwords")

# Load stopwords ONCE (fast)
STOPWORDS = set(stopwords.words("english"))

def clean_text(text):
    text = str(text).lower()
    text = re.sub(r"http\S+", "", text)
    text = re.sub(r"[^a-z\s]", "", text)
    words = text.split()
    return " ".join(w for w in words if w not in STOPWORDS)

def train_model():
    print("Loading datasets...")
    fake = pd.read_csv("fake.csv")
    true = pd.read_csv("true.csv")

    fake["label"] = 0
    true["label"] = 1

    data = pd.concat([fake, true], axis=0)

    # 🔥 LIMIT DATA SIZE (FAST MODE)
    data = data.sample(10000, random_state=42)

    print("Rows used for training:", len(data))

    print("Cleaning text...")
    data["clean_text"] = data["text"].apply(clean_text)

    print("Vectorizing text...")
    X = data["clean_text"]
    y = data["label"]

    vectorizer = TfidfVectorizer(max_features=2000)
    X_vectorized = vectorizer.fit_transform(X)

    print("Splitting data...")
    X_train, X_test, y_train, y_test = train_test_split(
        X_vectorized, y, test_size=0.2, random_state=42
    )

    print("Training model...")
    model = LogisticRegression(max_iter=1000)
    model.fit(X_train, y_train)

    print("Testing model...")
    accuracy = accuracy_score(y_test, model.predict(X_test))
    print("Model Accuracy:", accuracy)

    print("Saving model...")
    with open("model.pkl", "wb") as f:
        pickle.dump(model, f)

    with open("vectorizer.pkl", "wb") as f:
        pickle.dump(vectorizer, f)

    print("DONE ✅ Model and vectorizer saved")

if __name__ == "__main__":
    train_model()
