import sys
import csv
import json

def convert_csv_to_json(input_path: str):
    """ CSV to JSON conversion logic """
    print(f"Reading file: {input_path}")
    json_data = []
    try:
        with open(input_path, "r") as f:
            csv_reader = csv.reader(f)

            # Reads the firs row as the header
            header = next(csv_reader, None) # Set to Non if default file is empty.
            if not header:
                print("CSV file is empty or has no header.")
                return "[]" # Returns an empty JSON array.
            print(f"Header row: {header}")

            for i,row in enumerate(csv_reader):
                print(f"Data row {i+1}: {row}")
                # Create a dictionary for each row using the header
                row_dict = dict(zip(header, row))
                json_data.append(row_dict)
            print(f"Successfully processed CSV file: {input_path}")
            
            #Convert the list of dictionaries to a JSON string
            return json.dumps(json_data, indent=4)

    except FileNotFoundError:
        print(f"Error: file not found - {input_path}")
        sys.exit(1)
    except StopIteration: # Handles empty file after trying to read header
        print("CSV file is empty.")
        return "[]"
    except Exception as e:
        print(f"CSV to JSON conversion failed: {str(e)}")
        sys.exit(1)
        

def convert_json_to_csv(input_path: str):
    """ JSON to CSV conversion logic """
    print(f"Reading file: {input_path}")
    try:
        with open(input_path, "r") as f:
            content = f.read()
        print(f"Successfully read ${len(content)} characters")
        # Add missing conversion logic
        return content
    except FileNotFoundError:
        print(f"Error: file not found - ${input_path}")
        sys.exit(1)
    except Exception as e:
        print(f"Conversion failed: ${str(e)}")
        sys.exit(1)