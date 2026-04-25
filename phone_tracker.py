"""
Phone Number Tracker (MVP)

Looks up metadata for a phone number: country, region, carrier,

"""

import argparse
import sys

try:
    import phonenumbers
    from phonenumbers import carrier, geocoder, timezone, number_type, PhoneNumberType
except ImportError:
    sys.stderr.write(
        "Missing dependency. Install with:\n    pip install phonenumbers\n"
    )
    sys.exit(1)


TYPE_LABELS = {
    PhoneNumberType.FIXED_LINE: "Fixed line",
    PhoneNumberType.MOBILE: "Mobile",
    PhoneNumberType.FIXED_LINE_OR_MOBILE: "Fixed line or mobile",
    PhoneNumberType.TOLL_FREE: "Toll free",
    PhoneNumberType.PREMIUM_RATE: "Premium rate",
    PhoneNumberType.SHARED_COST: "Shared cost",
    PhoneNumberType.VOIP: "VoIP",
    PhoneNumberType.PERSONAL_NUMBER: "Personal number",
    PhoneNumberType.PAGER: "Pager",
    PhoneNumberType.UAN: "UAN",
    PhoneNumberType.VOICEMAIL: "Voicemail",
    PhoneNumberType.UNKNOWN: "Unknown",
}


def lookup(raw_number: str, region: str | None = None) -> dict:
    parsed = phonenumbers.parse(raw_number, region)

    is_valid = phonenumbers.is_valid_number(parsed)
    is_possible = phonenumbers.is_possible_number(parsed)

    return {
        "input": raw_number,
        "e164": phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.E164),
        "international": phonenumbers.format_number(
            parsed, phonenumbers.PhoneNumberFormat.INTERNATIONAL
        ),
        "national": phonenumbers.format_number(
            parsed, phonenumbers.PhoneNumberFormat.NATIONAL
        ),
        "country_code": parsed.country_code,
        "country_region": phonenumbers.region_code_for_number(parsed) or "Unknown",
        "location": geocoder.description_for_number(parsed, "en") or "Unknown",
        "carrier": carrier.name_for_number(parsed, "en") or "Unknown",
        "line_type": TYPE_LABELS.get(number_type(parsed), "Unknown"),
        "timezones": list(timezone.time_zones_for_number(parsed)),
        "is_valid": is_valid,
        "is_possible": is_possible,
    }


def render(info: dict) -> str:
    valid_mark = "✅(EXITS)" if info["is_valid"] else "❌(DON'T EXIST)"
    lines = [
        "",
        "📞 Phone Number Tracker",
        "─" * 40,
        f"Input          : {info['input']}",
        f"Valid number   : {valid_mark}  (possible: {info['is_possible']})",
        "",
        f"E.164          : {info['e164']}",
        f"International  : {info['international']}",
        f"National       : {info['national']}",
        "",
        f"Country code   : +{info['country_code']}",
        f"Region         : {info['country_region']}",
        f"Location       : {info['location']}",
        f"Carrier        : {info['carrier']}",
        f"Line type      : {info['line_type']}",
        f"Timezone(s)    : {', '.join(info['timezones']) or 'Unknown'}",
        "─" * 40,
    ]
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="Phone number metadata lookup (MVP).")
    parser.add_argument("number", nargs="?", help="Phone number, ideally in SA.+ format (e.g. +270005555)")
    parser.add_argument("--region", "-r", help="Default region code (e.g. SA, GB, FR) for numbers without '+'.")
    args = parser.parse_args()

    raw = args.number or input("Enter a phone number (with country code, e.g. +270005555): ").strip()
    if not raw:
        print("No number provided.", file=sys.stderr)
        return 1

    try:
        info = lookup(raw, args.region)
    except phonenumbers.NumberParseException as e:
        print(f"Could not parse number: {e}", file=sys.stderr)
        print("Tip: include the country code (e.g. +27...) or pass --region SA.", file=sys.stderr)
        return 2

    print(render(info))
    return 0


if __name__ == "__main__":
    sys.exit(main())
