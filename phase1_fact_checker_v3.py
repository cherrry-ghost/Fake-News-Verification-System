import wikipediaapi
import re

# ---------------- Wikipedia Setup ----------------
wiki = wikipediaapi.Wikipedia(
    language='en',
    extract_format=wikipediaapi.ExtractFormat.WIKI,
    user_agent="FakeNewsDetector/1.0 (student project)"
)


# ---------------- Helper Functions ----------------
def extract_year(statement):
    """Find a 4-digit year in the statement"""
    match = re.search(r'\b(19|20)\d{2}\b', statement)
    return int(match.group()) if match else None


def check_fact_with_year(role, country, person, year=None):
    """Check fact using Wikipedia"""
    page_title = f"{role} of {country}"
    page = wiki.page(page_title)

    if not page.exists():
        return "UNKNOWN", f"No page found for {page_title}"

    summary = page.summary.lower()

    if person.lower() not in summary:
        return "FALSE", f"{person} is not listed for {role} of {country}"

    if not year:
        return "TRUE", f"{person} is currently {role} of {country}"

    pattern = rf"{person.lower()}.*{year}"
    if re.search(pattern, summary):
        return "TRUE", f"{person} was {role} of {country} in {year}"
    else:
        return "FALSE", f"{person} was not {role} of {country} in {year}"


# ---------------- Synonyms and Country Mapping ----------------
role_keywords = {
    "President": ["president", "leader", "head of state"],
    "Prime Minister": ["prime minister", "pm", "premier"],
    "Capital": ["capital", "city"]
}

countries = {
    "usa": "United States",
    "us": "United States",
    "united states": "United States",
    "uk": "United Kingdom",
    "india": "India",
    "russia": "Russia",
    "france": "France"
}

# ---------------- MAIN ----------------
print("LIVE FACT CHECKER v4 SMART")
print("Type 'exit' to quit\n")

while True:
    statement = input("Enter statement: ")

    if statement.lower() == "exit":
        break

    # Extract year first
    year = extract_year(statement)

    # Remove year from words
    words = statement.lower().split()
    words_no_year = [w for w in words if str(year) != w]

    # Detect role using synonyms
    role = None
    for r, keywords in role_keywords.items():
        for kw in keywords:
            if kw in statement.lower():
                role = r
                break
        if role:
            break

    if not role:
        print("Fact type not supported yet\n")
        continue

    # Detect country
    country = None
    if "of" in words_no_year:
        of_index = words_no_year.index("of")
        raw_country = words_no_year[of_index + 1]
        country = countries.get(raw_country, raw_country.capitalize())
    else:
        # fallback: last word
        raw_country = words_no_year[-1]
        country = countries.get(raw_country, raw_country.capitalize())

    # Detect person
    person = words_no_year[0].capitalize()

    # Call the checker
    result, reason = check_fact_with_year(role, country, person, year)

    # Show results
    print("\nResult:", result)
    print("Reason:", reason)
    print("-" * 40)
