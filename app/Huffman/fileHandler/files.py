def read_file_as_bytes(filepath):
    with open(filepath, "rb") as f:
        data = f.read()
    return data


def get_frequency_list(data):
    frequency_list = [0] * 256
    for byte in data:
        frequency_list[byte] += 1
    return frequency_list


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
