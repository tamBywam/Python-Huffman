class PriorityQueue:
    # Konstruktor klasy PriorityQueue inicjalizuje pustą kolejkę
    def __init__(self):
        self.queue = []

    # Dodaje element do kolejki i utrzymuje właściwości kopca
    def push(self, node):
        self.queue.append(node)
        self._heapify_up(len(self.queue) - 1)

    # Usuwa i zwraca element o najwyższym priorytecie (najniższej częstotliwości)
    def pop(self):
        if len(self.queue) == 1:  # Jeśli w kolejce jest jeden element, zwraca go
            return self.queue.pop()
        root = self.queue[0]
        self.queue[0] = self.queue.pop()  # Przenosi ostatni element na początek
        self._heapify_down(0)  # Przywraca właściwości kopca
        return root

    # Zwraca liczbę elementów w kolejce
    def __len__(self):
        return len(self.queue)

    # Przywraca właściwości kopca po dodaniu elementu
    def _heapify_up(self, index):
        parent = (index - 1) // 2
        if index > 0 and self.queue[index].freq < self.queue[parent].freq:
            self.queue[index], self.queue[parent] = self.queue[parent], self.queue[index]
            self._heapify_up(parent)

    # Przywraca właściwości kopca po usunięciu elementu
    def _heapify_down(self, index):
        smallest = index
        left = 2 * index + 1
        right = 2 * index + 2

        # Znajduje najmniejszego z elementów: bieżącego, lewego i prawego dziecka
        if left < len(self.queue) and self.queue[left].freq < self.queue[smallest].freq:
            smallest = left
        if right < len(self.queue) and self.queue[right].freq < self.queue[smallest].freq:
            smallest = right

        # Jeśli najmniejszy element jest inny niż bieżący, zamienia je i kontynuuje
        if smallest != index:
            self.queue[index], self.queue[smallest] = self.queue[smallest], self.queue[index]
            self._heapify_down(smallest)


class Node:
    # Konstruktor klasy Node inicjalizuje węzeł z symbolem, częstotliwością i dziećmi
    def __init__(self, char=None, freq=0):
        self.char = char
        self.freq = freq
        self.left = None
        self.right = None

    # Definiuje porównywanie węzłów na podstawie częstotliwości
    def __lt__(self, other):
        return self.freq < other.freq


# Oblicza częstotliwości występowania znaków w tekście
def calculate_frequencies(text):
    frequencies = {}
    for char in text:
        frequencies[char] = frequencies.get(char, 0) + 1
    return frequencies


# Tworzy drzewo Huffmana na podstawie częstotliwości znaków
def build_huffman_tree(frequencies):
    pq = PriorityQueue()
    # Tworzy węzły dla każdego znaku i dodaje je do kolejki
    for char, freq in frequencies.items():
        pq.push(Node(char, freq))

    # Łączy węzły w drzewo Huffmana
    while len(pq) > 1:
        left = pq.pop()
        right = pq.pop()
        merged = Node(freq=left.freq + right.freq)  # Tworzy nowy węzeł łączący dwa najmniejsze
        merged.left = left
        merged.right = right
        pq.push(merged)

    return pq.pop()  # Zwraca korzeń drzewa


# Generuje kody Huffmana dla każdego znaku
def generate_codes(node, code="", codes={}):
    if node.char:  # Jeśli węzeł jest liściem, zapisuje kod
        codes[node.char] = code
    else:  # Rekurencyjnie przechodzi do dzieci węzła
        generate_codes(node.left, code + "0", codes)
        generate_codes(node.right, code + "1", codes)
    return codes


# Koduje tekst za pomocą wygenerowanych kodów
def encode_text(text, codes):
    return "".join(codes[char] for char in text)


# Zapisuje zakodowany tekst i kody do pliku
def save_to_file(encoded_text, codes, output_file):
    with open(output_file, "wb") as file:
        # Zapisywanie słownika kodów
        file.write((str(codes) + "\n").encode())
        # Zapisywanie zakodowanego tekstu jako danych binarnych
        byte_array = int(encoded_text, 2).to_bytes((len(encoded_text) + 7) // 8, byteorder='big')
        file.write(byte_array)


# Odczytuje zakodowany tekst i kody z pliku
def load_from_file(encoded_file):
    with open(encoded_file, "rb") as file:
        lines = file.readlines()
        codes = eval(lines[0].decode())  # Przywraca słownik kodów
        binary_data = b"".join(lines[1:])
        bit_string = bin(int.from_bytes(binary_data, byteorder='big'))[2:]  # Konwertuje dane binarne na ciąg bitów
        return codes, bit_string


# Dekoduje tekst na podstawie kodów Huffmana
def decode_text(bit_string, codes):
    reverse_codes = {v: k for k, v in codes.items()}  # Odwraca mapowanie kodów
    current_code = ""
    decoded_text = []

    for bit in bit_string:  # Iteruje po bitach i dopasowuje je do kodów
        current_code += bit
        if current_code in reverse_codes:
            decoded_text.append(reverse_codes[current_code])  # Dodaje znak do wyniku
            current_code = ""

    return "".join(decoded_text)


def main():
    input_file = "input.txt"
    encoded_file = "encoded.bin"
    decoded_file = "decoded.txt"

    # Wczytywanie tekstu z pliku
    with open(input_file, "r", encoding="utf-8") as file:
        text = file.read()

    # Obliczanie częstotliwości znaków
    frequencies = calculate_frequencies(text)

    # Tworzenie drzewa Huffmana
    huffman_tree = build_huffman_tree(frequencies)

    # Generowanie kodów Huffmana
    codes = generate_codes(huffman_tree)

    # Kodowanie tekstu
    encoded_text = encode_text(text, codes)

    # Zapis zakodowanego tekstu i słownika kodów do pliku
    save_to_file(encoded_text, codes, encoded_file)

    # Dekodowanie zakodowanego tekstu
    codes, bit_string = load_from_file(encoded_file)
    decoded_text = decode_text(bit_string, codes)

    # Zapis zdekodowanego tekstu do nowego pliku
    with open(decoded_file, "w", encoding="utf-8") as file:
        file.write(decoded_text)


if __name__ == "__main__":
    main()
