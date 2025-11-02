# from app.huffman.hufman import create_huffman_tree
def read_file_as_bytes(filepath):
    with open(filepath, "rb") as f:   # 'rb' = read as binary
        data = f.read()
    return data

def get_frequency_list(data):
    frequency_list = [0] * 256
    for byte in data:
        frequency_list[byte] += 1
    return frequency_list

# def generate_codes(node, current_code="", codes = None):
#     if codes is None:
#         codes = {}

#     if node is None:
#         return codes

#     # If leaf node
#     if node.left is None and node.right is None:
#         codes[node.byte] = current_code
#         return codes

#     # Recursive traversal
#     generate_codes(node.left, current_code + "0", codes)
#     generate_codes(node.right, current_code + "1", codes)
#     return codes

def generate_codes(node):
    codes = {}
    def traverse(node_, code=""):
        if node_ is None:
            return
        if node_.byte is not None:
            codes[node_.byte] = code
            return
        traverse(node_.left, code + "0")
        traverse(node_.right, code + "1")
    traverse(node)
    return codes

def bits_to_bytes(bitstring: str):
    if len(bitstring) == 0:
        return b'', 0
    padding = (8 - (len(bitstring) % 8)) % 8

    if padding > 0:
        bitstring = bitstring + ('0' * padding)

   
    output = bytearray()

    i = 0
    while i < len(bitstring):
        group = bitstring[i:i+8]   # take first chunk of 8 bits
        value = int(group, 2)      # convert binary to decimal as base is 2
        output.append(value)       # store as byte
        i += 8                     # next 8 bits

    # print("output is", output)
    # Return bytes object and padding 
    return bytes(output), padding



def write_compressed_file(output_path, encoded_bitstring, frequency_list):
    compressed_bytes, padding = bits_to_bytes(encoded_bitstring)
    
    with open(output_path, 'wb') as f:
        # magic header will me unique to "our" encoding
        f.write("RAU1")
                
        for freq in frequency_list:
            # if freq > 0:  we may use this logic but this will make some difficulties in decompressing
                f.write(freq.to_bytes(4, byteorder='big')) # writing frequency in file
        
        # Write padding
        f.write(bytes([padding]))
        
        # Write compressed data
        f.write(compressed_bytes)
    
    print(f"File saved: {output_path}")

def read_compressed_file(input_path):
    with open(input_path, 'rb') as f:

        magic = f.read(4)
        if magic != b'RAU1':
            raise ValueError("Invalid file format — not a RAU compressed file!")

        frequency_list = [int.from_bytes(f.read(4), 'big') for _ in range(256)]

        padding = ord(f.read(1))

        compressed_bytes = f.read()

    return frequency_list, compressed_bytes, padding


# def decompress_file(file_name):
#     with open (file_name, 'rb') as f:
#         frequency_list = [int.from_bytes(f.read(4), 'big') for _ in range(256)]
#         padding = ord(f.read(1))
#         compressed_bytes = f.read()

