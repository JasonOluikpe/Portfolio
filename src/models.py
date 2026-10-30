from dataclasses import dataclass


ClipData = tuple[str, str, str]  # Title, Caption, URL

@dataclass(frozen=True)
class Project:
    name: str
    summary: str
    description: str
    stack: list[str]
    links: list[tuple[str, str]]  # Label, URL
    overview: str
    clips: list[ClipData]
    more: str
    joke: str
    more_clips: list[ClipData]
