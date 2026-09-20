"""Smart Compressor: safe local compression utilities."""

__version__ = "1.0.0"
__author__ = "Radwan Abdulhadi Ahmed (@rad03i2)"

from .core import CompressionError, compress, extract, inspect_archive

__all__ = ["CompressionError", "compress", "extract", "inspect_archive"]
