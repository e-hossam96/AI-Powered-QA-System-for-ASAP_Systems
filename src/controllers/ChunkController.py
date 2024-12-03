import bs4
import pathlib
import wikipediaapi
from urllib.parse import urlparse, unquote
from .BaseController import BaseController
from configs import AssetTypeConfig
from langchain_core.documents.base import Document
from langchain_community.document_loaders import (
    TextLoader,
    PyMuPDFLoader,
    WebBaseLoader,
)
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

    def get_wikipedia_webpage_text(self, title: str, **kwargs) -> str | None:
        wiki_api = wikipediaapi.Wikipedia(**kwargs)
        page = wiki_api.page(title)
        if not page.exists():
            return None

        def format_section(section, level=0):
            excluded_sections = ["See also", "References", "External links"]
            text = ""
            # skip unwanted sections
            if section.title in excluded_sections:
                return text
            # add title if not main title
            if section.title != page.title:
                text += f"{'\t' * level}{section.title}\n"
            # add section text
            if section.text:
                text += f"{'\t' * level}{section.text}\n"
            # recursively format sub-sections
            for subsection in section.sections:
                text += format_section(subsection, level + 1)
            return text
        
        page_text = format_section(page)
        return page_text.strip()
