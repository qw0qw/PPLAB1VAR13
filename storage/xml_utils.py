"""Вспомогательные функции преобразования Python-значений в XML и обратно."""
import xml.etree.ElementTree as ET
from typing import Any


def to_xml(parent: ET.Element, tag: str, value: Any) -> None:
    """Рекурсивно записывает значение в XML (тип хранится в атрибуте)."""
    element = ET.SubElement(parent, tag)
    if isinstance(value, dict):
        for key, item in value.items():
            to_xml(element, key, item)
    elif isinstance(value, list):
        element.set("type", "list")
        for item in value:
            to_xml(element, "item", item)
    elif value is None:
        element.set("type", "none")
    else:
        element.set("type", type(value).__name__)
        element.text = str(value)


def from_xml(element: ET.Element) -> Any:
    """Преобразует XML-элемент обратно в значение Python."""
    kind = element.get("type")
    if kind == "list":
        return [from_xml(child) for child in element]
    if kind == "none":
        return None
    if kind is None:
        return {child.tag: from_xml(child) for child in element}
    converters = {"int": int, "float": float, "str": str}
    return converters[kind](element.text or "")
