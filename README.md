# 📞 Phone Number Tracker (Python MVP)

A lightweight **command-line tool** that looks up public metadata for any phone number using Google's [libphonenumber](https://github.com/google/libphonenumber) (via the `phonenumbers` Python port).

> ⚠️ This is **not** a GPS tracker. It does not locate a person or device. It only returns publicly available information derived from the number itself (country code, carrier prefix, line type, timezone, etc.).

---

##  Features

- ✅ Validates and parses phone numbers (E.164, international, national formats)
- 🌍 Detects **country / region**
- 📡 Detects **carrier** (e.g. Verizon, Vodafone)
- 📱 Detects **line type** (Mobile, Fixed Line, VoIP, Toll-Free, etc.)
- 🕒 Returns associated **timezones**
- 🖥️ Works via CLI args **or** interactive prompt

---

## 📦 Installation

Requires **Python 3.8+**.

```bash
git clone https://github.com/<your-username>/<your-repo>.git
cd <your-repo>
pip install phonenumbers
```

---

## 🚀 Usage

### One-off lookup
```bash
python phone_tracker.py +270005555
```

### With a default region (for local-format numbers)
```bash
python phone_tracker.py "+27 000 5555" --region SA
```

### Interactive mode
```bash
python phone_tracker.py
> Enter a phone number: +2700005555
```

---

## 📋 Example Output

```
─────────────────────────────────────────
 Phone Number Lookup
─────────────────────────────────────────
 Input         : +2700005555
 Valid         : ✅ Yes
 E.164         : +2700005555
 International : +27 000 5555
 National      : (27) 00005555
 Country code  : 1
 Region        : SA
 Location      : tembisa, JHB
 Carrier       : (unknown for landlines)
 Line type     : Fixed line or mobile
 Timezones     : SOUTH AFRICA
─────────────────────────────────────────
```

---

## 🧠 How It Works

The script wraps the `phonenumbers` library:

1. **Parse** the raw input into a structured `PhoneNumber` object.
2. **Validate** that it's a possible & valid number.
3. Query the bundled offline databases for:
   - `geocoder` → human-readable location
   - `carrier` → mobile network operator
   - `timezone` → IANA timezone IDs
   - `number_type` → mobile / fixed / VoIP / etc.
4. Pretty-print the results to the terminal.

All lookups are **offline** — no API keys, no network calls, no tracking.

---

## ⚖️ Disclaimer

This tool only surfaces metadata that is **inherent to the number's structure** (country code, allocated carrier block, etc.). It cannot and will not:

- Track real-time location
- Reveal the owner's identity
- Access call logs or messages

Use responsibly and respect local privacy laws.

---

## 📄 License

MIT — USE IT FOR LEARNING PURPOSES SINCE I WAS LEARNING TOO.
