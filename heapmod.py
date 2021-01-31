import operator


class Score():
    def __init__(self,value,tweet_id,embedding):
        self.value = value
        self.tweet_id = tweet_id
        self.tweet_embedding = embedding

class Heap(object):
    """"
    Attributes:
        heap: List representation of the heap
        compare(p, c): comparator function, returns true if the relation between p and c is parent-chield
    """
    def __init__(self, heap=None, compare=operator.lt, max_size = 1000):
        self.heap = [] if heap is None else heap
        self.compare = compare
        self.size = 0
        self.max_size = max_size

    def __repr__(self):
        return 'Heap({!r}, {!r})'.format(self.heap, self.compare)

    def _inv_heapify(self, child_index):
        """
        Do heapifying starting from bottom till it reaches the root.
        """
        heap, compare = self.heap, self.compare
        child = child_index
        while child > 0:
            parent = child // 2
            if compare(heap[parent].value, heap[child].value):
                return
            heap[parent], heap[child] = heap[child], heap[parent]
            child = parent

    def _heapify(self, parent_index):
        """
        Do heepifying starting from the root.
        """
        heap, compare = self.heap, self.compare
        length = len(heap)
        if length == 1:
            return
        parent = parent_index
        while 2 * parent < length:
            child = 2 * parent
            if child + 1 < length and compare(heap[child + 1].value, heap[child].value):
                child += 1
            if compare(heap[parent].value, heap[child].value):
                return
            heap[parent], heap[child] = heap[child], heap[parent]
            parent = child

    def insert(self,value,tweet_id,embedding):
        '''
        Insert new score in the heap
        '''
        score = Score(value,tweet_id,embedding)
        if self.size >= self.max_size:
            if score.value > self.min():
                self._del_min()
                self._add(score)
            print('Items score is lower than min')
        else:
            self._add(score)

    def _del_min(self):
        ''' Deletes the min number in the heap, the root'''
        heap = self.heap
        last_element = heap.pop()
        if not heap:
            return last_element
        item = heap[0]
        heap[0] = last_element
        self._heapify(0)
        self.size -= 1
        return item

    def min(self):
        if not self.heap:
            return None
        return self.heap[0].value

    def _add(self, element):
        ''' Adds new elemene to the heap'''
        self.heap.append(element)
        self._inv_heapify(len(self.heap) - 1)
        self.size += 1

    def check_heap(self):
        for i in self.heap:
            print(i.value)
