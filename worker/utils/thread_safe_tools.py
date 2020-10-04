from sys import stdout


class ThreadSafeTools:

    @staticmethod
    def print(message: str):
        stdout.write(message)

    @staticmethod
    def convert_gigabytes_to_bytes(size: float):
        return size * 1000000000
