import spacy

# Load spaCy English model


# Use lightweight blank English model (no external download required)
nlp = spacy.blank("en")

def extract_entities(text):
    doc = nlp(text)
    entities = [ent.text for ent in doc.ents]
    return entities

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
