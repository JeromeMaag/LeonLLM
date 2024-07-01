"""
Decode Tokenized Data using Predefined Tokens
---------------------------------------------

This script is designed to decode data that has previously been tokenized. 
It reverts the tokenized data back into its original form using a set of predefined tokens 
provided in a JSON file.

The script is executed from the command line and requires three arguments: 
1. The path to the JSON token file, 
2. The path to the file containing tokenized data, 
3. The output file where the decoded data should be saved.

Example:
    Command line:
        python decoder.py tokens.json tokenized_data.txt decoded_data.txt

    This command will read the tokenized data from 'tokenized_data.txt', decode it using 
    the mappings specified in 'tokens.json', and then write the original (decoded) data 
    to 'decoded_data.txt'.
"""

import json
import argparse
from src.tokenizer.tokenizer import get_token_file


def get_buffer_for_token(token, tokens):
    """
    Retrieve the original string (buffer) that corresponds to a given token.

    Args:
    token (int): The token for which to find the corresponding string.
    tokens (dict): A dictionary of tokens mapped to their respective strings.

    Returns:
    str: The original string corresponding to the provided token, or None if not found.
    """
    for category, items in tokens.items():
        for buffer, token_value in items.items():
            if token == token_value:
                return buffer
    return None


def detokenize_data(tokenized_data, notation):
    """
    Reverts tokenized data back to its original form based on provided token mappings.

    Args:
    tokenized_data (str): A string of tokenized data.
    notation (str): The notation for which the token mappings are defined.

    Returns:
    str: The decoded data as a single string.

    Example:
        Assuming the function is imported into another script, it can be used as follows:

        >> from decoder import detokenize_data
        >> tokenized_data_str = "some tokenized data string"
        >> token_file_path = "path/to/your/tokens.json"
        >> decoded_result = detokenize_data(tokenized_data_str, token_file_path)
        >> print(decoded_result)
    """
    token_path = get_token_file(notation)
    with open(token_path, "r") as file:
        tokens = json.load(file)

    decoded_data = ""
    split_data = tokenized_data.split()

    for token in split_data:
        buffer = get_buffer_for_token(int(token), tokens)
        if buffer is not None:
            # replace game separator with newline
            if buffer in tokens["gameSeparator"]:
                decoded_data += "\n"
            # add space after every move
            elif buffer in tokens["pieces"]:
                decoded_data += " " + buffer
            elif buffer in tokens["squares"]:
                decoded_data += buffer
            elif buffer in tokens["paddingToken"]:
                continue
            elif buffer in tokens["plusTokens"]:
                decoded_data += buffer
            else:
                decoded_data += " " + buffer
        # remove " " from the beginning of the string
        if decoded_data.startswith(" "):
            decoded_data = decoded_data[1:]
    # replace "\n " with "\n" to remove extra space at the beginning of each game
    decoded_data = decoded_data.replace("\n ", "\n")
    return decoded_data


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Decode tokenized data.")
    parser.add_argument(
        "notation", help="The notation for which the token mappings should be used."
    )
    parser.add_argument(
        "data_path",
        help="Path to the input data file containing tokenized data.",
    )
    parser.add_argument(
        "out_path", help="Path to the output file to store decoded data."
    )
    args = parser.parse_args()

    with open(args.notation, "r") as file:
        tokenized_data = file.read()

    decoded_data = detokenize_data(tokenized_data, args.notation)

    with open(args.out_path, "w") as out_file:
        out_file.write(decoded_data)
