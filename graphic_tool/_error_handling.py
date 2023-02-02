
"""
submodule of the graphic_tool package made to define and handle custom error for the package

@author: Zaynn-Lea

see on gitHub :
    * author :
        - Zaynn-Lea : https://github.com/Zaynn-lea

------------------------------------------------------------------------------------------------------------------------

    - LengthError : inherit from ValueError and define a more specific length error

    - ExtensionError : inherit from ValueError and define a more specific extension error

    - test_class : function to test if an object is an instance of a class or subclass
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
    function to test if an object is an instance of a class or an instance of a subclass
    of at least one of the type or class given in *args

    --------------------------------------------------------------------------------------------------------------------

    :param var: the variable you need to test

    :param *args: one or more class and type

    :return: the result of the test
    :type: bool
    """
    test = False
    state = True
    i = 0

    while state and not test:
        try:
            test = isinstance(var, *args[i]) or issubclass(type(var), *args[i])

        except IndexError:
            state = False

        else:
            i += 1

    return test
