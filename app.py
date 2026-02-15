import streamlit as st
import pickle
import re
import nltk
from nltk.corpus import stopwords
from nlp.entity_extractor import extract_entities
from nlp.fact_checker import wikipedia_verify

# ---------------------------
# Setup
# ---------------------------
nltk.download("stopwords")
STOP_WORDS = set(stopwords.words("english"))

with open("models/model.pkl", "rb") as f:
    model = pickle.load(f)

with open("models/vectorizer.pkl", "rb") as f:
    vectorizer = pickle.load(f)

# ---------------------------
# Text cleaning
# ---------------------------
def clean_text(text):
    text = text.lower()
    text = re.sub(r"http\\S+|www\\S+", "", text)
    text = re.sub(r"[^a-z\\s]", "", text)
    words = [w for w in text.split() if w not in STOP_WORDS]
    return " ".join(words)

# ---------------------------
# Rule-based checker
# ---------------------------
def rule_based_check(text):
    text_lower = text.lower()
    fake_signals = [
        "breaking", "shocking", "secret", "share this",
        "before it gets deleted", "revealed", "click here"
    ]
    real_signals = [
        "official statement", "ministry", "government",
        "according to", "press release", "court", "reported by"
    ]

    fake_score = sum(1 for f in fake_signals if f in text_lower)
    real_score = sum(1 for r in real_signals if r in text_lower)

    if fake_score >= 2 and fake_score > real_score:
        return "LIKELY FAKE"
    elif real_score >= 2 and real_score > fake_score:
        return "LIKELY REAL"
    else:
        return "UNCERTAIN"

# ---------------------------
# ML prediction
# ---------------------------
def ml_prediction(text):
    cleaned = clean_text(text)
    vectorized = vectorizer.transform([cleaned])

    # Get probabilities
    probs = model.predict_proba(vectorized)[0]
    classes = model.classes_

    # Map probabilities safely by class label
    prob_dict = dict(zip(classes, probs))

    # Adjust depending on how you trained:
    # If your training used 0 = FAKE and 1 = REAL
    prob_fake = prob_dict.get(0, 0)
    prob_real = prob_dict.get(1, 0)

    # --- Decision Logic ---
    confidence_gap = abs(prob_real - prob_fake)

    if confidence_gap < 0.10:
        label = "UNCERTAIN"
    elif prob_real > prob_fake:
        label = "LIKELY REAL"
    else:
        label = "LIKELY FAKE"

    return label, float(prob_fake), float(prob_real)

# ---------------------------
# Final decision
# ---------------------------
def final_decision(rule_result, ml_result, entities, text):
    ml_label, fake_conf, real_conf = ml_result
    wiki_flags = []

    for _, entity_list in entities.items():
        for e in entity_list:
            exists, similarity, _ = wikipedia_verify(e, text)
            wiki_flags.append((e, exists, similarity))

    verified_entities = [e for e, exists, _ in wiki_flags if exists]

    if verified_entities and rule_result != "LIKELY FAKE":
        decision = "LIKELY REAL ✅ (Verified factual entities)"
    elif rule_result == "LIKELY FAKE" and ml_label == "LIKELY FAKE" and fake_conf >= 0.85:
        decision = "LIKELY FAKE ⚠️ (Strong fake signals)"
    elif ml_label == "LIKELY FAKE" and fake_conf >= 0.80:
        decision = "LIKELY FAKE ⚠️ (ML confident)"
    elif ml_label == "LIKELY REAL" and real_conf >= 0.80:
        decision = "LIKELY REAL ✅ (ML confident)"
    elif rule_result != "UNCERTAIN":
        decision = rule_result + " (Rule-based)"
    else:
        decision = "UNCERTAIN ⚠️"

    return decision, wiki_flags

# ---------------------------
# STREAMLIT UI
# ---------------------------
st.set_page_config(page_title="Fake News Detector", layout="centered")

st.title("📰 Fake News Detection Web App")
st.write("Paste a news article below and click Analyze.")

news_text = st.text_area("News Text", height=220)

if st.button("Analyze"):
    if len(news_text.split()) < 10:
        st.warning("Please enter a longer news article.")
    else:
        entities = extract_entities(news_text)
        rule_result = rule_based_check(news_text)
        ml_result = ml_prediction(news_text)
        final, wiki_flags = final_decision(rule_result, ml_result, entities, news_text)

        st.subheader("Final Decision")
        if "REAL" in final:
            st.success(final)
        elif "FAKE" in final:
            st.error(final)
        else:
            st.warning(final)

        st.subheader("Analysis Details")
        st.write(f"Rule-based result: **{rule_result}**")
        st.write(f"ML prediction: **{ml_result[0]}**")
        st.write(f"ML confidence → Fake: {ml_result[1]:.2f}, Real: {ml_result[2]:.2f}")

        st.subheader("Entity Verification")
        for e, exists, sim in wiki_flags:
            status = "VERIFIED ✅" if exists else "NOT VERIFIED ⚠️"
            st.write(f"- {e}: {status} (Similarity={sim:.2f})")

