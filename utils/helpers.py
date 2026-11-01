
def clean_text(text):
    """Remove unnecessary spaces from text."""
    if not isinstance(text, str):
        return ""

    return text.strip()


def format_result(result):
    """Convert a result into a user-friendly string."""
    if result is None:
        return "No result available."

    return str(result)
