from collections import Counter


def check_duplicates_and_common_lines(
    file_1_path,
    file_2_path,
    delete_common=False,
    delete_duplicates_from_file_1=False,
    delete_duplicates_from_file_2=False,
):
    """
    Check for duplicate lines inside a sets and common lines between two sets.
    Optionally, remove duplicate or common lines.

    Args:
    - file_1_path (str): Path to the first file.
    - file_2_path (str): Path to the second file.
    - delete_common: Whether to delete common lines from the second file.
    - delete_duplicates_from_file_1: Whether to delete duplicate lines inside the first file.
    - delete_duplicates_from_file_2: Whether to delete duplicate lines inside the second file.

    Returns:
    - num_duplicate_training (int): Number of duplicate lines in the first file.
    - num_duplicate_validation (int): Number of duplicate lines in the second file.
    - num_common (int): Number of common lines between the two files.
    - duplicates_file_1 (set): Set of duplicate lines in the first file.
    - duplicates_file_2 (set): Set of duplicate lines in the second file.
    - common_lines (set): Set of common lines between the two files.
    """

    with open(file_1_path, "r") as f:
        lines_file_1 = f.readlines()

    with open(file_2_path, "r") as f:
        lines_file_2 = f.readlines()

    # Use Counter to count the number of occurrences of each line
    counter_file_1 = Counter(lines_file_1)
    counter_file_2 = Counter(lines_file_2)

    # Add all lines that occur more than once to a set
    duplicates_file_1 = {line for line, count in counter_file_1.items() if count > 1}
    duplicates_file_2 = {line for line, count in counter_file_2.items() if count > 1}

    # Use set intersection to find common lines
    common_lines = set(lines_file_1).intersection(set(lines_file_2))

    # Removes common lines from file 2
    if delete_common:
        lines_file_2 = [line for line in lines_file_2 if line not in common_lines]
        with open(file_2_path, "w") as f:
            f.writelines(lines_file_2)

    # Removes duplicate lines from file 1
    if delete_duplicates_from_file_1:
        lines_file_1 = [line for line in lines_file_1 if line not in duplicates_file_1]
        with open(file_1_path, "w") as f:
            f.writelines(lines_file_1)

    # Removes duplicate lines from file 2
    if delete_duplicates_from_file_2:
        lines_file_2 = [line for line in lines_file_2 if line not in duplicates_file_2]
        with open(file_2_path, "w") as f:
            f.writelines(lines_file_2)

    # Count the number of duplicate and common lines
    num_duplicate_training = len(duplicates_file_1)
    num_duplicate_validation = len(duplicates_file_2)
    num_common = len(common_lines)

    return (
        num_duplicate_training,
        num_duplicate_validation,
        num_common,
        duplicates_file_1,
        duplicates_file_2,
        common_lines,
    )
