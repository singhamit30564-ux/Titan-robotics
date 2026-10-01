"""Titan Robotics - an offline, educational Streamlit app about robots.

Package layout:
    titan.logic       pure helpers (no Streamlit) - filtering, validation, maths
    titan.dataio      loads the bundled JSON data from ``data/``
    titan.theme       dark blue/gold theme + CSS
    titan.components  small HTML card/grid builders
    titan.views       one render function per page
"""

__all__ = ["logic", "dataio", "theme", "components", "views"]
__version__ = "1.0.0"
