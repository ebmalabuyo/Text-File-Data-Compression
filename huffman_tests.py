import io
import unittest

# NOTE: Do not import anything else from huffman.  If you do, your tests
# will crash when I test them.  You shouldn't need to test your helper
# functions directly, just via testing the required functions.
from huffman import (
    HuffmanNode, count_frequencies, build_huffman_tree, create_codes,
    create_header, huffman_encode)


class TestList(unittest.TestCase):
    def test_count_frequencies_01(self) -> None:
        # Create fake file to use for testing
        in_file = io.StringIO('ddddddddddddddddccccccccbbbbaaff')
        frequencies = count_frequencies(in_file)
        in_file.close()

        expected = [0] * 256
        expected[97:103] = [2, 4, 8, 16, 0, 2]

        self.assertEqual(frequencies, expected)

    # NOTE: This is the same test as count_frequencies_01 but with a
    # real file
    def test_count_frequencies_02(self) -> None:
        with open('text_files/file2.txt') as in_file:
            frequencies = count_frequencies(in_file)

        expected = [0] * 256
        expected[97:103] = [2, 4, 8, 16, 0, 2]

        self.assertEqual(frequencies, expected)

    def test_node_lt_01(self) -> None:
        node1 = HuffmanNode(97, 10)
        node2 = HuffmanNode(65, 20)

        self.assertLess(node1, node2)
        self.assertGreater(node2, node1)

    def test_build_huffman_tree_01(self) -> None:
        frequencies = [0] * 256
        frequencies[97] = 5
        frequencies[98] = 10

        huffman_tree = build_huffman_tree(frequencies)

        # NOTE: This also requires a working __eq__ for your HuffmanNode
        self.assertEqual(
            huffman_tree,
            HuffmanNode(97, 15, HuffmanNode(97, 5), HuffmanNode(98, 10))
        )

    def test_create_codes_01(self) -> None:
        huffman_tree = HuffmanNode(
            97, 15,
            HuffmanNode(97, 5),
            HuffmanNode(98, 10)
        )

        codes = create_codes(huffman_tree)
        self.assertEqual(codes[ord('a')], '0')
        self.assertEqual(codes[ord('b')], '1')

    def test_create_header_01(self) -> None:
        frequencies = [0] * 256
        frequencies[97] = 5
        frequencies[98] = 10

        self.assertEqual(create_header(frequencies), '97 5 98 10')

    def test_huffman_encode_01(self) -> None:
        # Create fake files to use for testing
        in_file = io.StringIO('abcd abc ab a')
        out_file = io.StringIO()

        huffman_encode(in_file, out_file)
        result = out_file.getvalue()

        in_file.close()
        out_file.close()

        correct_out_text = (
            '32 3 97 4 98 3 99 2 100 1\n'
            '11011011000011011010011010011'
        )

        self.assertEqual(result, correct_out_text)

    # NOTE: This is the same test as encode_01, but with real files
    def test_huffman_encode_02(self) -> None:
        with open('text_files/file1.txt') as in_file, \
             open('text_files/file1_out.txt', 'w') as out_file:
            huffman_encode(in_file, out_file)

        with open('text_files/file1_out.txt') as student_out, \
             open('text_files/file1_encoded.txt') as correct_out:
            self.assertEqual(student_out.read(), correct_out.read())

    def test_huffman_empty(self):
        lst = [0] * 256
        test = build_huffman_tree(lst)
        self.assertIsNone(test)

    def test_create_code_01(self):
        test = HuffmanNode(98, 5)
        test_codes = create_codes(test)
        self.assertEqual(test_codes[ord('b')], '')

    def test_encode_edge_01(self):
        in_file = io.StringIO('bbbbbbb')
        out_file = io.StringIO()
        huffman_encode(in_file, out_file)
        com = out_file.getvalue()
        in_file.close()
        out_file.close()
        test = ('98 7\n')
        self.assertEqual(com, test)

    def test_huffman_encode_03(self) -> None:
        with open('text_files/file2.txt') as in_file, \
             open('text_files/file2_out.txt', 'w') as out_file:
            huffman_encode(in_file, out_file)

        with open('text_files/file2_out.txt') as student_out, \
             open('text_files/file2_encoded.txt') as correct_out:
            self.assertEqual(student_out.read(), correct_out.read())

    def test_build_huffman_02(self) -> None:
        frequencies = [0] * 256
        frequencies[98] = 1
        huffman_tree = build_huffman_tree(frequencies)
        self.assertEqual(huffman_tree, HuffmanNode(98, 1))

    def test_build_huffman_4(self) -> None:
        lst = [0] * 256
        lst[32] = 3
        lst[97] = 4
        lst[98] = 3
        lst[99] = 2
        lst[100] = 1
        huff = build_huffman_tree(lst)
        self.assertEqual(
            huff,
            HuffmanNode(32, 13, HuffmanNode(32, 6, HuffmanNode(
                32, 3), HuffmanNode(98, 3)),
                    HuffmanNode(97, 7, HuffmanNode(99, 3, HuffmanNode(
                        100, 1), HuffmanNode(99, 2)), HuffmanNode(97, 4))))


if __name__ == '__main__':
    unittest.main()
