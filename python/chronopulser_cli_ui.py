#!/usr/bin/env python3
# ==========================================================
# ChronoPulse Cipher - Encoder/Decoder - UI Version
# ----------------------------------------------------------
# Author: Open Source Community
# License: MIT
#
# Description:
#   Encodes and decodes messages using the ChronoPulse Cipher.
#   Supports lowercase letters, symbols, and <utf=N> numeric encoding.
#   UI Version may be buggier.
# ==========================================================
import tkinter as tk
from tkinter import scrolledtext, messagebox, filedialog, ttk
import json
import os
import traceback
import secrets
import platform
import re

# -------------------------------
# Crash Handler
# -------------------------------
def handle_crash(project_name, reason="Exception", exception=None):
    crash_id = ''.join(secrets.choice("abcdefghijklmnopqrstuvwxyz0123456789") for _ in range(12))
    os_name = platform.system()
    extra_info = f"Reason: {reason}\nCrash ID: {crash_id}\nOS: {os_name}"
    if exception:
        extra_info += f"\nException (truncated): {exception[:800]}"
    else:
        stack = "".join(traceback.format_stack(limit=5))
        extra_info += f"\nStack trace (truncated): {stack[:800]}"
    root = tk.Tk()
    root.withdraw()
    messagebox.showerror(f"{project_name} crashed!", extra_info)
    root.destroy()
    print(f"{project_name} crashed! Crash ID: {crash_id}")

# -------------------------------
# Load cipher
# -------------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DEFAULT_CIPHER_PATH = os.path.join(BASE_DIR, "chronopulse.json")

