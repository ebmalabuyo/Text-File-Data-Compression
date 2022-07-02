from __future__ import annotations
import string

from typing import Optional, TextIO

from ordered_list import pop, insert, get, OrderedList, size


class HuffmanNode:
    """Represents a node in a Huffman tree.

    Attributes:
        char: The character as an integer ASCII value
        frequency: The frequency of the character in the file
        left: The left Huffman sub-tree
        right: The right Huffman sub-tree
    """
    def __init__(
            self,
            char: int,
            frequency: int,
            left: Optional[HuffmanNode] = None,
            right: Optional[HuffmanNode] = None):
        self.char = char
        self.frequency = frequency
        self.left = left
        self.right = right

    def __eq__(self, other) -> bool:
        """Returns True if and only if self and other are equal."""
        return (other is not None and
                self.frequency == other.frequency and
                self.char == other.char and
                self.left == other.left and
                self.right == other.right)

    def __lt__(self, other) -> bool:
        """Returns True if and only if self < other."""
        return (self.frequency < other.frequency or
                self.frequency == other.frequency and
                self.char < other.char)


def count_frequencies(file: TextIO) -> list[int]:
    """Reads the given file and counts the frequency of each character.

    The resulting Python list will be of length 256, where the indices
    are the ASCII values of the characters, and the value at a given
    index is the frequency with which that character occured.
        """
    lst = [0] * 256

    for i in file:
        for val in i:
            lst[ord(val)] += 1
    return lst


def build_huffman_tree(frequencies: list[int]) -> Optional[HuffmanNode]:
    """Creates a Huffman tree of the characters with non-zero frequency.

    Returns the root of the tree.
    """
    lst = OrderedList()

    # check for empty list
    if frequencies.count(0) == 256:
        return None

    # use ordered list for each value
    for i in range(len(frequencies)):
        if frequencies[i] != 0:
            insert(lst, HuffmanNode(i, frequencies[i]))

    # popping the first two
    # must check for size first or else won't work
    # while contains more than one tree
    while size(lst) != 1:
        # removes first
        first = pop(lst, 0)
        # removes second
        second = pop(lst, 0)

        # lesser goes to the left
        # check by comparing the two
        # needed __eq__ above
        if second.frequency == first.frequency:
            if first.char < second.char:
                val = HuffmanNode(
                            first.char,
                            first.frequency + second.frequency,
                            first,
                            second)
        # if frequency is greater is second
        elif second.frequency > first.frequency:
            if second.char > first.char:
                val = HuffmanNode(
                            first.char,
                            first.frequency + second.frequency,
                            first,
                            second)
        # if not then second becomes char in this case
            else:
                val = HuffmanNode(
                        second.char,
                        first.frequency + second.frequency,
                        first,
                        second)
        # add to the ordered list
        insert(lst, val)
        # should be first item again
    return get(lst, 0)


def helper_create_codes(tree: Optional[HuffmanNode], lst, val):
    if tree is None:
        return
    # checks the left and the right nodes
    if tree.right is None and tree.left is None:
        if len(val) > 0:
            lst[tree.char] = val
        else:
            lst[tree.char] = ''
    # recursively call for both sides of tree
    helper_create_codes(tree.right, lst, val + '1')
    # concatenate '0' and '1'
    helper_create_codes(tree.left, lst, val + '0')
    # test helper to make sure it doesn't crash


def create_codes(tree: Optional[HuffmanNode]) -> list[str]:
    """Traverses the tree creating the Huffman code for each character.

    The resulting Python list will be of length 256, where the indices
    are the ASCII values of the characters, and the value at a given
    index is the Huffman code for that character.
    """
    # empty codes
    lst = [''] * 256
    # check with helper functio above
    helper_create_codes(tree, lst, '')
    # returns the main lst
    return lst


def create_header(frequencies: list[int]) -> str:
    """Returns the header for the compressed Huffman data.

    For example, given the file "aaabbbbcc", this would return:
    "97 3 98 4 99 2"
    """
    # initiate and add to lst
    lst = []
    for i in range(len(frequencies)):
        if frequencies[i] != 0:
            # need to make the value a string
            # append the index alsi
            lst.append(str(i))
            lst.append(str(frequencies[i]))
    # output is string
    str_val = ' '.join(lst)
    return str_val


def huffman_encode(in_file: TextIO, out_file: TextIO) -> None:
    """Encodes the data in the input file, writing the result to the
    output file.
    """
    f = count_frequencies(in_file)

    huff = build_huffman_tree(f)
    code = create_codes(huff)
    header = create_header(f) + '\n'

    in_file.seek(0)

    out_file.write(header)

    for line in in_file:
        for val in line:
            out_file.write(code[ord(val)])

    # # utilize previous to build output file
    # huff = build_huffman_tree(count_frequencies(in_file))
    # created_codes = create_codes(huff)
    # # NEED to include new line with ending
    # created_head = create_header(count_frequencies(in_file)) + '\n'
    # in_file.seek(0)

    # out_file.write(created_head)
    # # write into output
    # for i in in_file:
    #     for val in i:
    #         out_file.write(created_codes[ord(val)])


def parse_header(text: string) -> list:
    lst = [0] * 256
    s = text.split()
    count = 1
    while count < len(s):
        lst[int(s[count - 1])] = int(s[count])
        count += 2

    return lst


def huffman_decode(in_file: TextIO, out_file: TextIO) -> None:
    header = in_file.readline()
    code = ''
    check = header.split()
    if len(check) == 2:
        val = chr(int(check[0]))
        code += val * int(check[1])
        out_file.write(code)
        return
    lst = parse_header(header)
    hufftree = build_huffman_tree(lst)
    curr = hufftree
    for val in in_file.read():
        if val == '0':
            curr = curr.left
        elif val == '1':
            curr = curr.right
        if curr.left is None and curr.right is None:
            code += chr(curr.char)
            curr = hufftree
    out_file.write(code)
