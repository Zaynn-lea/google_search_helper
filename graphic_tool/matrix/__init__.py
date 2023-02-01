
"""
subpackage to contain a collection of dictionary, functions, classes and so on to defines matrices, theirs operation and
some utilities

@author: Zaynn-Lea

see on gitHub :
    * author :
        - Zaynn-Lea : https://github.com/Zaynn-lea

you can directly import the main matrix submodule using :
    from graphic_tool import matrix

this sub package has been created by spliting the matrix file into the matrix and JavidX9Matrix file,
due to circular import

------------------------------------------------------------------------------------------------------------------------

    - matrix : a submodules to handle classic matrices definitions, operations and manipulations

    - JavidX9Matrix : a submodules to handle the specific matrices definitions, operations and manipulations
                        used by JavidX9 in : https://www.youtube.com/watch?v=ih20l3pJoeU
"""

__author__ = "Gely Lea"

__all__ = ["matrix", "JavidX9Matrix"]

# so that the main submodule can be imported just as :
#   from graphic_tool import matrix

from .matrix import *