def load_cipher(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        handle_crash("ChronoPulser", reason="Failed loading cipher", exception=str(e))
        raise SystemExit(1)

# -------------------------------
# UTF Mapping
# -------------------------------
utf_map = {str(i+1): chr(97+i) for i in range(26)}

# -------------------------------
# Encode / Decode
# -------------------------------
def encode(text, cipher):
    alphabet = cipher["Alphabet"]
    symbols = cipher["Symbols"]
    symbol_map = {v["Represents"]: k for k, v in symbols.items()}
    result = []
    invalid_chars = []
    utf_pattern = re.compile(r"<utf=(\d+)>")
    i = 0
    while i < len(text):
        m = utf_pattern.match(text, i)
        if m:
            num = m.group(1)
            c = chr(96 + int(num)) if num.isdigit() and 1 <= int(num) <= 26 else "?"
            symbol = alphabet.get(c.upper(), "?")
            if c.islower():
                symbol = "_" + symbol  # lowercase prefix
            result.append(symbol + "●")
            i += len(m.group(0))
            continue

        c = text[i]
        upper = c.upper()
        if upper in alphabet:
            symbol = alphabet[upper]
            if c.islower():
                symbol = "_" + symbol
            result.append(symbol + "●")
        elif c == " ":
            result.append("○")
        elif c in symbol_map:
            result.append(symbol_map[c])
        else:
            result.append("?")
            invalid_chars.append(c)
        i += 1
    return "".join(result), invalid_chars

def decode(code, cipher):
    alphabet = cipher["Alphabet"]
    symbols = cipher["Symbols"]
    reverse = {v: k for k, v in alphabet.items()}
    result, current, invalid_chars = [], "", []
    for s in code:
        if s in ["□","■","_"]:  # include lowercase prefix
            current += s
        elif s == "●":
            is_lower = current.startswith("_")
            key = current[1:] if is_lower else current
            letter = reverse.get(key, "?")
            if is_lower:
                letter = letter.lower()
            result.append(letter)
            if key not in reverse:
                invalid_chars.append(current)
            current = ""
        elif s == "○":
            result.append(" ")
        elif s in symbols:
            result.append(symbols[s]["Represents"])
        else:
            result.append("?")
            invalid_chars.append(s)
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

# -------------------------------
# GUI
# -------------------------------
class ChronoPulserGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("ChronoPulser GUI")
        self.master.geometry("800x600")
        self.master.configure(bg="#20242a")

        # Load default cipher
        self.cipher = load_cipher(DEFAULT_CIPHER_PATH)

        # Cipher selection dropdown
        tk.Label(master, text="Select Cipher JSON:", fg="white", bg="#20242a").pack(pady=5)
        self.cipher_var = tk.StringVar(value=DEFAULT_CIPHER_PATH)
        self.cipher_dropdown = ttk.Combobox(master, textvariable=self.cipher_var, width=50)
        self.cipher_dropdown.pack()
        self.cipher_dropdown.bind("<<ComboboxSelected>>", self.load_selected_cipher)

        # Title
        tk.Label(master, text="ChronoPulser Cipher", fg="#5ad", bg="#20242a",
                 font=("Consolas", 24, "bold")).pack(pady=10)

        # Mode selection
        self.mode_var = tk.StringVar(value="encode")
        tk.Radiobutton(master, text="Encode", variable=self.mode_var, value="encode", bg="#20242a", fg="white").pack()
        tk.Radiobutton(master, text="Decode", variable=self.mode_var, value="decode", bg="#20242a", fg="white").pack()

        # Input
        tk.Label(master, text="Input", fg="white", bg="#20242a").pack()
        self.input_box = scrolledtext.ScrolledText(master, wrap=tk.WORD, width=80, height=7, font=("Consolas",12))
        self.input_box.pack(pady=5)

        # Buttons
        frame_buttons = tk.Frame(master, bg="#20242a")
        frame_buttons.pack(pady=5)
        tk.Button(frame_buttons, text="Process", command=self.process, bg="#5ad", fg="black").grid(row=0, column=0, padx=5)
        tk.Button(frame_buttons, text="Clear Input", command=lambda: self.input_box.delete("1.0", tk.END), bg="#f55", fg="white").grid(row=0, column=1, padx=5)
        tk.Button(frame_buttons, text="Clear Output", command=lambda: self.output_box.delete("1.0", tk.END), bg="#f55", fg="white").grid(row=0, column=2, padx=5)
        tk.Button(frame_buttons, text="Copy Output", command=self.copy_output, bg="#5ad", fg="black").grid(row=0, column=3, padx=5)
        tk.Button(frame_buttons, text="Load from File", command=self.load_file, bg="#5ad", fg="black").grid(row=0, column=4, padx=5)
        tk.Button(frame_buttons, text="Save Output", command=self.save_file, bg="#5ad", fg="black").grid(row=0, column=5, padx=5)

        # Output
        tk.Label(master, text="Output", fg="white", bg="#20242a").pack()
        self.output_box = scrolledtext.ScrolledText(master, wrap=tk.WORD, width=80, height=10, font=("Consolas",12))
        self.output_box.pack(pady=5)

    # -------------------------------
    # Methods
    # -------------------------------
    def load_selected_cipher(self, event=None):
        path = self.cipher_var.get()
        if os.path.isfile(path):
            self.cipher = load_cipher(path)
        else:
            messagebox.showerror("Error", f"Cipher file not found:\n{path}")

    def process(self):
        try:
            text = self.input_box.get("1.0", tk.END).strip()
            if not text:
                messagebox.showwarning("Warning", "No input provided!")
                return
            if self.mode_var.get() == "encode":
                output, invalid = encode(text, self.cipher)
            else:
                output, invalid = decode(text, self.cipher)
            self.output_box.delete("1.0", tk.END)
            self.output_box.insert(tk.END, output)
            if invalid:
                messagebox.showwarning("Invalid Characters Detected", f"The following characters could not be encoded/decoded:\n{', '.join(set(invalid))}")
        except Exception as e:
            handle_crash("ChronoPulser GUI", reason="Processing error", exception=traceback.format_exc())

    def copy_output(self):
        output = self.output_box.get("1.0", tk.END).strip()
        if output:
            self.master.clipboard_clear()
            self.master.clipboard_append(output)
            messagebox.showinfo("Copied", "Output copied to clipboard!")

    def load_file(self):
        file_path = filedialog.askopenfilename(title="Open Text File", filetypes=[("Text Files", "*.txt")])
        if file_path:
            with open(file_path, "r", encoding="utf-8") as f:
                self.input_box.delete("1.0", tk.END)
                self.input_box.insert(tk.END, f.read())

    def save_file(self):
        file_path = filedialog.asksaveasfilename(title="Save Output", defaultextension=".txt",
                                                 filetypes=[("Text Files", "*.txt")])
        if file_path:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(self.output_box.get("1.0", tk.END).strip())

# -------------------------------
# Run GUI
# -------------------------------
if __name__ == "__main__":
    try:
        root = tk.Tk()
        app = ChronoPulserGUI(root)
        root.mainloop()
    except Exception:
        handle_crash("ChronoPulser GUI", reason="Unhandled Exception", exception=traceback.format_exc())

# By C4L