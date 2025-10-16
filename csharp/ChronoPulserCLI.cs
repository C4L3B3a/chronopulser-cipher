// ==========================================================
// ChronoPulse Cipher - Encoder/Decoder (C#)
// ----------------------------------------------------------
// Author: Open Source Community
// License: MIT
//
// Description:
//   Reads a cipher definition from chronopulse.json,
//   then encodes or decodes ChronoPulse text using geometric symbols.
// ==========================================================

using System;
using System.IO;
using System.Collections.Generic;
using System.Text.Json;

public class ChronoPulseCipher
{
    public Dictionary<string, string> Alphabet { get; set; }
    public Dictionary<string, SymbolData> Symbols { get; set; }

    public class SymbolData
    {
        public string Represents { get; set; }
        public string Type { get; set; }
    }

    public static ChronoPulseCipher Load(string path)
    {
        string json = File.ReadAllText(path);
        return JsonSerializer.Deserialize<ChronoPulseCipher>(json);
    }
}

public class ChronoPulse
{
    public static string Encode(string text, ChronoPulseCipher cipher)
    {
        var result = new List<string>();
        var symbols = new Dictionary<string, string>();

        // Build reverse map for symbol representation
        foreach (var kv in cipher.Symbols)
            symbols[kv.Value.Represents] = kv.Key;

        foreach (char c in text)
        {
            string upper = c.ToString().ToUpper();

            if (cipher.Alphabet.ContainsKey(upper))
                result.Add(cipher.Alphabet[upper] + "●");
            else if (c == ' ')
                result.Add("○");
            else if (symbols.ContainsKey(c.ToString()))
                result.Add(symbols[c.ToString()]);
            else
                result.Add("?");
        }

        return string.Join("", result);
    }

    public static string Decode(string code, ChronoPulseCipher cipher)
    {
        var reverseAlpha = new Dictionary<string, string>();
        foreach (var kv in cipher.Alphabet)
            reverseAlpha[kv.Value] = kv.Key;

        var result = new List<string>();
        string current = "";

        foreach (char ch in code)
        {
            if (ch == '□' || ch == '■')
                current += ch;
            else if (ch == '●')
            {
                result.Add(reverseAlpha.ContainsKey(current) ? reverseAlpha[current] : "?");
                current = "";
            }
            else if (ch == '○')
                result.Add(" ");
            else if (cipher.Symbols.ContainsKey(ch.ToString()))
                result.Add(cipher.Symbols[ch.ToString()].Represents);
            else
                result.Add("?");
        }

        if (current.Length > 0)
            result.Add(reverseAlpha.ContainsKey(current) ? reverseAlpha[current] : "?");

        return string.Join("", result);
    }

    public static void Main()
    {
        var cipher = ChronoPulseCipher.Load("chronopulse.json");

        Console.WriteLine("=== ChronoPulse v2 Encoder/Decoder ===");
        Console.Write("Mode (encode/decode): ");
        string mode = Console.ReadLine().Trim().ToLower();

        Console.Write("Input: ");
        string input = Console.ReadLine();

        string output = mode switch
        {
            "encode" => Encode(input, cipher),
            "decode" => Decode(input, cipher),
            _ => "Invalid mode"
        };

        Console.WriteLine("\nResult:");
        Console.WriteLine(output);
    }
}

// By C4L