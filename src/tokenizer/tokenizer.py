"""
Tokenize Data using Predefined Tokens
-------------------------------------

This script allows for the tokenization of raw data into a more manageable tokenized format, 
utilizing a predefined set of tokens provided within a JSON file.

The script is run via the command line and requires three arguments: 
1. The path to the JSON token file, 
2. The path to the raw data file, 
3. The output file where the tokenized data should be saved.

Example:
    Command line:
        python tokenizer.py tokens.json input_data.txt output_tokenized.txt

    This command will read the data from 'input_data.txt', tokenize it based on 'tokens.json', 
    and write the tokenized output to 'output_tokenized.txt'.
"""

import json
import argparse
import multiprocessing


def get_token_file(notation):
    """
    Retrieves the token file corresponding to a given notation.

    Args:
    notation (str): The notation for which the token file is required. E.g. "xLAN", "xLANplus".

    Returns:
    str: The file path to the token file corresponding to the provided notation.

    Raises:
    ValueError: If the notation is not found in the notations.json file.
    """
    notation_file = "./src/notation.json"
    with open(notation_file, "r") as file:
        notations = json.load(file)

    if notation in notations:
        return notations[notation]["token_file"]
    else:
        raise ValueError(f"Notation '{notation}' not found in {notation_file} File.")


def get_token_for_buffer(buf, tokens):
    """
    Identifies the token corresponding to a buffer string, if it exists.

    Args:
    buf (str): The buffer string to be checked against the tokens.
    tokens (dict): A dictionary of token categories, each containing specific tokens.

    Returns:
    str, str: The identified token value and its category, if found. Otherwise, None.
    """
    for category, items in tokens.items():
        if buf in items:
            return items[buf], category
    return None, None


def tokenize_data(input_data, notation):
    """
    Tokenizes the input data based on the provided token mappings.

    Args:
    input_data (str): The raw input data as a string.
    notation (str): The notation for which the token mappings should be used.

    Returns:
    str: The tokenized data as a single string.

    Example:
        Assuming the function is imported into another script, it can be used as follows:

        >> from tokenizer import tokenize_data
        >> raw_data = "raw data string"
        >> token_file_path = "path/to/your/tokens.json"
        >> tokenized_result = tokenize_data(raw_data, token_file_path)
        >> print(tokenized_result)
    """
    token_path = get_token_file(notation)
    with open(token_path, "r") as file:
        tokens = json.load(file)

    tokenized_data = []
    tokenized_data.append(tokens["paddingToken"]["STARTSEQ"])  # add start token
    buffer = ""

    for char in input_data:
        buffer += char
        if buffer == "\n":
            buffer = ""
            tokenized_data.append("\n")
            continue
        token_value, token_category = get_token_for_buffer(buffer, tokens)

        if token_value is not None:
            tokenized_data.append(token_value)
            buffer = ""

            # add game separator token after each game
            if token_category == "results":
                tokenized_data.append(tokens["gameSeparator"]["GAMESEP"])

        # reset buffer if not matching any start of a valid value
        elif not any(
            key.startswith(buffer)
            for category, items in tokens.items()
            for key in items
        ):
            buffer = ""

    return " ".join(map(str, tokenized_data))


def worker(chunk, tokens):
    """
    Called by the multiprocessing pool to tokenize a chunk of data.

    Args:
    chunk (str): The chunk of data to be tokenized.
    tokens (dict): A dictionary of token categories, each containing specific tokens.
    """
    tokenized_data = []
    buffer = ""

    for char in chunk:
        buffer += char
        if buffer == "\n":
            buffer = ""
            tokenized_data.append("\n")
            continue
        token_value, token_category = get_token_for_buffer(buffer, tokens)

        if token_value is not None:
            tokenized_data.append(token_value)
            buffer = ""

            if token_category == "results":
                tokenized_data.append(tokens["gameSeparator"]["GAMESEP"])

        elif not any(
            key.startswith(buffer)
            for category, items in tokens.items()
            for key in items
        ):
            buffer = ""

    return tokenized_data


def tokenize_data_multiprocessing(input_data, notation, out_path, batch_size=100000):
    """
    Tokenizes the input data based on the provided token mappings, using multiprocessing to speed up the process.

    Args:
    input_data (str): The raw input data as a string.
    notation (str): The notation for which the token mappings should be used.
    out_path (str): File path to the output file where the tokenized data will be stored.
    batch_size (int): The number of lines to process at a time. Defaults to 100000.
    """
    token_path = get_token_file(notation)
    with open(token_path, "r") as file:
        tokens = json.load(file)

    # Determine the number of available CPU cores
    num_cores = multiprocessing.cpu_count()

    # Split the input data into lines and then into chunks of lines
    lines = input_data.splitlines(keepends=True)
    chunks = [
        "".join(lines[i : i + batch_size]) for i in range(0, len(lines), batch_size)
    ]
    result = []
    for chunk in enumerate(chunks):
        lines = chunk[1].splitlines(keepends=True)
        process_chunk_size = len(lines) // num_cores
        process_chunks = [
            "".join(lines[i : i + process_chunk_size])
            for i in range(0, len(lines), process_chunk_size)
        ]

        # Initialize multiprocessing pool
        pool = multiprocessing.Pool(processes=num_cores)

        # Map the worker function to the data chunks
        results = pool.starmap(worker, [(chunk, tokens) for chunk in process_chunks])

        print(f"Chunks done {chunk[0]+1}/{len(chunks)}", end="\r")
        # Close the pool and wait for the work to finish
        pool.close()
        pool.join()
        tokenized_data = " ".join(
            map(str, [item for sublist in results for item in sublist])
        )

        with open(out_path, "a") as out_file:
            out_file.write(tokenized_data)


def tokenize_file(
    notation, data_path, out_path, multiprocessing=True, batch_size=100000
):
    """
    The main function that reads input data, tokenizes it, and writes the tokenized data to an output file.

    Args:
    - notation (str): The notation for which the token mappings should be used.
    - data_path (str): Path to the input data file containing raw data to be tokenized.
    - out_path (str): Path to the output file where the tokenized data will be stored.
    - multiprocessing (bool): Whether to use multiprocessing to speed up the tokenization process.
    """
    with open(data_path, "r") as file:
        input_data = file.read()

    if multiprocessing:
        tokenize_data_multiprocessing(
            input_data=input_data,
            notation=notation,
            out_path=out_path,
            batch_size=batch_size,
        )
    else:
        tokenized_data = tokenize_data(input_data=input_data, notation=notation)

    if not multiprocessing:
        with open(out_path, "w") as out_file:
            out_file.write(tokenized_data)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Tokenize raw data using predefined tokens from a JSON file."
    )
    parser.add_argument(
        "notation", help="The notation for which the token mappings should be used."
    )
    parser.add_argument(
        "data_path",
        help="Path to the input data file containing raw data to be tokenized.",
    )
    parser.add_argument(
        "out_path",
        help="Path to the output file where the tokenized data will be stored.",
    )
    args = parser.parse_args()

    tokenize_file(args.notation, args.data_path, args.out_path)
