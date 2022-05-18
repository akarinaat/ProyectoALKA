import sys


class MaquinaVirtual:
    def __init__(self, message) -> None:
        print(message)


if __name__ == "__main__":
    MaquinaVirtual(sys.argv[1])
