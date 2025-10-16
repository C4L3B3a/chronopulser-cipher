# ChronoPulse Cipher Kit

**ChronoPulse** is a symbolic cipher language inspired by Morse code, using geometric and astral glyphs like `□`, `■`, `●`, `○`, and symbols like `☆`, `♤`, `♡`, `◇`, `♧`, `《》`, `¤`, `₩`, `÷`.  
It can **encode and decode messages** in Python, C#, and Lua using the same `chronopulse.json` cipher definition.

---

## Project Structure

```

ChronoPulse/
├── chronopulse.json          # Shared cipher map
├── python/
│   ├── chronopulse_encoder.py
│   ├── chronopulse_decoder.py
│   └── chronopulse_cli.py
├── csharp/
│   ├── ChronoPulseEncoder.cs
│   ├── ChronoPulseDecoder.cs
│   └── ChronoPulseCLI.cs
├── lua/
│   ├── chronopulse_encoder.lua
│   ├── chronopulse_decoder.lua
│   └── chronopulse_cli.lua
├── README.md
└── requirements.txt

````

---

## Requirements

### Python

- Python 3.8+
- Optional: `pyinstaller` to build standalone executables
```bash
pip install pyinstaller
````

### Lua

* Lua 5.4+ (or compatible)
* dkjson for JSON parsing

```bash
luarocks install dkjson
```

### C#

* .NET SDK 6+ (or 9 for cross-platform)

```bash
dotnet --version
```

---

## Symbols

| Symbol | Represents       |
| ------ | ---------------- |
| □      | dot              |
| ■      | dash             |
| ●      | End of letter    |
| ○      | Space / Word end |
| •      | Pause / Comma    |
| ☆      | !                |
| ♤      | ?                |
| ♡      | ...              |
| ◇      | (                |
| ♧      | )                |
| 《, 》   | "                |
| ¤      | #                |
| ₩      | $                |
| ÷      | %                |

---

## Python Usage

### Encode

```bash
python3 python/chronopulse_encoder.py
```

### Decode

```bash
python3 python/chronopulse_decoder.py
```

### CLI mode

```bash
python3 python/chronopulse_cli.py encode "Hello world!"
python3 python/chronopulse_cli.py decode "□□■●□■■●○☆"
```

### Build Standalone Executable

```bash
pyinstaller --onefile python/chronopulse_cli.py
```

Output: `dist/chronopulse_cli` (Windows `.exe`, macOS/Linux binary)

---

## C# Usage

### Run

```bash
dotnet run --project csharp/ChronoPulseEncoder.csproj
dotnet run --project csharp/ChronoPulseDecoder.csproj
```

### CLI Mode

```bash
dotnet run --project csharp/ChronoPulseCLI.csproj
```

### Build Executables

```bash
dotnet publish -c Release -r win-x64 --self-contained true
dotnet publish -c Release -r osx-x64 --self-contained true
dotnet publish -c Release -r linux-x64 --self-contained true
```

---

## Lua Usage

### Encode

```bash
lua lua/chronopulse_encoder.lua
```

### Decode

```bash
lua lua/chronopulse_decoder.lua
```

### CLI Mode

```bash
lua lua/chronopulse_cli.lua
```

---

## How It Works

1. **Encoder:** Converts normal text (letters, numbers, punctuation) into symbolic ChronoPulse code.
2. **Decoder:** Converts symbolic ChronoPulse code back into text.
3. **JSON Cipher:** The `chronopulse.json` file maps every character to its symbolic representation. Updating the JSON updates all encoders/decoders.

---

## Design Philosophy

* **Cryptic but reversible:** Code is visually mysterious but fully reversible.
* **Multi-platform:** Works in Python, C#, and Lua.
* **Modular:** Separate CLI, encoder, and decoder scripts.
* **Symbolic & artistic:** Uses unique glyphs to encode letters and symbols.

---

## License

**MIT License** – Free for personal, educational, or creative use.
You may copy, modify, and redistribute, but include this copyright notice.

```
MIT License

Copyright (c) 2025 C4L

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction...
```

---

## Examples

### Python CLI

```bash
python3 python/chronopulse_cli.py encode "Money#% (Test)!"
# Output: □■■□●□■□□●○¤₩÷◇□■□□●□■□●♧☆
```

```bash
python3 python/chronopulse_cli.py decode "□□■●□■■●○☆"
# Output: Hello!
```

### C# CLI

```bash
dotnet run --project csharp/ChronoPulseCLI.csproj
```

### Lua CLI

```bash
lua lua/chronopulse_cli.lua
```

---

## **`requirements.txt`** (Python)

```txt
pyinstaller>=6.0.0
````

---

By C4L