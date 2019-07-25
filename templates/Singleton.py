from typing import Optional, Dict, Any


class Singleton(type):
    _instances: Optional[Dict] = {}

    def __call__(cls, *args: Any,
                 **kwargs: Any) -> object:
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        # else:
        #     cls._instances[cls].__init__(*args, **kwargs)
        return cls._instances[cls]

# Example:
# class Logger(metaclass=Singleton):
#     pass
