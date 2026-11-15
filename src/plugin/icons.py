import json
from difflib import SequenceMatcher
from pathlib import Path
from typing import List, NamedTuple

ASSETS_DIR = Path(__file__).resolve().parent / "assets"
META_FILE = ASSETS_DIR / "meta.json"
FONT_FAMILY = str(ASSETS_DIR / "#Material Design Icons Desktop")
MATCH_THRESHOLD = 50


class Icon(NamedTuple):
    name: str
    aliases: List[str]
    codepoint: str

    @property
    def glyph(self) -> str:
        return chr(int(self.codepoint, 16))


def load_icons(path: Path = META_FILE) -> List[Icon]:
    entries = json.loads(path.read_text(encoding="utf-8"))
    return [Icon(entry["name"], entry.get("aliases") or [], entry["codepoint"]) for entry in entries]


def _is_separator(char: str) -> bool:
    return char in (" ", "-")


def similarity(query: str, text: str) -> float:
    return SequenceMatcher(_is_separator, query, text.lower()).ratio() * 100


def score(query: str, icon: Icon) -> float:
    query = query.lower()
    return max(similarity(query, text) for text in (*icon.aliases, icon.name))


def matches(query: str, icon_score: float) -> bool:
    return query == "" or icon_score > MATCH_THRESHOLD
