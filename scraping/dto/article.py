from dataclasses import dataclass

@dataclass
class ArticleDTO:
    title: str
    kicker: str | None
    link:str
    img_url: str