import json
from bitarray import bitarray
import os

def save(bitarray_data, filename, code_table):
    with open(filename, 'wb') as file:
        bitarray_data.tofile(file)
    # Save the code table
    with open(filename + '_codes.json', 'w') as file:
        json.dump(code_table, file)

def load(encoded_filename, code_table_filename):
    # Load binary file into a bitarray
    with open(encoded_filename, 'rb') as file:
        encoded_bitarray = bitarray()
        encoded_bitarray.fromfile(file)

    # Load the code table from a JSON file
    with open(code_table_filename, 'r') as file:
        code_table = json.load(file)

    return encoded_text, code_table

def create(filename):
    with open(filename, 'r') as file:
        text = file.read()

    # Create a frequency table
    freq_table = {}
    for char in text:
        if char in freq_table:
            freq_table[char] += 1
        else:
            freq_table[char] = 1

    # Create a binary code table
    code_table = {}
    for i, char in enumerate(freq_table.keys()):
        # Convert the index to a 6-bit binary number
        binary_code = format(i, '06b')
        code_table[char] = binary_code

    return code_table

def encode(filename, code_table):
    with open(filename, 'r') as file:
        text = file.read()

    # Encode the text
    encoded_text = ''.join(code_table[char] for char in text)

    # Convert the encoded text to a bitarray
    encoded_bitarray = bitarray(encoded_text)

    return encoded_bitarray

def decode(encoded_bitarray, code_table):
    # Convert the bitarray to a string of bits
    encoded_text = ''.join(str(b) for b in encoded_bitarray)

    # Reverse the code table
    reversed_code_table = {v: k for k, v in code_table.items()}

    # Split the encoded text into chunks of the length of the shortest code
    min_length = min(len(code) for code in code_table.values())
    chunks = [encoded_text[i:i+min_length] for i in range(0, len(encoded_text), min_length)]

    # Decode the text
    decoded_text = ''.join(reversed_code_table.get(chunk, '') for chunk in chunks)

    return decoded_text

def save_text_to_file(text, filename):
    with open(filename, 'w') as file:
        file.write(text)



def compare_files(file1, file2):
    with open(file1, 'r') as f1, open(file2, 'r') as f2:
        text1 = f1.read()
        text2 = f2.read()

    diff_count = sum(c1 != c2 for c1, c2 in zip(text1, text2))

    # If files have different lengths, add the difference to the count
    diff_count += abs(len(text1) - len(text2))

    return diff_count

def compare_file_sizes(file1, file2):
    size1 = os.path.getsize(file1)
    size2 = os.path.getsize(file2)

    if size1 > size2:
        smaller_percentage = (size1 - size2) / size1 * 100
        print(f"{file2} is {smaller_percentage}% smaller than {file1}")
    elif size2 > size1:
        smaller_percentage = (size2 - size1) / size2 * 100
        print(f"{file1} is {smaller_percentage}% smaller than {file2}")
    else:
        print("Both files are of the same size.")

codes = create('norm_hamlet.txt')
encoded_text = encode('norm_hamlet.txt', codes)
save(encoded_text, 'encoded_hamlet.txt',codes)
decoded_text = decode(encoded_text, codes)
save_text_to_file(decoded_text, 'decoded_hamlet.txt')
print(compare_files('norm_hamlet.txt', 'decoded_hamlet.txt'))
compare_file_sizes('norm_hamlet.txt', 'encoded_hamlet.txt')
