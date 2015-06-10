from functools import wraps


def lens(f):
    @wraps(f)
    def wrapper(self):
        return Lens(self, f(self))
    return property(wrapper)


class Lens:
    def __init__(self, obj, override):
        self.__obj = obj
        self.__override = override

    def __getattr__(self, attr):
        if self.__override:
            return (
                getattr(self.__override, attr, None)
                or getattr(self.__obj, attr))
        else:
            return getattr(self.__obj, attr)
