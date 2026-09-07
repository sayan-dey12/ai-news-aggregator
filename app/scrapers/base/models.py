from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class RSSArticle(BaseModel):
    title: str
    description: str
    url: str
    guid: str
    published_at: datetime
    category: Optional[str] = None