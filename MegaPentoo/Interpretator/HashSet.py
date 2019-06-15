class HashSet:
    __hash_table__ = list()
    __elems__ = list()

    def put(self, elem):
        self.__hash_table__.append(h)
        self.__elems__.append(elem)

    def is_in(self, elem):
        h = hash(elem)
        try:
            i = self.__hash_table__.index(h)
            return self.__elems__[i]
        except ValueError:
            return None
