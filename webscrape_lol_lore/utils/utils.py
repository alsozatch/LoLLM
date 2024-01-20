import os

def read_file_into_array(filepath):
    """Reads a file and returns an array with each element being a line."""
    lines = []

    with open(filepath, 'r') as file:
        for line in file:
            # Append each line to the list, removing leading/trailing whitespace
            lines.append(line.strip())
    return lines

def save_string_to_file(text, file_path):
    """
    Save a string to a file.
    Creates the intermediate directories if they don't exist.

    :param text: The string to be saved to the file.
    :param file_path: The path to the file where the string will be saved.
    """
    try:
        # Create the directory if it doesn't exist
        directory = os.path.dirname(file_path)
        if not os.path.exists(directory):
            os.makedirs(directory)

        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(text)
        print(f'Successfully saved to {file_path}!')
    except Exception as e:
        print(f'Error: {e}')