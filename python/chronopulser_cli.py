#!/usr/bin/env python3
# ==========================================================
# ChronoPulse Cipher - Encoder/Decoder
# ----------------------------------------------------------
# Author: Open Source Community
# License: MIT
#
# Description:
#   Encodes and decodes messages using the ChronoPulse Cipher.
#   Supports lowercase letters, symbols, and <utf=N> numeric encoding.
# ==========================================================

import json
import os
import re

# -----------------------------
# Utility: Load Cipher JSON
# -----------------------------
def load_cipher(path: str):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

# -----------------------------
# UTF Mapping (optional)
# -----------------------------
utf_map = {str(i+1): chr(97+i) for i in range(26)}  # 1->a, 2->b, etc.
reverse_utf_map = {v: str(i+1) for i, v in enumerate("abcdefghijklmnopqrstuvwxyz")}

# -----------------------------
# Encoding Function
# -----------------------------
def encode_chronopulse(text: str, cipher: dict):
    alphabet = cipher["Alphabet"]
    symbols = {v["Represents"]: k for k, v in cipher["Symbols"].items()}
    result = []
    invalid_chars = []

    utf_pattern = re.compile(r"<utf=(\d+)>")
    i = 0
    while i < len(text):
        m = utf_pattern.match(text, i)
        if m:
            num = m.group(1)
            char = utf_map.get(num, "?")
            symbol = alphabet.get(char.upper(), "?")
            if char.islower():
                symbol = "_" + symbol
            result.append(symbol + "●")
            i += len(m.group(0))
            continue

        char = text[i]
        upper = char.upper()
        if upper in alphabet:
            symbol = alphabet[upper]
            if char.islower():
                symbol = "_" + symbol
            result.append(symbol + "●")
        elif char == " ":
            result.append("○")
        elif char in symbols:
            result.append(symbols[char])
        else:
            result.append("?")
            invalid_chars.append(char)
        i += 1

    return "".join(result), invalid_chars

# -----------------------------
# Decoding Function
# -----------------------------
def decode_chronopulse(code: str, cipher: dict):
    alphabet = cipher["Alphabet"]
    reverse = {v: k for k, v in alphabet.items()}
    symbols = cipher["Symbols"]

    result = []
    current = ""
    invalid_chars = []

    for ch in code:
        if ch in ("□", "■", "_"):  # include lowercase prefix
            current += ch
        elif ch == "●":
            is_lower = current.startswith("_")
            key = current[1:] if is_lower else current
            letter = reverse.get(key, "?")
            if is_lower:
                letter = letter.lower()
            result.append(letter)
            if key not in reverse:
                invalid_chars.append(current)
            current = ""
        elif ch == "○":
            result.append(" ")
        elif ch in symbols:
            result.append(symbols[ch]["Represents"])
        else:
            result.append("?")
            invalid_chars.append(ch)

    if current:
        is_lower = current.startswith("_")
        key = current[1:] if is_lower else current
        letter = reverse.get(key, "?")
        if is_lower:
            letter = letter.lower()
        result.append(letter)
        if key not in reverse:
            invalid_chars.append(current)

    return "".join(result), invalid_chars

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
        output, invalid = encode_chronopulse(text, cipher)
    elif mode == "decode":
        output, invalid = decode_chronopulse(text, cipher)
    else:
        print("Invalid mode. Please type 'encode' or 'decode'.")
        return

    print("\nResult:\n")
    print(output)
    if invalid:
        print("\nInvalid/unsupported characters found:", ", ".join(invalid))


if __name__ == "__main__":
    main()

# By C4L