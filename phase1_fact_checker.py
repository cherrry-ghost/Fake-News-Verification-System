import wikipediaapi

# Create Wikipedia object
wiki = wikipediaapi.Wikipedia(
    language='en',
    extract_format=wikipediaapi.ExtractFormat.WIKI,
    user_agent="FakeNewsDetector/1.0 (student project)"
)


def check_president_claim(country, person):
    page_title = f"President of {country}"
    page = wiki.page(page_title)

    if not page.exists():
        return "INSUFFICIENT INFORMATION", f"No Wikipedia page found for {page_title}"

    summary = page.summary.lower()

    if person.lower() in summary:
        return "TRUE", f"{person} is mentioned as President of {country}"
    else:
        return "FALSE", f"Wikipedia lists a different president for {country}"

# ---------------- MAIN PROGRAM ----------------

print("LIVE FACT CHECKER (Phase 1)")
print("Type 'exit' to quit\n")

while True:
    statement = input("Enter statement: ")

    if statement.lower() == "exit":
        break

    # Very simple parsing (for now)
    words = statement.split()

    if "president" in words and "of" in words:
        person = words[0]
        country = words[-1]

        result, reason = check_president_claim(country, person)

        print("\nResult:", result)
        print("Reason:", reason)
        print("-" * 40)
    else:
        print("Unsupported statement format.\n")
