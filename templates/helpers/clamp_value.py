from typing import Union


def Clamp(value: Union[float, int],
          lowerBound: Union[float, int],
          upperBound: Union[float, int]) -> Union[float, int]:
    """
    Clamp the given value between lower and upper bounds.
    if value > upper_bound -> return upper_bound
    elif value < lower_bound -> return lower_bound
    else return value

    :param value: float
    :param lowerBound: float
    :param upperBound: float
    :return: float
    """
    return max(lowerBound, min(upperBound, value))


def ClampPositive(value: Union[float, int],
                  upperBound: Union[float, int]) -> Union[float, int]:
    """
    Clamp the given value between lower and upper bounds.
    if value > upper_bound -> return upper_bound
    elif value < 0 -> value = return 0
    else return value

    :param value: float
    :param upperBound: float > 0
    :return: float
    """
    return max(0, min(upperBound, value))
