class MinHeap:
    def __init__(self):
        self.heap = []

    def left(self, root):
        left_child_idx = 2 * root + 1  # as zero based index
        return left_child_idx

    def right(self, root):
        right_child_idx = 2 * root + 2
        return right_child_idx

    def parent(self, parent):
        return (parent - 1) // 2

    def heapify(self, root):
        """locally min heapify the root"""
        n = len(self.heap)
        left = self.left(root)
        right = self.right(root)
        smallest = root

        if left < n and self.heap[left] < self.heap[smallest]:
            smallest = left

        if right < n and self.heap[right] < self.heap[smallest]:
            smallest = right

        if root != smallest:
            # swap
            self.heap[root], self.heap[smallest] = self.heap[smallest], self.heap[root]

            # now value at smallest index is of root so heapify that node again
            self.heapify(smallest)  # this is the recursive call

    def make_heap(self):
        size = len(self.heap)
        # cause complete binary tree so at least half of the nodes are leaf node
        for i in reversed(range(size // 2)):
            self.heapify(i)

    def dequeue(self):
        if len(self.heap) == 0:
            return None

        # ! this condition was missing
        if len(self.heap) == 1:
            return self.heap.pop()

        root = self.heap[0]
        # just like in heap sort replace the last element with fist but remove the the last element now
        self.heap[0] = self.heap.pop()
        # now heapify the new top or root node as we have guarantee that
        # it was previously heap so do not need to heapify all
        self.heapify(0)
        return root

    def heapify_up(self, index):
        # this is iterative
        while index > 0:
            parent = self.parent(index)
            if self.heap[index] < self.heap[parent]:
                # swap
                self.heap[index], self.heap[parent] = (
                    self.heap[parent],
                    self.heap[index],
                )
                index = parent
            else:
                break

    def addNode(self, node):
        self.heap.append(node)
        self.heapify_up(len(self.heap) - 1)

    def __len__(self):
        return len(self.heap)
