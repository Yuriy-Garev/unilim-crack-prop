from typing import List

from numpy import array, float_


def list2array(inputList: List) -> array:
    """
    Converts list() to numpy.array()
    :param inputList: list()
    :return: numpy.array()
    """
    if inputList is None:
        raise ValueError
    else:
        return array(inputList, dtype=float_)
