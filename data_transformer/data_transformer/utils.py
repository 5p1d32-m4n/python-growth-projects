import sys
import csv
import io
import json
import pandas as pd
import re
import shlex


def convert_csv_to_json(input_path: str):
    """ CSV to JSON conversion logic """
    print(f"Reading file: {input_path}")
    json_data = []
    try:
        with open(input_path, "r") as f:
            csv_reader = csv.reader(f)

            # Reads the firs row as the header
            # Set to Non if default file is empty.
            header = next(csv_reader, None)
            if not header:
                print("CSV file is empty or has no header.")
                return "[]"  # Returns an empty JSON array.
            print(f"Header row: {header}")

            for i, row in enumerate(csv_reader):
                print(f"Data row {i+1}: {row}")
                # Create a dictionary for each row using the header
                row_dict = dict(zip(header, row))
                json_data.append(row_dict)
            print(f"Successfully processed CSV file: {input_path}")

            # Convert the list of dictionaries to a JSON string
            return json.dumps(json_data, indent=4)

    except FileNotFoundError:
        print(f"Error: file not found - {input_path}")
        sys.exit(1)
    except StopIteration:  # Handles empty file after trying to read header
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
            raw_json_data = json.loads(f.read())

        # Normalize JSON data to a list of items
        if isinstance(raw_json_data, dict):
            processed_json_data = [raw_json_data]
        elif isinstance(raw_json_data, list):
            processed_json_data = raw_json_data
        else:
            # Handle cases where JSON is not a list or dict (e.g., a single string, number)
            print(
                f"Unsupported top-level JSON type: {type(raw_json_data)}. Expected a list or an object.")
            return ""

        # Extract keys and filter for dictionary items in a single pass
        all_keys = set()
        dict_items_for_csv = []
        for item in processed_json_data:
            if isinstance(item, dict):
                all_keys.update(item.keys())
                dict_items_for_csv.append(item)

        # If no keys were found (e.g., empty JSON, list of non-dicts, or list of empty dicts)
        if not all_keys:
            print(
                "JSON data is empty, contains no dictionary objects, or dictionary objects have no keys.")
            return ""

        headers = sorted(list(all_keys))

        output_csv = io.StringIO()
        writer = csv.DictWriter(
            output_csv, fieldnames=headers, extrasaction='ignore')

        writer.writeheader()
        for item in dict_items_for_csv:  # Iterate over the pre-filtered list of dictionaries
            writer.writerow(item)

        return output_csv.getvalue()

    except FileNotFoundError:
        print(f"Error: file not found - {input_path}")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON file - {input_path}. Details: {str(e)}")
        sys.exit(1)
    except Exception as e:
        print(f"JSON to CSV conversion failed: {str(e)}")
        sys.exit(1)


def parse_filter_string(filter_string: str):
    """
    Parse a single filter stirng like "Column = 'Value'", "Age > 30", etc.
    Parse a filter string into a dict  with 'column', 'operator', and 'value'.
    Handles quoted strings & numberical values.
    """
    # Regex to capture column name, operator and value.
    # Group 1: Column name (alphanumeric and underscores)
    # Group 2: Operator (e.g., =, >, <, !=, >=, <=, contains, like, in)
    # Group 3: Value (quoted string, number or bare word)

    match = re.match(
        r"^\s*([a-zA-Z_][a-zA-Z0-9_]*)\s*([=!><]+|contains|like|in|startswith|endswith)\s*(.+)\s*$",
        filter_string,
        re.IGNORECASE
    )

    if not match:
        raise ValueError(
            f"Invalid filter format: '{filter_string}', Expected format: 'Columnt Operator Value'")
    column = match.group(1)
    operator = match.group(2).lower()
    value_str = match.group(3).strip()

    # Now I'm going to parse the value string inot its appropriate type.
    return {'column': column, 'operator': operator, 'value': value_str}


def filter_csv(csv_row, filter_cond: dict):
    """ Filter CSV data based on provided arguments """
    column = filter_cond['column']
    operator = filter_cond['operator']
    value = filter_cond['value']

    # Get the value from the csv row (Also handle if columns doesn't exist)
    row_value = csv_row.get(column, None)

    # Perform comparison based on the operator:
    if operator == '=':
        return str(row_value) == str(value)
    elif operator == '==':
        return str(row_value) == str(value)
    elif operator == '!=':
        return str(row_value) != str(value)
    elif operator == '>':
        return str(row_value) > str(value)
    elif operator == '<':
        return str(row_value) < str(value)
    elif operator == '>=':
        return str(row_value) >= str(value)
    elif operator == '<=':
        return str(row_value) <= str(value)
    elif operator.lower() == 'contains':
        return str(value) in str(row_value)
    elif operator.lower() == 'like':
        return str(value) in str(row_value)
    elif operator.lower() == 'in':
        return str(value) in str(row_value)
    else:
        raise ValueError(f"Unsupported operator: {operator}")
    return data


def reduce_csv(input_path: str, filter_args: str):
    """ Filter CSV data based on provided arguments """
    print(f"Reading file: {input_path}")
    try:
        with open(input_path, "r") as f:
            csv_reader = csv.DictReader(f)
            filter_dict = parse_filter_string(filter_args)
            data = [row for row in csv_reader if filter_csv(row, filter_dict)]
            print(f"data for csv filtered: {data}")
            return data
    except FileNotFoundError:
        print(f"Error: file not found - {input_path}")
        sys.exit(1)
    except Exception as e:
        print(f"CSV filtering has failed: {str(e)}")
        sys.exit(1)
