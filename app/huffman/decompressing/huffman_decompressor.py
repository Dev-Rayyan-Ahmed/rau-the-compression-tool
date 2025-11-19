from app.huffman.huffman_main.hufman import create_huffman_tree
from app.huffman.fileHandler.files import read_compressed_file
import os


def byte_to_bits(byte_data: str):
    bits = ""
    for byte in byte_data:
        # Formatting, like 3-> 00000011 to 8 bits (from 1 byte)
        bits += format(byte, "08b")
    return bits


def huff_decompress_file(input_file, output_dir):
    freq_list, compressed_bytes, padding, ext = read_compressed_file(input_file)
    root = create_huffman_tree(freq_list)
    bitString = byte_to_bits(compressed_bytes)
    if padding > 0:
        # removing extra padding added to complete byte while encoding
        bitString = bitString[:-padding]

    decoded_bytes = []
    current_node = root
    for bit in bitString:
        current_node = current_node.left if bit == "0" else current_node.right
        # Reached EndPoint
        if current_node.left is None and current_node.right is None:
            decoded_bytes.append(current_node.byte)
            current_node = root  # Reset

    name, _ = os.path.splitext(os.path.basename(input_file))

    final_path = os.path.join(output_dir, name + ext)
    print(output_dir)
    with open(final_path, "wb") as f:
        f.write(bytes(decoded_bytes))
