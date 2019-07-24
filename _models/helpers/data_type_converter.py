from numpy import array, float_


def list2array(inputList):
    """
    Converts list() to numpy.array()
    :param inputList: list()
    :return: numpy.array()
    """
    if inputList is None:
        raise ValueError
    else:
        return array(inputList, dtype=float_)
