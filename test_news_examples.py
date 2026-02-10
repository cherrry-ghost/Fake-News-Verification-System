# test_news_examples.py

from main import clean_text, rule_based_check, ml_prediction, final_decision, generate_explanation
from nlp.entity_extractor import extract_entities

# ---------------------------
# 10 test news items
# ---------------------------
test_news = [
    # Likely real
    "The Supreme Court of India announced a new ruling on environmental regulations in 2020.",
    "According to the Ministry of Health, vaccination programs will continue nationwide in 2024.",
    "NASA confirmed that the James Webb Space Telescope captured images of distant galaxies.",

    # Likely fake
    "Breaking: Government secretly approves flying cars for all citizens before it gets deleted!",
    "According to leaked documents, aliens will start paying taxes in the United States next year.",
    "Shocking: This secret ingredient in your food will instantly cure all diseases!",

    # Ambiguous / uncertain
    "A new report says that education policies are changing in some schools.",
    "The town council discussed new traffic rules today.",
    "Experts suggest that an unusual weather phenomenon might occur in the northern regions next month.",
    "According to the Ministry of Finance, a new digital currency may be introduced in 2025."
]

# ---------------------------
# Run tests
# ---------------------------
for idx, text in enumerate(test_news, start=1):
    print("\n" + "=" * 60)
    print(f"TEST {idx}:\n{text}\n")

    word_count = len([w for w in text.split() if w.strip() != ""])
    if word_count < 10:
        print("⚠️ Input too short for reliable analysis. Skipping.")
        continue

    # Entities
    entities = extract_entities(text)
    print("ENTITIES DETECTED:")
    for k, v in entities.items():
        if v:
            print(f"{k}: {', '.join(v)}")

    # ML + Rule
    rule_result = rule_based_check(text)
    ml_label, fake_conf, real_conf = ml_prediction(text)

    # Final decision
    final, wiki_flags = final_decision(rule_result, (ml_label, fake_conf, real_conf), entities, text)

    print("\n--- RESULTS ---")
    print(f"Rule-based Check : {rule_result}")
    print(f"ML Prediction   : {ml_label}")
    print(f"ML Confidence   : Fake={fake_conf:.2f}, Real={real_conf:.2f}")

    print("\n--- ENTITY VERIFICATION ---")
    for e, sim, exists in wiki_flags:
        status = "MATCHED ✅" if sim >= 0.5 else "NOT MATCHED ⚠️"
        print(f"{e}: {status} (Similarity={sim:.2f})")

    explanations = generate_explanation(text, rule_result, ml_label, fake_conf, real_conf)
    print(f"\nFINAL DECISION : {final}")
    if explanations:
        print("\nREASONS:")
        for r in explanations:
            print(f"• {r}")

print("\n" + "=" * 60)
print("All tests completed.")
