import json

def load_cipher(path="../chronopulse.json"):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def encode_chronopulse(text, cipher):
    alphabet = cipher["Alphabet"]
    symbols = {v["Represents"]: k for k, v in cipher["Symbols"].items()}

    result = []
    for char in text:
        if char.upper() in alphabet:
            result.append(alphabet[char.upper()] + "●")
        elif char == " ":
            result.append("○")
        elif char in [",", ".", ";", ":"]:
            result.append("•")
        elif char in symbols:
            result.append(symbols[char])
        else:
            result.append("?")
    return "".join(result)

if __name__ == "__main__":
    cipher = load_cipher()
    text = input("Enter text to encode: ")
    print(encode_chronopulse(text, cipher))
