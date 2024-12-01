import re
import random
import string
import pathlib
import aiofiles
from fastapi import UploadFile
from .BaseController import BaseController


class AssetController(BaseController):
    def __init__(self) -> None:
        super().__init__()

    def validate_unstructured_asset_type(self, asset: UploadFile) -> bool:
        is_valid = True
        if asset.content_type not in self.app_settings.ASSET_UNSTRUCTURED_ALLOWED_TYPES:
            is_valid = False
        return is_valid

    def validate_unstructured_asset_size(self, asset: UploadFile) -> bool:
        is_valid = True
        if asset.size > self.app_settings.ASSET_UNSTRUCTURED_ALLOWED_SIZE:
            is_valid = False
        return is_valid

    def generate_random_string(self, length: int = 12) -> str:
        population = string.ascii_lowercase + string.digits
        return "".join(random.choices(population=population, k=length))

    def get_clean_asset_name(self, name) -> str:
        return re.sub(r"\W", r".", name)

    def get_unique_asset_path(self, filename: str) -> tuple[pathlib.Path, str]:
        clean_asset_name = self.get_clean_asset_name(filename)
        prefix = self.generate_random_string()
        unique_asset_name = f"{prefix}__{clean_asset_name}"
        unique_asset_path = self.files_dir_path.joinpath(unique_asset_name)
        while unique_asset_path.exists():
            prefix = self.generate_random_string()
            unique_asset_name = f"{prefix}__{clean_asset_name}"
            unique_asset_path = self.files_dir_path.joinpath(unique_asset_name)
        return unique_asset_path, unique_asset_name

    async def write_uploaded_unstructured_asset(
        self, asset: UploadFile, asset_path: pathlib.Path
    ) -> bool:
        result = True
        try:
            async with aiofiles.open(asset_path, "wb") as f:
                while asset_chunk := await asset.read(
                    size=self.app_settings.ASSET_UNSTRUCTURED_UPLOAD_CHUNK_SIZE
                ):  # walrus operator
                    await f.write(asset_chunk)
        except Exception as e:
            result = False
        return result
