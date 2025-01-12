class PriorityQueue:
    def __init__(self):
        self.queue = []

    def push(self, node):
        self.queue.append(node)
        self._heapify_up(len(self.queue) - 1)

    def pop(self):
        if len(self.queue) == 1: 
            return self.queue.pop()
        root = self.queue[0]
        self.queue[0] = self.queue.pop() 
        self._heapify_down(0) 
        return root

    def __len__(self):
        return len(self.queue)

    def _heapify_up(self, index):
        parent = (index - 1) // 2
        if index > 0 and self.queue[index].freq < self.queue[parent].freq:
            self.queue[index], self.queue[parent] = self.queue[parent], self.queue[index]
            self._heapify_up(parent)

    def _heapify_down(self, index):
        smallest = index
        left = 2 * index + 1
        right = 2 * index + 2

        if left < len(self.queue) and self.queue[left].freq < self.queue[smallest].freq:
            smallest = left
        if right < len(self.queue) and self.queue[right].freq < self.queue[smallest].freq:
            smallest = right

        if smallest != index:
            self.queue[index], self.queue[smallest] = self.queue[smallest], self.queue[index]
            self._heapify_down(smallest)


class Node:
    def __init__(self, char=None, freq=0):
        self.char = char
        self.freq = freq
        self.left = None
        self.right = None

    def __lt__(self, other):
        return self.freq < other.freq


def calculate_frequencies(text):
    frequencies = {}
    for char in text:
        frequencies[char] = frequencies.get(char, 0) + 1
    return frequencies


def build_huffman_tree(frequencies):
    pq = PriorityQueue()
    for char, freq in frequencies.items():
        pq.push(Node(char, freq))

    while len(pq) > 1:
        left = pq.pop()
        right = pq.pop()
        merged = Node(freq=left.freq + right.freq)
        merged.left = left
        merged.right = right
        pq.push(merged)

    return pq.pop()


def generate_codes(node, code="", codes={}):
    if node.char:
        codes[node.char] = code
    else:
        generate_codes(node.left, code + "0", codes)
        generate_codes(node.right, code + "1", codes)
    return codes


def encode_text(text, codes):
    return "".join(codes[char] for char in text)


def save_to_file(encoded_text, codes, output_file):
    with open(output_file, "wb") as file:
        file.write((str(codes) + "\n").encode())
        byte_array = int(encoded_text, 2).to_bytes((len(encoded_text) + 7) // 8, byteorder='big')
        file.write(byte_array)


def load_from_file(encoded_file):
    with open(encoded_file, "rb") as file:
        lines = file.readlines()
        codes = eval(lines[0].decode())
        binary_data = b"".join(lines[1:])
        bit_string = bin(int.from_bytes(binary_data, byteorder='big'))[2:]
        return codes, bit_string


def decode_text(bit_string, codes):
    reverse_codes = {v: k for k, v in codes.items()}
    current_code = ""
    decoded_text = []

    for bit in bit_string:
        current_code += bit
        if current_code in reverse_codes:
            decoded_text.append(reverse_codes[current_code])
            current_code = ""

    return "".join(decoded_text)


def main():
    input_file = "input.txt"
    encoded_file = "encoded.bin"
    decoded_file = "decoded.txt"

    with open(input_file, "r", encoding="utf-8") as file:
        text = file.read()

    frequencies = calculate_frequencies(text)

    huffman_tree = build_huffman_tree(frequencies)

    codes = generate_codes(huffman_tree)

    encoded_text = encode_text(text, codes)

    save_to_file(encoded_text, codes, encoded_file)

    codes, bit_string = load_from_file(encoded_file)
    decoded_text = decode_text(bit_string, codes)

    with open(decoded_file, "w", encoding="utf-8") as file:
        file.write(decoded_text)


if __name__ == "__main__":
    main()
