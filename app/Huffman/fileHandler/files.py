def read_file_as_bytes(filepath):
    with open(filepath, "rb") as f:
        data = f.read()
    return data


def get_frequency_list(data):
    frequency_list = [0] * 256
    for byte in data:
        frequency_list[byte] += 1
    return frequency_list

def encode_frequency_list(frequency_list):
    encoded_bytes = bytearray()
    i = 0
    
    while i < 256:
        freq = frequency_list[i]
        
        if freq > 0:
            # for non-zero freq
            encoded_bytes.extend(freq.to_bytes(4, byteorder="big"))
            i += 1
            
        else:
            # if frequency is zero then we use RLE to encode running zeros
            running_length = 0
            j = i

            while j < 256 and frequency_list[j] == 0 and running_length < 255:
                running_length += 1
                j += 1
            
            if running_length >= 1:
                # adding control byte and Running length
                encoded_bytes.append(0xFF)
                encoded_bytes.append(running_length)
                
                i += running_length

    return bytes(encoded_bytes)

def RLE_write_compressed_file(output_path, encoded_bitstring, frequency_list):
    
    compressed_bytes, padding = bits_to_bytes(encoded_bitstring)
    encoded_freq_bytes = encode_frequency_list(frequency_list) 

    with open(output_path, "wb") as f:
        f.write(b"RAU1") 
        
        f.write(len(encoded_freq_bytes).to_bytes(4, byteorder="big")) 
        
        f.write(encoded_freq_bytes)

        f.write(bytes([padding]))

        f.write(compressed_bytes)

    print(f"File saved: {output_path}")

def decode_frequency_list(encoded_freq_list):
    freq_list = [0]*256
    
    # i is pointer for Freq_list & encoded_otr runs on Encoded_freq_list
    i = 0
    encoded_ptr = 0

    while i<256 and encoded_ptr < len(encoded_freq_list):
        
        if encoded_freq_list[encoded_ptr] == 0xFF:
            # if true, we hav found RLE Encoding
            running_length = encoded_freq_list[encoded_ptr+1]

            # freq_list is already filled with 0s, so we just skip them
            i += running_length
            encoded_ptr += 2
        else:
            freq_byte = encoded_freq_list[encoded_ptr : encoded_ptr+4]
            freq = int.from_bytes(freq_byte, byteorder="big")
            freq_list[i] = freq

            i +=1
            encoded_ptr +=4
    
    return freq_list

def RLE_read_compressed_file(input_path):
    
    with open(input_path, "rb") as f:
        magic = f.read(4)
        if magic != b'RAU1':
            raise ValueError ("Invalid File Format : Not a RAU Compressed file")
        
        encoded_freq_list_len = int.from_bytes(f.read(4), byteorder= "big")
        encoded_freq_list = f.read(encoded_freq_list_len)
        frequency_list = decode_frequency_list(encoded_freq_list)
        
        padding = f.read(1)[0]
        compressed_bytes = f.read()
    
    return frequency_list, compressed_bytes, padding



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
        return b"", 0
    padding = (8 - (len(bitstring) % 8)) % 8

    if padding > 0:
        bitstring = bitstring + ("0" * padding)

    output = bytearray()

    i = 0
    while i < len(bitstring):
        # take first chunk of 8 bits
        group = bitstring[i : i + 8]
        # convert binary to decimal as base is 2
        value = int(group, 2)
        # store as byte
        output.append(value)
        # next 8 bits
        i += 8
    return bytes(output), padding


def write_compressed_file(output_path, encoded_bitstring, frequency_list):
    compressed_bytes, padding = bits_to_bytes(encoded_bitstring)

    with open(output_path, "wb") as f:
        # magic header will me unique to "our" encoding
        f.write(b"RAU1")

        for freq in frequency_list:
            # if freq > 0:  we may use this logic but this will make some difficulties in decompressing
            # writing frequency in file
            f.write(freq.to_bytes(4, byteorder="big"))

        # Write padding
        f.write(bytes([padding]))

        # Write compressed data
        f.write(compressed_bytes)

    print(f"File saved: {output_path}")


def read_compressed_file(input_path):
    with open(input_path, "rb") as f:

        magic = f.read(4)
        if magic != b"RAU1":
            raise ValueError("Invalid file format — not a RAU compressed file!")

        frequency_list = [int.from_bytes(f.read(4), "big") for _ in range(256)]

        padding = ord(f.read(1))

        compressed_bytes = f.read()

    return frequency_list, compressed_bytes, padding
