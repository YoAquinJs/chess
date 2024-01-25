"""TODO"""

from os import path, listdir
from enum import Enum, auto
from typing import Any, Callable, Generic, Optional, TypeVar
from json import dumps, load
from game_logic.serializable import Serializable
from game_logic.consts import AssetType
from utils.utils import get_asset_path

ENCODING = "utf-8"
JSON_INDENT = 4

class SerializeResultStatus(Enum):
    """TODO
    """
    SUCCESFULL = auto()
    MAX_SAVES_REACHED = auto()
    NOT_FOUND = auto()
    INCORRECT_OBJ_TYPE=auto()

class DeserializeResultStatus(Enum):
    """TODO
    """
    SUCCESFULL = auto()
    NOT_FOUND = auto()

Ser = TypeVar("Ser", bound=Serializable)
class Serializer(Generic[Ser]):
    """TODO
    """

    def __init__(self, file_end: str, file_prefix: str, asset_type: AssetType,
                 max_saves_count: int=0) -> None:
        if not file_end.endswith(".json"):
            raise ValueError("File end must be .json")
        self.file_end = file_end
        self.file_prefix = file_prefix
        self.asset_type = asset_type
        self.has_max_saves = max_saves_count > 0
        self.max_saves_count = max_saves_count


    def count_saves(self, *directories: str, asset_type: AssetType=AssetType.SAVINGS) -> int:
        """Return the count of saves in the specified directory

        Args:
            asset_type (AssetType, optional): Type of asset. Defaults to AssetType.SAVINGS.

        Returns:
            int: Count
        """
        directory_path = get_asset_path(asset_type, *directories)
        is_file: Callable[[str], bool] = lambda f: path.isfile(path.join(directory_path, f))
        is_save: Callable[[str], bool] = lambda f: f.startswith(self.file_prefix) and f.endswith(self.file_end)
        file_names = [f for f in listdir(directory_path) if is_file(f)]
        saved_files = [f for f in file_names if is_save(f)]
        return len(saved_files)

    def serialize(self, obj: Ser, filename: str, *directories: str) -> SerializeResultStatus:
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
        directory_path = get_asset_path(self.asset_type, *directories)
        if self.has_max_saves:
            saves_count = self.count_saves(*directories, asset_type=self.asset_type)
            if saves_count >= self.max_saves_count:
                return SerializeResultStatus.MAX_SAVES_REACHED
        try:
            file_path = path.join(directory_path, f"{self.file_prefix}{filename}{self.file_end}")
            with open(file_path, "w", encoding=ENCODING) as file:
                json_dict = obj.get_serialization_attrs()
                json_string = format_json(dumps(json_dict, indent=JSON_INDENT))
                file.write(json_string)
                return SerializeResultStatus.SUCCESFULL

        except FileNotFoundError:
            return SerializeResultStatus.NOT_FOUND

    def deserialize(self, contructor: Callable[[dict[str, Any]], Ser], filename: str,
                    *directories: str)-> tuple[Optional[Ser], DeserializeResultStatus]:
        """TODO
        """
        try:
            file_fullname = f"{self.file_prefix}{filename}{self.file_end}"
            file_path = get_asset_path(self.asset_type, *[*directories, file_fullname])
            with open(file_path, "r", encoding=ENCODING) as file:
                json_dict = load(file)
                obj = contructor(json_dict)
                return obj, DeserializeResultStatus.SUCCESFULL

        except FileNotFoundError:
            return None, DeserializeResultStatus.NOT_FOUND

#TODO serializable interface and abstraction for code repetition
#TODO build a ConsistantDataPath to serialize to
