from .fileHandler.files import (
    get_frequency_list,
    generate_codes,
    read_file_as_bytes,
    write_compressed_file,
)
from .huffman.hufman import create_huffman_tree
from .decompressing.huffman_decompressor import huff_decompress_file

if __name__ == "__main__":
    print("RAU: Compressor Tool")
    data = read_file_as_bytes("input.txt")
    # print (data)
    frequency = get_frequency_list(data=data)
    print(sum(frequency))
    root = create_huffman_tree(frequency)
    print(root.frequency)
    # print(generate_codes(root))
    codes = generate_codes(root)

    encoded_bitstring = "".join(codes[char] for char in data)
    # print(encoded_bitstring)

    write_compressed_file("output.rau", encoded_bitstring, frequency)

    huff_decompress_file("output.rau")
    print("Decompressing Done")
