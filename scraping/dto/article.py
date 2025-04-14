from dataclasses import dataclass
from dataclasses import dataclass
from typing import Any, Dict
import logging

@dataclass(frozen=True)
class ArticleDTO:
    title: str
    kicker: str
    link:str
    img_url: str

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ArticleDTO":
        # Validamos que todos los campos existan y sean strings
        for field in ("title", "kicker", "link", "img_url"):
            if field not in data or not isinstance(data[field], str):
                logging.error({"context":"ArticleDTO.from_dict()", "data":data})
                raise ValueError(f"Campo faltane o invalido: {field}")
        return cls(**data)