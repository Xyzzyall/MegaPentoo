class HashSet:
    __hash_table__ = list()
    __elems__ = list()

    def put(self, elem):
        if not self.is_in(elem):
            self.__hash_table__.append(hash(elem))
            self.__elems__.append(elem)

    def is_in(self, elem):
        h = hash(elem)
        try:
            i = self.__hash_table__.index(h)
            return self.__elems__[i]
        except ValueError:
            return None

    def delete(self, elem):
        if self.is_in(elem):
            self.__hash_table__.remove(hash(elem))
            self.__elems__.remove(elem)

    def __str__(self):
        res = "{"
        for elem in self.__elems__:
            res += str(elem) + ";"
        res += "}"
        return res