import argparse
from chronopulse_encoder import encode_chronopulse, load_cipher
from chronopulse_decoder import decode_chronopulse

def main():
    parser = argparse.ArgumentParser(description="ChronoPulse CLI")
    parser.add_argument("mode", choices=["encode", "decode"], help="Operation mode")
    parser.add_argument("input", help="Text to encode or code to decode")
    parser.add_argument("--json", default="../chronopulse.json", help="Path to JSON cipher")
    args = parser.parse_args()

    cipher = load_cipher(args.json)
    if args.mode == "encode":
        print(encode_chronopulse(args.input, cipher))
    else:
        print(decode_chronopulse(args.input, cipher))

if __name__ == "__main__":
    main()
