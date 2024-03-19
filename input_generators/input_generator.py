# abstract base class for input_generators that creates an abstract method called generate
from abc import ABC, abstractmethod


class InputGenerator(ABC):
    @abstractmethod
    def generate(self, seed):
        pass
