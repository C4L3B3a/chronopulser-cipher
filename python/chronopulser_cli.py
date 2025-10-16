import json
import argparse
import re  # For detecting <utf=number> patterns

# -------------------------------
# Load cipher JSON from a file
# -------------------------------
def load_cipher(path="../chronopulse.json"):
    """
    Loads the ChronoPulse cipher JSON file.
    Returns a dictionary containing Alphabet, Symbols, and Control characters.
    """
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

# -------------------------------
# UTF mapping: <utf=number> -> letter
# -------------------------------
# This allows users to type <utf=1> for 'a', <utf=2> for 'b', etc.
utf_map = {str(i+1): chr(97+i) for i in range(26)}  # '1':'a', ..., '26':'z'
reverse_utf_map = {v: str(i+1) for i, v in enumerate("abcdefghijklmnopqrstuvwxyz")}

# -------------------------------
# Encode function
# -------------------------------
def encode_chronopulse(text, cipher):
    """
    Encodes a text string into ChronoPulse symbols using the provided cipher.
    Features:
      - Lowercase letters get a leading '_'
      - Spaces become '○', commas/periods become '•'
      - <utf=number> syntax translates numbers 1-26 to letters
    """
    alphabet = cipher["Alphabet"]
    symbols = {v["Represents"]: k for k, v in cipher["Symbols"].items()}

    # Regex pattern to detect <utf=number> in input
    utf_pattern = re.compile(r"<utf=(\d+)>")
    result = []
    i = 0
    while i < len(text):
        # Check if current position matches <utf=number>
        m = utf_pattern.match(text, i)
        if m:
            num = m.group(1)
            char = utf_map.get(num, "?")  # Default to '?' if number invalid
            base = alphabet[char.upper()]
            if char.islower():
                base = "_" + base  # Add '_' prefix for lowercase
            result.append(base + "●")  # Add end-of-letter symbol
            i += len(m.group(0))  # Skip past <utf=number>
            continue

        char = text[i]
        if char.isalpha():  # Handle letters
            base = alphabet[char.upper()]
            if char.islower():
                base = "_" + base
            result.append(base + "●")
        elif char == " ":  # Space between words
            result.append("○")
        elif char in [",", ".", ";", ":"]:  # Common punctuation
            result.append("•")
        elif char in symbols:  # Other symbols from JSON
            result.append(symbols[char])
        else:  # Unknown character
            result.append("?")
        i += 1
    return "".join(result)

# -------------------------------
# Decode function
# -------------------------------
def decode_chronopulse(code, cipher):
    """
    Decodes a ChronoPulse code string back into text.
    Supports:
      - '_' prefix for lowercase letters
      - '●' as end-of-letter
      - '○' as word separator
      - '•' as comma/pause
      - JSON symbols mapping
    """
    alphabet = cipher["Alphabet"]
    reverse = {v: k for k, v in alphabet.items()}  # Reverse mapping: symbols -> letter
    symbols = cipher["Symbols"]

    result, current = [], ""
    for s in code:
        if s in ("□", "■", "_"):  # Building a letter (include '_' for lowercase)
            current += s
        elif s == "●":  # End of letter
            is_lower = current.startswith("_")
            key = current[1:] if is_lower else current
            letter = reverse.get(key, "?")
            if is_lower:
                letter = letter.lower()  # Restore lowercase
            result.append(letter)
            current = ""
        elif s == "○":  # Word separator
            result.append(" ")
        elif s == "•":  # Comma/pause
            result.append(", ")
            current = ""
        elif s in symbols:  # Other symbols
            result.append(symbols[s]["Represents"])
        else:  # Unknown symbol
            result.append("?")

    # Handle any leftover letter at the end
    if current:
        is_lower = current.startswith("_")
        key = current[1:] if is_lower else current
        letter = reverse.get(key, "?")
        if is_lower:
            letter = letter.lower()
        result.append(letter)

    return "".join(result).strip()

# -------------------------------
# CLI main function
# -------------------------------
def main():
    """
    Command-line interface for ChronoPulse.
    Users can run:
      python chronopulse_cli.py encode "Hello world"
      python chronopulse_cli.py decode "□□■●□■■●○"
    If arguments are missing, it prompts interactively.
    """
    parser = argparse.ArgumentParser(description="ChronoPulse CLI")
    parser.add_argument("mode", choices=["encode", "decode"], nargs="?", help="Operation mode")
    parser.add_argument("input", nargs="?", help="Text to encode or code to decode")
    parser.add_argument("--json", default="../chronopulse.json", help="Path to JSON cipher")
    args = parser.parse_args()

    cipher = load_cipher(args.json)

    # Interactive fallback if arguments not provided
    if not args.mode:
        args.mode = input("Mode (encode/decode): ").strip()
    if not args.input:
        args.input = input("Enter text/code: ").strip()

    if args.mode == "encode":
        print(encode_chronopulse(args.input, cipher))
    elif args.mode == "decode":
        print(decode_chronopulse(args.input, cipher))
    else:
        print("Invalid mode. Use 'encode' or 'decode'.")

# -------------------------------
# Run CLI
# -------------------------------
if __name__ == "__main__":
    main()
    
# By C4L