import json

def load_cipher(path="../chronopulse.json"):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def decode_chronopulse(code, cipher):
    alphabet = cipher["Alphabet"]
    reverse = {v: k for k, v in alphabet.items()}
    symbols = cipher["Symbols"]

    result, current = [], ""

    for s in code:
        if s in ("□", "■"):
            current += s
        elif s == "●":
            if current:
                result.append(reverse.get(current, "?"))
                current = ""
        elif s == "○":
            result.append(" ")
        elif s == "•":
            result.append(", ")
            current = ""
        elif s in symbols:
            result.append(symbols[s]["Represents"])
        else:
            result.append("?")

    if current:
        result.append(reverse.get(current, "?"))

    return "".join(result).strip()

if __name__ == "__main__":
    cipher = load_cipher()
    code = input("Enter code to decode: ")
    print(decode_chronopulse(code, cipher))
