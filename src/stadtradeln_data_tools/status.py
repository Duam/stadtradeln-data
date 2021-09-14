from enum import Enum


class Status(Enum):
    UNKNOWN_DATASET = 0
    FILE_ALREADY_EXISTS = 1
    FAILURE = 2
    SUCCESS = 3
    SSL_ERROR = 4

