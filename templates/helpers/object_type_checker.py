def isFunction(obj: object) -> bool:
    """Returns True if the object is type of function"""

    return str(type(obj)) == '<class \'function\'>'


def isMethod(obj: object) -> bool:
    """Returns True if the object is type of class method"""

    return str(type(obj)) == '<class \'method\'>'
