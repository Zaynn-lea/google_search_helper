
"""
submodule of the graphic_tool package made to define and handle custom error for the package

made by Gely Lea

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
