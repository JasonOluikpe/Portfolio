from dataclasses import dataclass


ClipData = tuple[str, str, str] # Title, Caption, Filepath

@dataclass(frozen=True)
class Project:
    name: str
    summary: str
    description: str
    stack: list[str]
    links: list[tuple[str, str]] # Label, URL
    overview: tuple[str, str] # Filepath, Placeholder Text
    clips: list[ClipData]
    more: str
    joke: str
    more_clips: list[ClipData]
