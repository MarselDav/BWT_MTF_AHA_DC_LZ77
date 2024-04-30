class DeltaCoding:
    def __init__(self):
        self.block_size = 4096

    def encode(self, input_path, output_path):
        with open(input_path, "rb") as file_reader:
            with open(output_path, "wb") as file_writer:
                prev_byte = 0
                while True:
                    bytes_block = file_reader.read(self.block_size)

                    if not bytes_block:
                        break

                    encoded_block = bytearray()
                    for byte in bytes_block:
                        diff = byte - prev_byte
                        diff = diff % 256

                        encoded_block.append(diff)
                        prev_byte = byte
                    file_writer.write(encoded_block)

    def decode(self, input_path, output_path):
        with open(input_path, "rb") as file_reader:
            with open(output_path, "wb") as file_writer:
                prev_byte = 0
                while True:
                    bytes_block = file_reader.read(self.block_size)

                    if not bytes_block:
                        break

                    encoded_block = bytearray()
                    for diff in bytes_block:
                        byte = (prev_byte + diff) % 256
                        file_writer.write(bytes([byte]))

                        prev_byte = byte
                    file_writer.write(encoded_block)


if __name__ == "__main__":
    delta_coding = DeltaCoding()

    # test_data_path = "../../files/enwik7.txt"
    test_data_path = "../../files/compressed_by_BWT_MTF_AHA.txt"

    compressed_path = "DC/compressed_text.txt"
    decompressed_path = "DC/decompressed_text.txt"

    delta_coding.encode(test_data_path, compressed_path)
    delta_coding.decode(compressed_path, decompressed_path)

    with open(test_data_path, "rb") as file_read:
        original_data = file_read.read()

    with open(decompressed_path, "rb") as file_read:
        decode_data = file_read.read()

    print(original_data == decode_data)
