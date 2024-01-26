"""This module contains the FileFormat class """

from dataclasses import dataclass

from game_logic.consts import AssetType


@dataclass
class FileFormat():
    """Represents the naming format for serialization

    Attributes:
        file_end (str): _description_
        file_prefix (str): _description_
        asset_type (AssetType): _description_

    """
    file_end: str
    file_prefix: str
    asset_type: AssetType

    def is_valid_format(self, extension: str) -> bool:
        """Whether the format matches the extension

        Args:
            extension (str): Extension

        Returns:
            bool: Whether is valid
        """
        return self.file_end.endswith(extension)

    def is_of_format(self, file: str) -> bool:
        """If the file is of this format

        Args:
            file (str): Full filename

        Returns:
            bool: Whether is of this format
        """
        return file.startswith(self.file_prefix) and file.endswith(self.file_end)

    def get_fullname(self, filename: str) -> str:
        """Compute the fullnmae of a filename

        Args:
            filename (str): Filename

        Returns:
            str: Fullname
        """
        return f"{self.file_prefix}{filename}{self.file_end}"
