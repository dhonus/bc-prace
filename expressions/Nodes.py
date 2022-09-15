
class Node:
    def __init__(self):
        self.__value = "node"
        self.__left = None
        self.__right = None

    def get_value(self):
        return self.__value

    def prin(self):
        print("node")


class Impl(Node):
    def prin(self):
        print("Impl")
