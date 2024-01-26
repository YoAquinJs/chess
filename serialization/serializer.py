"""TODO"""
#TODO build a ConsistantDataPath to serialize to

from dataclasses import dataclass, field
from os import path, listdir
from enum import Enum, auto
from typing import Any, Callable, Generic, Optional, TypeVar
from json import dumps, load
from serialization.file_format import FileFormat
from serialization.serializable import Serializable
from game_logic.consts import AssetType
from utils.utils import get_asset_path

ENCODING = "utf-8"
JSON_INDENT = 4
FILE_EXTENSION = "json"
class SerializeResult(Enum):
    """TODO
    """
    SUCCESFULL = auto()
    MAX_SAVES_REACHED = auto()
    NOT_FOUND = auto()
    INCORRECT_OBJ_TYPE=auto()

class DeserializeResult(Enum):
    """TODO
    """
    SUCCESFULL = auto()
    NOT_FOUND = auto()
    MISSING_ATTRS = auto()

Ser = TypeVar("Ser", bound=Serializable)
@dataclass
class Serializer(Generic[Ser]):
    """TODO
    """

    format: FileFormat
    constructor: Callable[[dict[str, Any]], Ser]
    max_saves_count: int = 0
    has_max_saves: bool = field(init=False)
    def __post_init__(self) -> None:
        if not self.format.is_valid_format(FILE_EXTENSION):
            raise ValueError("Invalid file format provided")
        self.has_max_saves = self.max_saves_count > 0


    def count_saves(self, *directories: str, asset_type: AssetType=AssetType.SAVINGS) -> int:
        """Return the count of saves in the specified directory

        Args:
            asset_type (AssetType, optional): Type of asset. Defaults to AssetType.SAVINGS.

        Returns:
            int: Count
        """
        dir_path = get_asset_path(asset_type, *directories)
        prefix, file_end = self.format.file_prefix, self.format.file_end
        files = filter(lambda f: path.isfile(path.join(dir_path, f)), listdir(dir_path))
        saves = filter(lambda f: f.startswith(prefix) and f.endswith(file_end), files)
        return len(list(saves))

    def serialize(self, obj: Ser, filename: str, *directories: str) -> SerializeResult:
        """TODO
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
        if self.has_max_saves:
            saves_count = self.count_saves(*directories, asset_type=self.format.asset_type)
            if saves_count >= self.max_saves_count:
                return SerializeResult.MAX_SAVES_REACHED
        try:
            file_fullname = f"{self.format.file_prefix}{filename}{self.format.file_end}"
            file_path = path.join(dir_path, file_fullname)
            with open(file_path, "w", encoding=ENCODING) as file:
                json_dict = obj.get_serialization_attrs()
                json_string = format_json(dumps(json_dict, indent=JSON_INDENT))
                file.write(json_string)
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
        """TODO
        """
        file_fullname = f"{self.format.file_prefix}{filename}{self.format.file_end}"
        file_path = get_asset_path(self.format.asset_type, *[*directories, file_fullname])
        obj = self._try_deserialize(file_path, **kwargs)

        if isinstance(obj, DeserializeResult):
            return None, obj
        return obj, DeserializeResult.SUCCESFULL
