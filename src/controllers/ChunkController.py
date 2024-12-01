import pathlib
from .BaseController import BaseController
from configs import AssetTypeConfig
from models.data_schemas import Chunk
from bson.objectid import ObjectId
from langchain_core.documents.base import Document
from langchain_community.document_loaders import TextLoader, PyMuPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter


class ChunkController(BaseController):
    def __init__(self) -> None:
        super().__init__()

    def get_asset_path(self, asset_name: str) -> pathlib.Path:
        return self.files_dir_path.joinpath(asset_name)

    def get_unstructured_asset_loader(
        self, asset_path: pathlib.Path
    ) -> TextLoader | PyMuPDFLoader | None:
        asset_ext = asset_path.suffix
        asset_loader = None
        if asset_path.exists():
            if asset_ext == AssetTypeConfig.TEXT.value:
                asset_loader = TextLoader(asset_path, encoding="utf-8")
            elif asset_ext == AssetTypeConfig.PDF.value:
                asset_loader = PyMuPDFLoader(str(asset_path))
        return asset_loader

    def get_unstructured_asset_content(
        self, asset_path: pathlib.Path
    ) -> list[Document]:
        asset_loader = self.get_unstructured_asset_loader(asset_path)
        asset_content = None
        if asset_loader is not None:
            asset_content = asset_loader.load()
        return asset_content

    def process_unstructured_asset_content(
        self, asset_content: list[Document], chunk_size: int, overlap_size: int
    ) -> list[Document]:
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=overlap_size,
        )
        texts = [doc.page_content for doc in asset_content]
        metadata = [doc.metadata for doc in asset_content]
        asset_chunks = text_splitter.create_documents(texts=texts, metadatas=metadata)
        return asset_chunks

    # def convert_unstructured_asset_chunks_to_chunks(
    #     self,
    #     asset_chunks: list[Document],
    #     source_name: str,
    #     source_id: ObjectId,
    # ) -> list[Chunk]:
    #     chunks = [
    #         Chunk(text=c.page_content, source_name=source_name, source_id=source_id)
    #         for c in asset_chunks
    #     ]
    #     return chunks
