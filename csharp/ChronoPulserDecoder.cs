using System;
using System.Collections.Generic;
using System.IO;
using System.Text.Json;

class ChronoPulseDecoder
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

        var reverse = new Dictionary<string, string>();
        foreach (var kv in alphabet)
            reverse[kv.Value] = kv.Key;

        Console.Write("Enter code to decode: ");
        string code = Console.ReadLine();
        Console.WriteLine(Decode(code, reverse, symbols));
    }

    static string Decode(string code, Dictionary<string, string> reverse, Dictionary<string, JsonElement> symbols)
    {
        string result = "", current = "";

        foreach (char s in code)
        {
            if (s == '□' || s == '■')
                current += s;
            else if (s == '●')
            {
                if (reverse.ContainsKey(current))
                    result += reverse[current];
                current = "";
            }
            else if (s == '○')
                result += " ";
            else if (s == '•')
            {
                result += ", ";
                current = "";
            }
            else if (symbols.ContainsKey(s.ToString()))
            {
                var rep = symbols[s.ToString()].GetProperty("Represents").GetString();
                result += rep;
            }
            else
                result += "?";
        }

        if (current.Length > 0 && reverse.ContainsKey(current))
            result += reverse[current];

        return result.Trim();
    }
}
