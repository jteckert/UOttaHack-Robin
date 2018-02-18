import numpy


class ArrayDeque:

    def __init__(self):
        self._buffer = numpy.array([None])
        self._in_buf = 0
        self._head = 0
        self._tail = 0

    def is_empty(self):
        return self._in_buf == 0

    def _set_length(self, length):
        new_buf = []
        for item in self:
            new_buf.append(item)
        new_buf.extend([None] * (length - len(self._buffer)))

        self._head = 0
        self._tail = len(self._buffer)
        self._buffer = numpy.array(new_buf)

    def _set_item(self, item, ind):
        self._buffer[(self._head + ind) % len(self._buffer)] = item

    def add(self, item):
        if self._in_buf < len(self._buffer):
            self._buffer[self._tail] = item
            self._tail = (self._tail + 1) % len(self._buffer)
            self._in_buf = self._in_buf + 1
        else:
            self._set_length(len(self._buffer) * 2)
            self.add(item)

    def remove(self):
        if self._in_buf > 0:
            ret = self._buffer[self._head]
            self._in_buf = self._in_buf - 1

            if 0 < self._in_buf < len(self._buffer) / 4:
                self._set_length(len(self._buffer) // 2)
            else:
                self._head = (self._head + 1) % len(self._buffer)
            return ret

    def force_remove(self, index):
        mid = self._in_buf // 2
        if index >= mid:
            for i in range(index + 1, self._in_buf):
                self._set_item(self[i], i - 1)
            self._tail = (self._tail + len(self._buffer) - 1) % len(self._buffer)
            self._in_buf -= 1
        else:
            for i in range(index):
                self._set_item(self[i], i + 1)
            self.remove()

    def size(self):
        return self._in_buf

    def __getitem__(self, item):
        return self._buffer[(self._head + item) % len(self._buffer)]

    def __iter__(self):
        return _ADequeIterator(self)


class _ADequeIterator:
    def __init__(self, deque):
        self._deque = deque
        self._index = 0

    def __next__(self):
        if self._index >= self._deque.size():
            raise StopIteration
        else:
            ret = self._deque[self._index]
            self._index = self._index + 1
            return ret
