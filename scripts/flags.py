"""Country -> flag emoji for the `country_or_body` field.

Unknown names fall back to the EU flag, which is also the correct symbol for
`EU/...` bodies such as ENISA and CERT-EU.
"""

FLAGS = {
    "EU": "🇪🇺", "Europe": "🇪🇺",
    "Austria": "🇦🇹", "Belgium": "🇧🇪", "Bulgaria": "🇧🇬", "Croatia": "🇭🇷",
    "Cyprus": "🇨🇾", "Czechia": "🇨🇿", "Czech Republic": "🇨🇿", "Denmark": "🇩🇰",
    "Estonia": "🇪🇪", "Finland": "🇫🇮", "France": "🇫🇷", "Germany": "🇩🇪",
    "Greece": "🇬🇷", "Hungary": "🇭🇺", "Iceland": "🇮🇸", "Ireland": "🇮🇪",
    "Italy": "🇮🇹", "Latvia": "🇱🇻", "Liechtenstein": "🇱🇮", "Lithuania": "🇱🇹",
    "Luxembourg": "🇱🇺", "Malta": "🇲🇹", "Netherlands": "🇳🇱", "Norway": "🇳🇴",
    "Poland": "🇵🇱", "Portugal": "🇵🇹", "Romania": "🇷🇴", "Slovakia": "🇸🇰",
    "Slovenia": "🇸🇮", "Spain": "🇪🇸", "Sweden": "🇸🇪", "Switzerland": "🇨🇭",
    "United Kingdom": "🇬🇧", "UK": "🇬🇧",
}


def flag(country_or_body: str) -> str:
    country = (country_or_body or "EU").split("/", 1)[0].strip()
    return FLAGS.get(country, "🇪🇺")
