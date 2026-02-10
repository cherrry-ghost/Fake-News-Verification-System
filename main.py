# main.py

import pickle
import re
import nltk
from nltk.corpus import stopwords
from nlp.entity_extractor import extract_entities
from nlp.fact_checker import wikipedia_verify

# ---------------------------
# NLTK setup
# ---------------------------
nltk.download("stopwords")
STOP_WORDS = set(stopwords.words("english"))

# ---------------------------
# Load ML model & vectorizer
# ---------------------------
with open("models/model.pkl", "rb") as f:
    model = pickle.load(f)

with open("models/vectorizer.pkl", "rb") as f:
    vectorizer = pickle.load(f)

# ---------------------------
# Text cleaning
# ---------------------------
def clean_text(text):
    text = text.lower()
    text = re.sub(r"http\S+|www\S+", "", text)
    text = re.sub(r"[^a-z\s]", "", text)
    words = text.split()
    words = [w for w in words if w not in STOP_WORDS]
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
    prob_fake, prob_real = model.predict_proba(vectorized)[0]

    if prob_real >= 0.65:
        label = "LIKELY REAL"
    elif prob_fake >= 0.65:
        label = "LIKELY FAKE"
    else:
        label = "UNCERTAIN"

    return label, float(prob_fake), float(prob_real)

# ---------------------------
# Explanation generator
# ---------------------------
def generate_explanation(text, rule_result, ml_label, fake_conf, real_conf):
    reasons = []
    text_lower = text.lower()
    sensational_words = [
        "breaking", "shocking", "secret", "revealed",
        "share this", "before it gets deleted"
    ]
    official_words = [
        "official statement", "ministry", "government",
        "press release", "court", "according to"
    ]
    if any(word in text_lower for word in sensational_words):
        reasons.append("Sensational or emotionally charged language detected")
    if any(word in text_lower for word in official_words):
        reasons.append("Mentions official or authoritative sources")
    if fake_conf >= 0.75:
        reasons.append(f"ML model shows high fake confidence ({fake_conf:.2f})")
    if real_conf >= 0.75:
        reasons.append(f"ML model shows high real confidence ({real_conf:.2f})")
    if rule_result == "UNCERTAIN" and ml_label == "UNCERTAIN":
        reasons.append("Insufficient strong signals for a confident decision")
    return reasons

# ---------------------------
# Final decision with Wikipedia verification override
# ---------------------------
# ---------------------------
# Final decision with Wikipedia verification override (FIXED)
# ---------------------------
def final_decision(rule_result, ml_result, entities, text):
    ml_label, fake_conf, real_conf = ml_result
    wiki_flags = []

    for entity_type, entities_list in entities.items():
        for e in entities_list:
            exists, similarity, summary = wikipedia_verify(e, text)
            wiki_flags.append((e, exists, similarity))

    verified_entities = [e for e, exists, sim in wiki_flags if exists]

    # 🚫 BLOCK ML FROM OVERRIDING FACTS
    if verified_entities and rule_result != "LIKELY FAKE":
        decision = "LIKELY REAL ✅ (Verified factual entities)"

    # 🚨 Strong fake only when ALL agree
    elif (
        rule_result == "LIKELY FAKE"
        and ml_label == "LIKELY FAKE"
        and fake_conf >= 0.85
    ):
        decision = "LIKELY FAKE ⚠️ (Strong fake signals)"

    # ML confident real
    elif ml_label == "LIKELY REAL" and real_conf >= 0.80:
        decision = "LIKELY REAL ✅ (ML confident)"

    # ML confident fake (only if no verified entities)
    elif ml_label == "LIKELY FAKE" and fake_conf >= 0.80:
        decision = "LIKELY FAKE ⚠️ (ML confident)"

    # Rule-based fallback
    elif rule_result != "UNCERTAIN":
        decision = rule_result + " (Rule-based)"

    else:
        decision = "UNCERTAIN ⚠️"

    return decision, wiki_flags

# ---------------------------
# Main execution
# ---------------------------
def main():
    print("\n=== ADVANCED FAKE NEWS DETECTION SYSTEM ===\n")
    text = input("Enter full news text:\n\n").strip()
    word_count = len([w for w in text.split() if w.strip() != ""])
    if word_count < 10:
        print("\n⚠️ Input too short for reliable analysis. Please enter full news content.")
        return

    # Step 1: Entity extraction
    entities = extract_entities(text)
    print("\nENTITIES DETECTED:")
    for k, v in entities.items():
        if v:
            print(f"{k}: {', '.join(v)}")

    # Step 2: Rule-based + ML predictions
    rule_result = rule_based_check(text)
    ml_label, fake_conf, real_conf = ml_prediction(text)

    # Step 3: Final decision with Wikipedia verification
    final, wiki_flags = final_decision(rule_result, (ml_label, fake_conf, real_conf), entities, text)

    # Step 4: Print intermediate results
    print("\n--- RESULTS ---")
    print(f"Rule-based Check : {rule_result}")
    print(f"ML Prediction   : {ml_label}")
    print(f"ML Confidence   : Fake={fake_conf:.2f}, Real={real_conf:.2f}")

    print("\n--- ENTITY VERIFICATION ---")
    for e, exists, sim in wiki_flags:
        status = "VERIFIED ✅" if exists else "NOT VERIFIED ⚠️"
        print(f"{e}: {status} (Similarity={sim:.2f})")

    # Step 5: Explanation
    explanations = generate_explanation(text, rule_result, ml_label, fake_conf, real_conf)

    print(f"\nFINAL DECISION : {final}")

    if explanations:
        print("\nREASONS:")
        for r in explanations:
            print(f"• {r}")


# ---------------------------
if __name__ == "__main__":
    main()
