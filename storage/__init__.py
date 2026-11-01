"""Публичный интерфейс файловых хранилищ."""

from .base import Storage
from .json_storage import JsonStorage
from .xml_storage import XmlStorage
from .serialization import platform_to_dict, platform_from_dict, restore_platform

__all__ = [
    "Storage", "JsonStorage", "XmlStorage",
    "platform_to_dict", "platform_from_dict", "restore_platform",
]
