import sys
import os
from .huffman.fileHandler.files import compress_file
from .huffman.decompressing.huffman_decompressor import huff_decompress_file


def run_from_electron():
    if len(sys.argv) < 2:
        raise Exception("too less arguments")
    if len(sys.argv) > 3:
        output_path = sys.argv[3]

    else:
        output_path = os.path.dirname(os.path.abspath(sys.argv[2]))

    file = sys.argv[2]
    if sys.argv[1] == "-c":
        compress_file(file, output_path)
        sys.stdout.flush()  # IMPORTANT: Makes sure the output is sent right away
    elif sys.argv[1] == "-d":
        huff_decompress_file(file, output_path)
        print("Decompressing Done")


if __name__ == "__main__":
    run_from_electron()
