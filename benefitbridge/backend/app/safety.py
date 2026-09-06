import re

DISCLAIMER = "Verify current eligibility and application instructions on the official government portal."

def screen_response(text: str) -> str:
    if not text:
        return text
    cleaned = re.sub(r"(?i)(guaranteed|definitely eligible|officially approved)", "may be eligible", text)
    if DISCLAIMER.lower() not in cleaned.lower():
        cleaned = f"{cleaned}\n\n{DISCLAIMER}"
    return cleaned