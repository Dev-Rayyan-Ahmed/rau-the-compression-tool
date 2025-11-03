from app.huffman.node import Node
from app.huffman.min_heap.MinHeap import MinHeap

# from app.fileHandler.files import frequency


def create_heap_of_nodes(min_heap, frequency):
    # as there are total 256 ascii value so we can use an array of len 256
    for i, freq in enumerate(frequency):
        if freq > 0:
            node = Node(byte=i, frequency=freq)
            min_heap.addNode(node)

    return min_heap


def create_huffman_tree(freq_list: list):
    min_heap = MinHeap()
    create_heap_of_nodes(min_heap, freq_list)

    while len(min_heap) > 1:  # this is fine
        left = min_heap.dequeue()
        right = min_heap.dequeue()

        new_node = Node(byte=None, frequency=left.frequency + right.frequency)
        new_node.left = left
        new_node.right = right
        min_heap.addNode(new_node)

    tree = min_heap.dequeue()

    return tree


if __name__ == "__main__":

    # frequency_list = [0] * 256
    # frequency_list[98] = 1
    # frequency_list[111] = 2
    # frequency_list[107] = 2
    # frequency_list[101] = 3
    # frequency_list[112] = 1
    # huffman_tree = create_huffman_tree(frequency)
    # print(huffman_tree)
    pass
