import wikipediaapi
import re
from difflib import get_close_matches

print("FACT CHECKER STARTED SUCCESSFULLY")

# ---------------- Wikipedia Setup ----------------
wiki = wikipediaapi.Wikipedia(
    language="en",
    extract_format=wikipediaapi.ExtractFormat.WIKI,
    user_agent="FakeNewsProject/1.0 (learning project)"
)

# ---------------- Helper Functions ----------------
def extract_year(text):
    match = re.search(r"\b(19|20)\d{2}\b", text)
    return int(match.group()) if match else None


def check_fact(role, country, person, year=None):
    page_title = f"{role} of {country}"
    page = wiki.page(page_title)

    if not page.exists():
        return "UNKNOWN", f"No Wikipedia page for {page_title}"

    summary = page.summary.lower()

    if person.lower() not in summary:
        return "FALSE", f"{person} not found in {page_title}"

    if year is None:
        return "TRUE", f"{person} is listed as {role} of {country}"

    if str(year) in summary:
        return "TRUE", f"{person} was {role} of {country} in {year}"
    else:
        return "FALSE", f"{person} was not {role} of {country} in {year}"


# ---------------- Role Keywords ----------------
role_keywords = {
    "President": ["president", "leader", "head"],
    "Prime Minister": ["prime minister", "pm", "premier"],
    "Capital": ["capital"]
}

# ---------------- Country Mapping ----------------
countries = {
    "india": "India",
    "usa": "United States",
    "us": "United States",
    "united states": "United States",
    "uk": "United Kingdom",
    "russia": "Russia",
    "france": "France"
}

# ---------------- MAIN LOOP ----------------
print("\nType 'exit' to quit\n")

while True:
    statement = input("Enter statement: ").lower()

    if statement == "exit":
        break

    year = extract_year(statement)
    words = statement.split()

    # Detect role
    role = None
    for r, keys in role_keywords.items():
        for k in keys:
            if k in statement:
                role = r
                break
        if role:
            break

    if not role:
        print("\nResult: UNKNOWN")
        print("Reason: Role not supported yet")
        print("-" * 40)
        continue

    # Detect country
    country = None
    for w in words:
        if w in countries:
            country = countries[w]
            break

    if not country:
        print("\nResult: UNKNOWN")
        print("Reason: Country not detected")
        print("-" * 40)
        continue

    # Detect person (simple)
    person = None
    for w in words:
        if w not in role_keywords.get(role, []) and w not in countries:
            if w not in ["is", "of", "the", "in"]:
                person = w.capitalize()
                break

    if not person:
        print("\nResult: UNKNOWN")
        print("Reason: Person not detected")
        print("-" * 40)
        continue

    result, reason = check_fact(role, country, person, year)

    print("\nResult:", result)
    print("Reason:", reason)
    print("-" * 40)
