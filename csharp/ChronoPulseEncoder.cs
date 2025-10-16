using System;
using System.Collections.Generic;
using System.IO;
using System.Text.Json;

class ChronoPulseEncoder
{
    static void Main()
    {
        var cipherJson = File.ReadAllText("../chronopulse.json");
        var cipher = JsonSerializer.Deserialize<Dictionary<string, object>>(cipherJson);
        var alphabet = JsonSerializer.Deserialize<Dictionary<string, string>>(
            ((JsonElement)cipher["Alphabet"]).GetRawText()
        );
        var symbols = JsonSerializer.Deserialize<Dictionary<string, JsonElement>>(
            ((JsonElement)cipher["Symbols"]).GetRawText()
        );

        var symbolMap = new Dictionary<string, string>();
        foreach (var kv in symbols)
            symbolMap[kv.Value.GetProperty("Represents").GetString()] = kv.Key;

        Console.Write("Enter text to encode: ");
        string text = Console.ReadLine();
        Console.WriteLine(Encode(text, alphabet, symbolMap));
    }

    static string Encode(string text, Dictionary<string, string> alphabet, Dictionary<string, string> symbols)
    {
        string result = "";
        foreach (char c in text)
        {
            string ch = c.ToString();
            if (alphabet.ContainsKey(ch.ToUpper()))
                result += alphabet[ch.ToUpper()] + "●";
            else if (ch == " ")
                result += "○";
            else if (",.;:".Contains(ch))
                result += "•";
            else if (symbols.ContainsKey(ch))
                result += symbols[ch];
            else
                result += "?";
        }
        return result;
    }
}
