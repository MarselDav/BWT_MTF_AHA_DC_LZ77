from source.AdaptiveHaffmanCoding.AdaptiveHaffmanCompress import AHA_COMPRESS
from source.AdaptiveHaffmanCoding.AdaptiveHaffmanDecompress import AHA_DECOMPRESS
from source.BurrowsWheeleTransform.BWT import BWT
from source.MoveToFront.MTF import MTF
from source.DeltaCoding.DeltaCoding import DeltaCoding
from source.LempelZiv.LZ77 import LZ77


class BWT_MTF_AHA_DC_LZ77:  # BWT + MTF + AHA + DC + LZ77
    def __init__(self):
        self.mtf = MTF()
        self.bwt = BWT()
        self.adaptive_haffman_compress = AHA_COMPRESS()
        self.adaptive_haffman_decompress = AHA_DECOMPRESS()
        self.delta = DeltaCoding()
        self.lz77 = LZ77()
        self.intermediate1_path = "intermediate_file1.txt"
        self.intermediate2_path = "intermediate_file2.txt"

    def encode(self, input_path: str, output_path: str):
        self.bwt.encode(input_path, self.intermediate1_path)
        self.mtf.encode(self.intermediate1_path, self.intermediate2_path)
        self.adaptive_haffman_compress.encode(self.intermediate2_path, self.intermediate1_path)
        self.delta.encode(self.intermediate1_path, self.intermediate2_path)
        self.lz77.encode(self.intermediate2_path, output_path)

    def decode(self, input_path: str, output_path: str):
        self.lz77.decode(input_path, self.intermediate1_path)
        self.delta.decode(self.intermediate1_path, self.intermediate2_path)
        self.adaptive_haffman_decompress.decode(self.intermediate2_path, self.intermediate1_path)
        self.mtf.decode(self.intermediate1_path, self.intermediate2_path)
        self.bwt.decode(self.intermediate2_path, output_path)


def test_compress():
    test_data_path = "../../testing_files/small_test_file.txt"
    # test_data_path = "../../testing_files/enwik8.txt"
    compressed_path = "../../testing_files/compressed_text.txt"
    decompressed_path = "../../testing_files/decompressed_text.txt"

    bwt_mtf_aha_dc_lz77 = BWT_MTF_AHA_DC_LZ77()
    bwt_mtf_aha_dc_lz77.encode(test_data_path, compressed_path)
    bwt_mtf_aha_dc_lz77.decode(compressed_path, decompressed_path)

    with open(test_data_path, "rb") as file_reader:
        orig_data = file_reader.read()

    with open(compressed_path, "rb") as file_reader:
        encode_data = file_reader.read()

    with open(decompressed_path, "rb") as file_reader:
        decode_data = file_reader.read()

    print("Правильность декодирования: ", orig_data == decode_data)
    print("BWT_MTF_AHA_DC_LZ77: ", len(encode_data))


if __name__ == "__main__":
    test_compress()
