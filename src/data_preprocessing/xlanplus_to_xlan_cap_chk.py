import json
import sys


def get_replacements(file_ending, mode):
    if mode not in ["chk", "cap"]:
        return None  # Mode is invalid

    if file_ending == "json" or file_ending == "xlanplus":
        if mode == "chk":
            return {"$": "+", "!": "#", "x": "-"}
        elif mode == "cap":
            return {"+": "-", "#": "-", "$": "x", "!": "x"}
    elif file_ending == "tok":
        if mode == "chk":
            return {"79": "77", "80": "78", "81": "76"}
        elif mode == "cap":
            return {"77": "76", "78": "76", "79": "77", "80": "77", "81": "77"}

    return None  # File ending is invalid or not supported


def replace_in_file(input_file_path, output_file_path, replacements, file_ending):

    ### JSON ###

    if file_ending == "json":
        with open(input_file_path, "r") as input_file:
            data = json.load(input_file)

        for item in data:
            for key, value in item.items():
                if isinstance(value, str):
                    for old, new in replacements.items():
                        value = value.replace(old, new)
                    item[key] = value
                elif isinstance(value, list):
                    for i, str_val in enumerate(value):
                        for old, new in replacements.items():
                            str_val = str_val.replace(old, new)
                        value[i] = str_val

        with open(output_file_path, "w") as output_file:
            json.dump(data, output_file, indent=2)

    ### TOK and XLANPLUS ###

    elif file_ending in ["tok", "xlanplus"]:
        with open(input_file_path, "r") as input_file, open(
            output_file_path, "w"
        ) as output_file:
            for line in input_file:
                for old, new in replacements.items():
                    line = line.replace(old, new)
                output_file.write(line)
    else:
        print("Unsupported file format. Supported formats are json, tok, and xlanplus.")
        sys.exit(1)


if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python script.py <input_file_path> <output_file_path> <chk/cap>")
        sys.exit(1)

    input_file_path, output_file_path, mode = sys.argv[1:4]
    file_ending = input_file_path.split(".")[-1]

    replacements = get_replacements(file_ending, mode)
    if replacements is None:
        print("Invalid mode or file format. Supported modes are 'chk' and 'cap'.")
        print("Supported file formats are json, tok, and xlanplus.")
        sys.exit(1)

    replace_in_file(input_file_path, output_file_path, replacements, file_ending)
    print(f"Processing complete. Output written to {output_file_path}")
