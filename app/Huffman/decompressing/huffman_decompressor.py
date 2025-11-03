from app.Huffman.huffman_main.hufman import create_huffman_tree
from app.Huffman.fileHandler.files import read_compressed_file


def byte_to_bits(byte_data: str):
    bits = ""
    for byte in byte_data:
        ## Fomatting, like 3-> 00000011 to 8 bits (from 1 byte)
        bits += format(byte, "08b")
    return bits


def huff_decompress_file(path: str):
    freq_list, compressed_bytes, padding = read_compressed_file(path)
    root = create_huffman_tree(freq_list)
    bitString = byte_to_bits(compressed_bytes)
    if padding > 0:
        ## removing extra padding added to complete byte while encoding
        bitString = bitString[:-padding]

    decoded_bytes = []
    current_node = root
    for bit in bitString:
        current_node = current_node.left if bit == "0" else current_node.right
        ## Reached EndPoint
        if current_node.left is None and current_node.right is None:
            decoded_bytes.append(current_node.byte)
            current_node = root  ## Reset

    with open("Decompressed.txt", "wb") as f:
        f.write(bytes(decoded_bytes))
