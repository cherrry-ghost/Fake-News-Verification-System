import wikipedia
from difflib import SequenceMatcher

def text_similarity(a, b):
    return SequenceMatcher(None, a.lower(), b.lower()).ratio()

def wikipedia_verify(entity, original_text):
    try:
        summary = wikipedia.summary(entity, sentences=2, auto_suggest=False)
        similarity = text_similarity(summary, original_text)
        return True, similarity, summary
    except wikipedia.exceptions.DisambiguationError as e:
        return True, 0.30, "Multiple meanings found"
    except wikipedia.exceptions.PageError:
        return False, 0.0, ""
    except Exception:
        return False, 0.0, ""
