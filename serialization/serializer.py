"""This module contains the Serializable Class and corresponding contstants,
it's in charge of managing the savings and loadings of Serializable objects,
plus some utilities relate"""
#TODO build a ConsistantDataPath to serialize to

from dataclasses import dataclass, field
from enum import Enum, auto
from json import dumps, load
from os import listdir, path
from typing import Any, Callable, Generic, Optional, TypeVar

from serialization.file_format import FileFormat
from serialization.serializable import Serializable
from utils.utils import get_asset_path

JSON_INDENT = 4
ENCODING = "utf-8"
FILE_EXTENSION = "json"

class SerializeResult(Enum):
    """Result status for serialization
    """
    SUCCESFULL = auto()
    MAX_SAVES_REACHED = auto()
    NOT_FOUND = auto()
    INCORRECT_OBJ_TYPE=auto()

class DeserializeResult(Enum):
    """Result status for deserialization
    """
    SUCCESFULL = auto()
    NOT_FOUND = auto()
    MISSING_ATTRS = auto()


Ser = TypeVar("Ser", bound=Serializable)
@dataclass
class Serializer(Generic[Ser]):
    """Serializer for Serializable Objects, requires a Serializable Type for it's Ser Generic type

    Attributes:
        format (FileFormat): File format
        constructor (Callable[[dict[str, Any]], Ser]): The Serializable Object constructor
        max_saves_count (int): The maximum amount of saves if any
        has_max_saves (bool): Whether the serializable has or not a limit in savings

    """

    format: FileFormat
    constructor: Callable[[dict[str, Any]], Ser]
    max_saves_count: int = 0
    has_max_saves: bool = field(init=False)

    def __post_init__(self) -> None:
        if not self.format.is_valid_format(FILE_EXTENSION):
            raise ValueError("Invalid file format provided")
        self.has_max_saves = self.max_saves_count > 0

    def get_saves(self, dir_path: str) -> list[str]:
        """Get the saves in a directory

        Args:
            dir_path (str): Directory

        Returns:
            list[str]: File names of saves in directory
        """
        files = filter(lambda f: path.isfile(path.join(dir_path, f)), listdir(dir_path))
        saves = filter(self.format.is_of_format, files)
        return list(saves)

    def _validate_max_saves(self, dir_path: str) -> bool:
        if not self.has_max_saves:
            return False
        saves_count = len(self.get_saves(dir_path))
        return saves_count >= self.max_saves_count

    def serialize(self, obj: Ser, filename: str, *directories: str) -> SerializeResult:
        """Serializes the specified Serializable if possible

        Args:
            obj (Ser): Object to serialize
            filename (str): Filename
            *directories (str): Sub directories in the specified Asset Type

        Returns:
            SerializeResult: Result status
        """
        # Format Json for fixing visualization
        def format_json(json: str) -> str:
            removed = 0
            second_char = False
            in_brackets = False
            for i, c in enumerate(json):
                if c == '[':
                    if second_char is False:
                        second_char = True
                        continue
                    in_brackets = True
                if c == ']':
                    in_brackets = False
                if in_brackets and c in ('\n', ' '):
                    json = json[:i-removed] + json[i+1-removed:]
                    removed += 1
            return json

        # Validate Maximum Saves Reached
        dir_path = get_asset_path(self.format.asset_type, *directories)
        if self._validate_max_saves(*directories):
            return SerializeResult.MAX_SAVES_REACHED

        try:
            file_fullname = self.format.get_fullname(filename)
            file_path = path.join(dir_path, file_fullname)
            with open(file_path, "w", encoding=ENCODING) as file:
                json_dict = obj.get_serialization_attrs()
                json = format_json(dumps(json_dict, indent=JSON_INDENT))
                file.write(json)
                return SerializeResult.SUCCESFULL

        except FileNotFoundError:
            return SerializeResult.NOT_FOUND

    def _try_deserialize(self, file_path: str, **kwargs: Any) -> Ser | DeserializeResult:
        try:
            with open(file_path, "r", encoding=ENCODING) as file:
                json = load(file)
            return self.constructor(json, **kwargs)
        except KeyError:
            return DeserializeResult.MISSING_ATTRS
        except FileNotFoundError:
            return DeserializeResult.NOT_FOUND

    def deserialize(self, filename: str, *directories: str,
                    **kwargs: Any) -> tuple[Optional[Ser], DeserializeResult]:
        """Deserializes object if found and is valid

        Args:
            filename (str): Filename
            *directories (str): Sub directories in the specified Asset Type
            **kwargs (Any): Additional arguments for the Serializable Constructor

        Returns:
            tuple[Optional[Ser], DeserializeResult]: Loaded object if valid and result status
        """
        file_fullname = self.format.get_fullname(filename)
        file_path = get_asset_path(self.format.asset_type, *[*directories, file_fullname])
        obj = self._try_deserialize(file_path, **kwargs)

        if isinstance(obj, DeserializeResult):
            return None, obj
        return obj, DeserializeResult.SUCCESFULL
