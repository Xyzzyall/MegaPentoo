from MegaPentoo.Interpretator.LinkedList import Elem as LinkedList


class HashSet:
    __hash_table__ = LinkedList(None, None, None)
    __elems__ = LinkedList(None, None, None)

    def put(self, elem):
        if not self.is_in(elem):
            self.__hash_table__.append(hash(elem))
            self.__elems__.append(elem)

    def is_in(self, elem):
        h = hash(elem)
        try:
            i = self.__hash_table__.find_index_of(h)
            if not i:
                raise ValueError
            return self.__elems__.index(i)
        except ValueError:
            return None

    def get_index(self, elem):
        h = hash(elem)
        try:
            i = self.__hash_table__.find_index_of(h)
            if not i:
                raise ValueError
            return i
        except ValueError:
            return None

    def delete(self, elem):
        if self.is_in(elem):
            self.__hash_table__.delete_val(hash(elem))
            self.__elems__.delete_val(elem)

    def __str__(self):
        #res = "{"
        #for elem in [val for elem.val in self.__elems__]:
        #    res += str(elem) + ";"
        #res += "}"

        return '{' + str(self.__elems__.index(1))[1:-1] + '}'
