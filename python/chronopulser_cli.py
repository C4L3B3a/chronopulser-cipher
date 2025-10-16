#!/usr/bin/env python3
# ==========================================================
# ChronoPulse v2 - Encoder/Decoder
# ----------------------------------------------------------
# Author: Open Source Community
# License: MIT
#
# Description:
#   Encodes and decodes messages using the ChronoPulse v2 Cipher.
#   The cipher uses geometric and symbolic characters such as □■●○☆♤♡◇♧《》¤₩÷.
#
#   Configuration is read from a JSON file (chronopulse.json).
#   This makes it easy to extend or customize the cipher.
# ==========================================================

import json
import os

# -----------------------------
# Utility: Load Cipher JSON
# -----------------------------
def load_cipher(path: str):
    """Load and decode a ChronoPulse cipher file (JSON)."""
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


# -----------------------------
# Encoding Function
# -----------------------------
def encode_chronopulse(text: str, cipher: dict) -> str:
    """Convert plain text into ChronoPulse encoded symbols."""
    alphabet = cipher["Alphabet"]
    symbols = {v["Represents"]: k for k, v in cipher["Symbols"].items()}

    result = []

    for char in text:
        upper = char.upper()

        if upper in alphabet:
            # Encode letters/numbers
            result.append(alphabet[upper] + "●")  # "●" = End of letter
        elif char == " ":
            result.append("○")  # "○" = Space
        elif char in symbols:
            result.append(symbols[char])  # Symbol/punctuation replacement
        else:
            result.append("?")  # Unknown character placeholder

    return "".join(result)


# -----------------------------
# Decoding Function
# -----------------------------
def decode_chronopulse(code: str, cipher: dict) -> str:
    """Convert ChronoPulse symbols back into readable text."""
    alphabet = cipher["Alphabet"]
    reverse_alpha = {v: k for k, v in alphabet.items()}
    symbols = cipher["Symbols"]

    result = []
    current = ""

    for ch in code:
        if ch in ("□", "■"):
            current += ch
        elif ch == "●":
            # End of a letter
            result.append(reverse_alpha.get(current, "?"))
            current = ""
        elif ch == "○":
            # Space
            result.append(" ")
        elif ch in symbols:
            # Symbol or punctuation
            result.append(symbols[ch]["Represents"])
        else:
            result.append("?")

    # In case last letter was missing "●"
    if current:
        result.append(reverse_alpha.get(current, "?"))

    return "".join(result)


# -----------------------------
# Main CLI
# -----------------------------
def main():
    cipher_path = os.path.join(os.path.dirname(__file__), "chronopulse.json")
    cipher = load_cipher(cipher_path)

    print("=== ChronoPulse v2 Encoder/Decoder ===")
    mode = input("Mode (encode/decode): ").strip().lower()
    text = input("Enter text/code: ").strip()

    if mode == "encode":
        output = encode_chronopulse(text, cipher)
    elif mode == "decode":
        output = decode_chronopulse(text, cipher)
    else:
        print("Invalid mode. Please type 'encode' or 'decode'.")
        return

    print("\nResult:")
    print(output)


if __name__ == "__main__":
    main()
    
# By C4L