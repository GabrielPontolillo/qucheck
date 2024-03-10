# create class that all property based tests inherit from, and add the required methods that specify input
# generation, preconditions, operations, and post conditions
from abc import ABC, abstractmethod


class Property(ABC):
    # constructor to initialise the class with the statistical analysis object
    def __init__(self, statistical_analysis):
        self.statistical_analysis = statistical_analysis
        self.classical_assertion_outcome = True

    # generate inputs for the test
    # outputs a list of the generated inputs
    @abstractmethod
    def generate_input(self):
        pass

    # specify the preconditions for the test
    @abstractmethod
    def preconditions(self):
        pass

    # the coordinator will pass all inputs in list order to the operations method
    # specify the operations to be performed on the input
    @abstractmethod
    def operations(self, *inputs):
        pass
