class Singleton(type):
    """A metaclass that creates a Singleton base class when called.

    Instances can be called with constructor, or using get_instance() method. The latter
    is more descritive of what is happening behind the constructor.

    """

    _instances = {}

    def __call__(cls, *args, **kwargs):
        # This convertes calls MyClass() to Singleton.__call__(MyClass)
        if cls not in Singleton._instances:
            Singleton._instances[cls] = super().__call__(*args, **kwargs)
        return Singleton._instances[cls]

    def get_instance(cls):
        # This is the same as return Singleton.__call__(cls)
        return cls()
