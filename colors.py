
"""
submodule du package graphic_tool made to handle color definition and manipulation

here the module has been extracted from the package to be use as a stand alone

@author: Zaynn-Lea

see on gitHub :
    * author :
        - Zaynn-Lea : https://github.com/Zaynn-lea

    * project : https://github.com/Zaynn-lea/google_search_helper

------------------------------------------------------------------------------------------------------------------------

this module contains :

    - colors : a dictionary which keys are string of color name in english and values are the triplets (r, g, b)
"""

# +----------------------+
# |   color dictionary   |
# +----------------------+
colors = {
    # black, grey shades and white
    "black": (0, 0, 0),
    "grey": (128, 128, 128),
    "grey-75%": (192, 192, 192),
    "grey-50%": (128, 128, 128),
    "grey-25%": (64, 64, 64),
    "white": (255, 255, 255),

    # red, green, blue
    "red": (255, 0, 0),
    "green": (0, 255, 0),
    "blue": (0, 0, 255),

    # yellow, cyan, magenta
    "yellow": (255, 255, 0),
    "cyan": (0, 255, 255),
    "magenta": (255, 0, 255),
}
