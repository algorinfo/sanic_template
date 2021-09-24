from dataclasses import dataclass
from typing import List, Optional


@dataclass
class CategoryResponse:
    id: int
    code: str
    created_at: str


@dataclass
class CategoryPost:
    code: int
    description: str

    def __post_init__(self):
        self.code = int(self.code)


@dataclass
class ArticlePost:
    title: str
    content: str
    category_id: int
    draft: bool = True
    author_id: Optional[int] = None
    id: Optional[int] = None

    def __post_init__(self):
        if self.category_id:
            self.category_id = int(self.category_id)
        if self.author_id:
            self.author_id = int(self.author_id)
        if self.id:
            self.id = int(self.id)

