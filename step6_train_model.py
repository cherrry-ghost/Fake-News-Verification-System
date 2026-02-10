import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score

# Step 1: Load data
data = pd.read_csv("real_fake_news.csv", encoding="latin1")
data = data[['text', 'label']]

# Step 2: Clean text
import re
def clean_text(text):
    text = text.lower()
    text = re.sub(r'[^a-zA-Z]', ' ', text)
    return text
data['text'] = data['text'].apply(clean_text)

# Step 3: Convert text to numbers
vectorizer = TfidfVectorizer(stop_words='english')
X = vectorizer.fit_transform(data['text'])
y = data['label']

# Step 4: Split data into train and test sets
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Step 5: Train Logistic Regression model
model = LogisticRegression()
model.fit(X_train, y_train)

# Step 6: Make predictions
y_pred = model.predict(X_test)

# Step 7: Evaluate accuracy
accuracy = accuracy_score(y_test, y_pred)
print("Model training completed!")
print("Accuracy on test data:", accuracy)
