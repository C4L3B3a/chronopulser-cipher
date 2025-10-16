using System;

class ChronoPulseCLI
{
    static void Main()
    {
        Console.Write("Choose mode (encode/decode): ");
        string mode = Console.ReadLine().ToLower();
        Console.Write("Enter text/code: ");
        string input = Console.ReadLine();

        if (mode == "encode")
            ChronoPulseEncoder.Main();
        else if (mode == "decode")
            ChronoPulseDecoder.Main();
        else
            Console.WriteLine("Invalid mode");
    }
}
