from app.huffman.hufman import create_huffman_tree
from app.fileHandler.files import read_compressed_file

def byte_to_bits(byte_data: str):
    bits = ""
    for byte in byte_data:
        bits += format(byte, "08b") ## Fomatting, like 3-> 00000011 to 8 bits (from 1 byte)
    return bits
    

def huff_decompress_file(path: str):
    freq_list, compressed_bytes, padding = read_compressed_file(path)
    root = create_huffman_tree(freq_list)
    bitString = byte_to_bits(compressed_bytes)
    if padding >0:
        bitString = bitString[:-padding] ## removing extra padding added to complete byte while encoding

    decoded_bytes = []
    current_node = root
    for bit in bitString:
        current_node = current_node.left if bit == "0" else current_node.right
        if current_node.left is None and current_node.right is None: ## Reached EndPoint
            decoded_bytes.append(current_node.byte) 
            current_node = root ## Reset
    
    with open("Decompressed.txt","wb") as f:
        f.write(bytes(decoded_bytes))
    
    

        