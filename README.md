# ChronoPulse Cipher

ChronoPulse is a **geometric-symbolic cipher** that encodes text into a sequence of shapes and symbols such as `□■●○☆♤♡◇♧《》¤₩÷`.  
It is designed for readability, creativity, and experimental linguistics — similar in spirit to Morse code, but with a symbolic twist.

---

## Example

| Input | Encoded Output |
|-------|----------------|
| `HELLO` | `□□□□●□●□■□□●□■□□●■■■■●` |
| `HI!`   | `□□□□●□□●☆` |
| `TEST`  | `■●□●□□□●■●` |

---

## Cipher Structure

The cipher is defined in `chronopulse.json`:

- **Alphabet** → geometric letter patterns (`□`, `■`)
- **Control** → flow and spacing symbols (`●`, `○`, `•`)
- **Symbols** → punctuation and other marks (`☆`, `♤`, etc.)

Example excerpt:
```json
{
  "Alphabet": { "A": "□■", "B": "■■□", ... },
  "Symbols": {
    "☆": {"Represents": "!", "Type": "punctuation"},
    "♤": {"Represents": "?", "Type": "punctuation"}
  },
  "Control": {
    "●": "End of letter",
    "○": "Space/word end",
    "•": "Pause/comma"
  }
}
````

---

## Implementations

| Language | File              | Description                              |
| -------- | ----------------- | ---------------------------------------- |
| Python   | `chronopulse.py`  | CLI-based encoder/decoder                |
| C#       | `ChronoPulse.cs`  | Console app version                      |
| Lua      | `chronopulse.lua` | Lightweight interpreter-friendly version |

---

## Usage

### Python

```bash
python3 chronopulse.py
```

### C#

```bash
dotnet run
```

### Lua

```bash
lua chronopulse.lua
```

Then choose:

```
Mode (encode/decode): <encode or decode>
Input: <your text or code>
```

---

## Extending the Cipher

You can edit `chronopulse.json` to:

* Add new symbols or punctuation
* Change alphabet sequences
* Customize control flow

Any changes are automatically loaded at runtime — no recompilation needed.

---

## License

MIT License — free for modification, reuse, or study.
Created by the open source community for creative encryption and symbolic communication.

---

By C4L :D
