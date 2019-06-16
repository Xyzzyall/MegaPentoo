


class Elem:
    val = None
    next = None
    prev = None

    def __init__(self, val, next, prev):
        self.val = val
        self.next = next
        self.prev = prev

    def index(self, ind):
        i = 0
        buf = self
        while i < ind:
            buf = buf.next
            i += 1
            if not buf:
                return None

        return buf

    def get_last(self):
        buf = self
        i = 0
        while buf.next:
            buf = buf.next
            i += 1
        return buf, i

    def append(self, val):
        last = self.get_last()[0]
        L = Elem(val, None, last)
        last.next = L

    def insert(self, i, val):
        i -= 1
        if i == -1:
            L = Elem(val, self, None)
            self.prev = L
        else:
            e0 = self.index(i)
            e2 = e0.next
            L = Elem(val, e2, e0)
            e0.next = L
            if e2:
                e2.prev = L

    def delete_index(self, i):
        e1 = self.index(i)
        e0 = e1.prev
        e2 = e1.next
        e0.next = e2
        e2.prev = e0

    def find_index_of(self, val):
        buf = self
        i = 0
        while not val == buf.val:
            i += 1
            buf = buf.next
            if not buf:
                return None
        else:
            return i

    def delete_val(self, val):
        self.delete_index(self.find_index_of(val))

    def __str__(self):
        res = "[" + str(self.val)
        buf = self.next
        while buf:
            res += ", " + str(buf.val)
            buf = buf.next
        return res + "]"

