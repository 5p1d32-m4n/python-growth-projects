import argparse
import mimetypes
import json
from utils import convert_csv_to_json, convert_json_to_csv


def main():
    parser = argparse.ArgumentParser(
        description="A data transformation tool for the busy dev.")

    # Add arguments
    parser.add_argument('file', help="Input file.")
    parser.add_argument('-o', '--output', help='output file.')
    parser.add_argument('-v', '--verbose', action='store_true',
                        help='Enable verbose output.')

    # Parse arguments
    args = parser.parse_args()
    mime_type, _ = mimetypes.guess_type(args.file)

    # CLI logic goes here
    print(f"Processing ${args.file}")
    if mime_type:
        print(f"Detected MIME type: {mime_type}")
    if mime_type == "text/csv":
        print("CSV file detected.")
        data = convert_csv_to_json(args.file)
        if args.output:
            with open(args.output, 'w') as f:
                f.write(data)
    if mime_type == "application/json":
        print("JSON file detected.")
        data = convert_json_to_csv(args.file)
        if args.output:
            with open(args.output, 'w') as f:
                f.write(data)
    if args.verbose:
        print("Enabled verbosity.")


if __name__ == "__main__":
    main()
