📰 Fake News Verification System
📌 Project Description

This project is a Fake News Verification System that determines whether a given news article is REAL or FAKE using a hybrid approach:

Rule-based fact checking

Machine Learning-based classification

The system combines both results to produce a final decision.

⚙️ Technologies Used

Python

Pandas

Scikit-learn

NLTK

TF-IDF Vectorization

Logistic Regression

🧠 System Architecture
User Input
   ↓
Rule-Based Verification
   ↓
ML Fake News Detection
   ↓
Final Decision Logic

🔍 Phase 1: Rule-Based Verification

Detects sensational words

Checks credibility indicators

Flags suspicious patterns

Produces an initial judgment

🤖 Phase 2: Machine Learning Detection

Converts text into numerical features using TF-IDF

Trained using labeled real and fake news datasets

Uses Logistic Regression for classification

Outputs prediction confidence

✅ Final Decision Logic

Combines rule-based and ML results

Outputs one of the following:

LIKELY REAL

LIKELY FAKE

NEEDS MANUAL VERIFICATION

▶️ How to Run the Project
1. Activate virtual environment
.venv\Scripts\activate

2. (First time only) Train ML model
python phase2_ml_model.py

3. Run the application
python main.py

🧪 Example Output
Rule-based Check : LIKELY REAL
ML Prediction   : UNCERTAIN

FINAL DECISION  : LIKELY REAL

🎯 Conclusion

This system demonstrates how combining rule-based logic with machine learning improves fake news detection accuracy and reliability.