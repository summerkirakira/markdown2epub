import enum

from pydantic import BaseModel
from typing import Optional
from ebooklib import epub


class ConverterConfig(BaseModel):
    convert_image: bool = True
    style: Optional[str] = None
    lang: Optional[str] = None


class ChapterType(enum.Enum):
    NOVEL = 0
    COMIC = 1


class ChapterMeta(BaseModel):
    chapter_order: int
    chapter_name: Optional[str] = None
    chapter_type: ChapterType = ChapterType.NOVEL
    show_chapter_order: bool = True
    download_headers: dict[str, str] = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/103.0.0.0 Safari/537.36 "
    }


class SectionDict(BaseModel):
    section_name: str
    section_order: int
    section_content: list[epub.EpubHtml]

