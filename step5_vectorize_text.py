import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer

# Step 1: Load cleaned data
data = pd.read_csv("news.csv", encoding="latin1")

# Step 2: Keep only required columns
data = data[['text', 'label']]

# Step 3: Create TF-IDF vectorizer
vectorizer = TfidfVectorizer(stop_words='english')

# Step 4: Convert text to numbers
X_vectorized = vectorizer.fit_transform(data['text'])

# Step 5: Check result
print("Vectorization completed!")
print("Shape of vectorized data:", X_vectorized.shape)
