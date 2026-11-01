"""Реализация файлового хранилища XML."""
import xml.etree.ElementTree as ET

from exceptions.storage_error import StorageError
from .base import Storage
from .serialization import platform_to_dict, restore_platform
from .xml_utils import to_xml, from_xml


class XmlStorage(Storage):
    """Хранилище в формате XML."""

    def save(self, platform) -> None:
        root = ET.Element("platform")
        for key, value in platform_to_dict(platform).items():
            to_xml(root, key, value)
        tree = ET.ElementTree(root)
        ET.indent(tree)
        try:
            tree.write(self._path, encoding="utf-8", xml_declaration=True)
        except OSError as error:
            raise StorageError(f"Не удалось записать файл: {error}") from error

    def load(self):
        try:
            root = ET.parse(self._path).getroot()
        except FileNotFoundError:
            raise StorageError(f"Файл {self._path} не найден") from None
        except (OSError, ET.ParseError) as error:
            raise StorageError(f"Не удалось прочитать файл: {error}") from error
        try:
            data = {child.tag: from_xml(child) for child in root}
        except (KeyError, ValueError) as error:
            raise StorageError(f"Неверный формат XML: {error!r}") from error
        return restore_platform(data)
