import argparse
import mimetypes

def main():
    parser = argparse.ArgumentParser(description="A data transformation tool for the busy dev.")

    # Add arguments
    parser.add_argument('file', help="Input file.")
    parser.add_argument('-o', '--output', help='output file.')
    parser.add_argument('-v', '--verbose', action='store_true', help='Enable verbose output.')

    # Parse arguments
    args = parser.parse_args()
    mime_type, _ = mimetypes.guess_type(args.file)

    # CLI logic goes here
    print(f"Processing ${args.file}")
    if mime_type:
        print(f"Detected MIME type: {mime_type}")
    if args.verbose:
        print("Enabled verbosity.")


if __name__ == "__main__":
    main()