
"""
submodule of the graphic_tool package made to define and handle custom error for the package

@author: Zaynn-Lea

see on gitHub :
    * author :
        - Zaynn-Lea : https://github.com/Zaynn-lea

------------------------------------------------------------------------------------------------------------------------

    - LengthError : inherit from ValueError and define a more specific length error

    - ExtensionError : inherit from ValueError and define a more specific extension error
"""


# +------------------+
# |   custom error   |
# +------------------+
class LengthError(ValueError):
    """
    this class defines a custom error to handle a length error

    this class inherits from ValueError
    """
    pass


class ExtensionError(ValueError):
    """
    this class defines a custom error to handle a extension error

    this class inherits from ValueError
    """
    pass


# +---------------------+
# |   tests functions   |
# +---------------------+
def test_class(var, *args: type) -> bool:
    """
    TODO
    """
    classes = list(args)
    test = True
    i = 0

    while test:
        test = isinstance(var, classes[i]) or issubclass(type(var), classes[i])

    return test
