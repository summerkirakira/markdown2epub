import markdown2
from typing import Optional
from markdown2 import Markdown
from models import ConverterConfig, ChapterMeta
import requests
from lxml import etree
import xml.etree.ElementTree as ET
import ebooklib
from ebooklib import epub
import pathlib


class BasicChapterConverter:
    """
    Basic Markdown converter
    """

    name: str = "Basic Chapter Converter"

    def __str__(self):
        return f"[{self.name}]"

    def __init__(self, config: ConverterConfig = ConverterConfig()):
        self.config = config
        self.markdown_converter: Markdown = Markdown()
        pass

    def _convert_md_to_html(self, md_str: str) -> (str, ChapterMeta):
        html = self.markdown_converter.convert(md_str)
        return html, ChapterMeta(**html.metadata)

    def convert_from_path(self, path: pathlib.Path) -> (str, ChapterMeta):
        with path.open('r') as f:
            md_content: str = f.read()
        return self._convert_md_to_html(md_content)


class EPUBConverter:
    """
    Basic Chapter Converter
    """

    name: str = "EPUB Converter"

    def __str__(self):
        return f"[{self.name}]"

    def __init__(self, config: ConverterConfig):
        self.config = config
        self.chapter_converter = BasicChapterConverter(self.config)
        self.md_path: Optional[pathlib.Path] = None
        self.epub_book = epub.EpubBook()

    def set_md_path(self, path: pathlib.Path) -> 'EPUBConverter':
        if not path.exists():
            raise ValueError("Path not exists")
        if not path.is_dir():
            raise ValueError("Path is not a directory")
        self.md_path = path
        return self

    def set_style(self, style: str) -> 'EPUBConverter':
        self.config.style = style
        return self

    def set_title(self, title: str) -> 'EPUBConverter':
        self.epub_book.set_title(title)
        return self

    def add_author(self, author: str) -> 'EPUBConverter':
        self.epub_book.add_author(author)
        return self

    def set_language(self, language: str) -> 'EPUBConverter':
        self.epub_book.set_language(language)
        return self

    def set_cover(self, file_name, content, create_page=True) -> 'EPUBConverter':
        self.epub_book.set_cover(file_name=file_name, content=content, create_page=create_page)
        return self

    def set_description(self, description: str) -> 'EPUBConverter':
        self.epub_book.add_metadata('DC', 'description', description)
        return self

    def add_metadata(self, name: str, content: str) -> 'EPUBConverter':
        self.epub_book.add_metadata(None, 'meta', '', {'name': name, 'content': content})
        return self


