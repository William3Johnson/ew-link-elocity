
from copy import deepcopy


class Model:
    """ MVC Concrete Model """

    def __init__(self, reg_id=None):
        """
        :param reg_id: Registry ID
        :return:
        """
        self.reg_id = reg_id

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.reg_id == other.reg_id

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        if self.reg_id is None:
            raise AssertionError('O objeto está desincronizado com o banco de dados.')
        return hash(''.join(dir(self))) ^ hash(self.reg_id)

    def __repr__(self):
        return '%s(%s)' % (self.__class__.__name__, self.reg_id)

    def __self__(self):
        return self


class MemoryDAO:
    """
    Store values in memory instead of any persistence
    Usually used in tests as a test fixture to raise coverage
    """

    def __init__(self):
        self._stack = {}

    def cls(self, obj):
        return obj.__class__.__name__

    def create(self, obj):
        if obj.reg_id in self._stack:
            raise FileExistsError
        self._stack[obj.reg_id] = deepcopy(obj)

    def retrieve(self, reg_id):
        if reg_id not in self._stack:
            raise FileNotFoundError
        obj = self._stack[reg_id]
        return deepcopy(obj)

    def retrieve_all(self):
        return [deepcopy(self._stack[i]) for i in self._stack]

    def update(self, obj):
        if obj.reg_id in self._stack:
            self._stack[obj.reg_id] = deepcopy(obj)
        else:
            raise FileNotFoundError

    def delete(self, obj):
        del self._stack[obj.reg_id]

    def find_by(self, attributes):
        assert isinstance(attributes, dict)
        result = []
        if len(self._stack) == 0:
            return result
        sample = list(self._stack.items())[0][1]
        intersect_keys = set(attributes).intersection(set(sample.__dict__))
        for k, reg in self._stack.items():
            for key in intersect_keys:
                stack_item = reg.__dict__
                if stack_item[key] == attributes[key]:
                    result.append(deepcopy(reg))
        return result

    def persist(self, obj):
        if obj.reg_id not in self._stack:
            self.create(obj)
        else:
            obj = self._stack[obj.reg_id]
        return deepcopy(obj)


class MemoryDAOFactory:

    def __init__(self):
        self.__instances = {}

    def get_instance(self, cls) -> MemoryDAO:
        if id(cls) in list(self.__instances.keys()):
            return self.__instances[id(cls)]
        self.__instances[id(cls)] = MemoryDAO()
        return self.__instances[id(cls)]
