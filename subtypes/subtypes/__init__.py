"""
'subtypes' is too much of a common package name, avoid clashes
"""
from pkgutil import extend_path

__path__ = extend_path(__path__, __name__)

