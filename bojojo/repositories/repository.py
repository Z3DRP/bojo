from abc import ABC, abstractmethod

class Repository(ABC):

    @abstractmethod
    def add(self, entity):
        pass

    @abstractmethod
    def get(self, entity_id):
        pass

    @abstractmethod
    def update(self, entity):
        pass

    @abstractmethod
    def delete(self, entity_id):
        pass
