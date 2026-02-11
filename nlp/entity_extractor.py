import spacy
import subprocess
import sys
# Load spaCy English model
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    subprocess.run([sys.executable, "-m", "spacy", "download", "en_core_web_sm"])
    nlp = spacy.load("en_core_web_sm")
# ---------------------------
# Entity Extraction Function
# ---------------------------
def extract_entities(text):
    doc = nlp(text)

    entities = {
        "PERSON": [],
        "ORG": [],
        "GPE": [],
        "DATE": []
    }

    for ent in doc.ents:
        if ent.label_ in entities:
            entities[ent.label_].append(ent.text)

    # Remove duplicates
    for key in entities:
        entities[key] = list(set(entities[key]))

    return entities


# ---------------------------
# Test (optional)
# ---------------------------
if __name__ == "__main__":
    sample_text = "The Supreme Court of India announced a new ruling in 2024."
    print(extract_entities(sample_text))
