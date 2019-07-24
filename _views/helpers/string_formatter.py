from typing import Iterable


def PreformatArrayLikeData(array_like_data: Iterable,
                           array_name: str) -> str:
    str_arr = str(array_name) + "\n"
    str_arr += "[\n"
    for i in array_like_data[:-1]:
        str_arr += "  " + str(i) + "\n"
    str_arr += "  " + str(array_like_data[-1])
    str_arr += "\n]\n"
    return str_arr
