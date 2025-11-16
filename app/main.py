import sys
from .Huffman.fileHandler.files import (
    get_frequency_list,
    generate_codes,
    read_file_as_bytes,
    write_compressed_file,
    encode_frequency_list,
    RLE_write_compressed_file
)
from .Huffman.huffman_main.hufman import create_huffman_tree
from .Huffman.decompressing.huffman_decompressor import huff_decompress_file


def run_from_electron():
    if len(sys.argv) < 3:
        raise Exception("too less arguments")
    file = sys.argv[2]
    if sys.argv[1] == "-c":
        data = read_file_as_bytes(file)
        frequency = get_frequency_list(data=data)

        print(frequency)
        print("\n\n\n")
        print(encode_frequency_list(frequency))

        root = create_huffman_tree(frequency)
        codes = generate_codes(root)
        encoded_bitstring = "".join(codes[char] for char in data)
        RLE_write_compressed_file("output.rau", encoded_bitstring, frequency)
        sys.stdout.flush()  # IMPORTANT: Makes sure the output is sent right away
    elif sys.argv[1] == "-d":
        huff_decompress_file(file)
        print("Decompressing Done")


if __name__ == "__main__":
    run_from_electron()
