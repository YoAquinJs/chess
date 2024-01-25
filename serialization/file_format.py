"""TODO"""

from dataclasses import dataclass

from game_logic.consts import AssetType


@dataclass
class FileFormat():
    """TODO"""
    file_end: str
    file_prefix: str
    asset_type: AssetType

    def is_valid_format(self, extension: str) -> bool:
        """TODO
        """
        return self.file_end.endswith(extension)
