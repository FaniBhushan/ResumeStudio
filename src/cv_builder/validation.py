from __future__ import annotations

import re
from urllib.parse import urlsplit


SUPPORTED_NETWORKS = {
    name.casefold() for name in (
        "LinkedIn", "GitHub", "GitLab", "IMDB", "Instagram", "ORCID", "Mastodon",
        "StackOverflow", "ResearchGate", "YouTube", "Google Scholar", "Telegram",
        "WhatsApp", "Leetcode", "X", "Bluesky", "Reddit",
    )
}


def phone_format_error(phone: str) -> str | None:
    value = phone.strip()
    if not value:
        return None
    if not re.fullmatch(r"\+[0-9().\-\s]+", value):
        return "Use +, digits, spaces, parentheses, dots, or hyphens only. Include the country code (for example, +49 30 12345678)."
    digits = re.sub(r"\D", "", value)
    if not 8 <= len(digits) <= 15 or digits.startswith("0"):
        return "Enter a valid international phone number with its country code (for example, +49 30 12345678), or leave it blank."
    return None


def email_format_error(email: str) -> str | None:
    value = email.strip()
    if not value:
        return None
    if len(value) > 254 or not re.fullmatch(r"[^\s@]+@[^\s@]+\.[^\s@]+", value):
        return "Enter an email address in the format name@example.com, or leave it blank."
    return None


def date_format_error(value: str, *, end_date: bool = False) -> str | None:
    date = value.strip()
    if not date or (end_date and date.casefold() in {"present", "current"}):
        return None
    match = re.fullmatch(r"(\d{4})-(\d{2})", date)
    if not match or not 1 <= int(match.group(2)) <= 12:
        return "Use YYYY-MM (for example, 2024-03)."
    return None


def links_format_error(text: str) -> str | None:
    for line_number, line in enumerate(text.splitlines(), start=1):
        value = line.strip()
        if not value:
            continue
        if ":" in value:
            network, destination = (part.strip() for part in value.split(":", 1))
            if network.casefold() in {"website", "url", "portfolio"}:
                if not destination:
                    return f"Link on line {line_number}: add a website address after '{network}:'."
                url = destination if "://" in destination else f"https://{destination}"
                parsed = urlsplit(url)
                if parsed.scheme not in {"http", "https"} or not parsed.hostname or any(char.isspace() for char in destination):
                    return f"Link on line {line_number}: enter a valid website address, such as https://example.com."
            elif network.casefold() not in SUPPORTED_NETWORKS:
                return f"Link on line {line_number}: '{network}' is not a supported network. Use Website: https://example.com for other links."
            elif not destination:
                return f"Link on line {line_number}: add a username or profile URL after '{network}:'."
        else:
            url = value if "://" in value else f"https://{value}"
            parsed = urlsplit(url)
            if parsed.scheme not in {"http", "https"} or not parsed.hostname or any(char.isspace() for char in value):
                return f"Link on line {line_number}: enter a valid website address, such as https://example.com."
    return None
