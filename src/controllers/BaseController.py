import pathlib
from helpers import Settings


class BaseController:
    def __init__(self) -> None:
        self.app_settings = Settings()
        self.base_dir_path = pathlib.Path(__file__).parent.parent
        self.files_dir_path = self.base_dir_path.joinpath(
            pathlib.Path("assets").joinpath("files")
        )
        self.vectordb_dir_path = self.base_dir_path.joinpath(
            pathlib.Path("assets").joinpath("vectordb")
        )
        # create the needed directories
        self.files_dir_path.mkdir(parents=True, exist_ok=True)
        self.vectordb_dir_path.mkdir(parents=True, exist_ok=True)
