import wikipediaapi

wiki = wikipediaapi.Wikipedia(
    language='en',
    extract_format=wikipediaapi.ExtractFormat.WIKI,
    user_agent="FakeNewsDetector/1.0 (student project)"
)

def check_fact(role, country, person):
    page_title = f"{role} of {country}"
    page = wiki.page(page_title)

    if not page.exists():
        return "UNKNOWN", f"No page found for {page_title}"

    summary = page.summary.lower()

    if person.lower() in summary:
        return "TRUE", f"{person} matches information on Wikipedia"
    else:
        return "FALSE", f"Wikipedia shows different information for {country}"

print("LIVE FACT CHECKER v2")
print("Type 'exit' to quit\n")

while True:
    statement = input("Enter statement: ")

    if statement.lower() == "exit":
        break

    words = statement.lower().split()

    if "president" in words:
        role = "President"
    elif "prime" in words or "pm" in words:
        role = "Prime Minister"
    elif "capital" in words:
        role = "Capital"
    else:
        print("Fact type not supported yet\n")
        continue

    person = words[0].capitalize()
    country = words[-1].capitalize()

    result, reason = check_fact(role, country, person)

    print("\nResult:", result)
    print("Reason:", reason)
    print("-" * 40)
