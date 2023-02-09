
"""
package to contain a collection of dictionary, functions, classes and so on to help when doing graphics

@author: Zaynn-Lea

see on gitHub :
    * author :
        - Zaynn-Lea : https://github.com/Zaynn-lea

------------------------------------------------------------------------------------------------------------------------

    - colors : a submodules to handle color definition and manipulation

    - vector : a submodules to handle vectors definitions, operations and manipulations

    - triangles : a submodules to handle definition and manipulation of triangles and meshes of triangles

    - square_tyle : a submodules to handle definition and manipulation of 2D square tyles

------------------------------------------------------------------------------------------------------------------------

    - matrix : a subpackage to handle matrices definitions, operations and manipulations

------------------------------------------------------------------------------------------------------------------------

I advise to have a file where you import every submodule/package you're gonna use such that you can import more easily
in the rest of your project
example :

graphic_tool_import.py :

    from graphic_tool.vector import *
    from graphic_tool.colors import *
    from graphic_tool.square_tyle import *

rest of your project :

    import graphic_tool_import as gt

with this way, you only import with the tools you need and you have them in a single namespace
"""

__author__ = "Gely Lea"

__all__ = ["vector", "matrix", "triangles", "square_tile.py", "colors", "border"]
