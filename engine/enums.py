from enum import Enum, auto

class Tile(Enum):
    WHITE = auto()
    PURPLE = auto()
    EMPTY = auto()

COLORS = {
    "blue": "#76c1ff",
    "yellow": "#fffe72",
    "green": "#65fc8e",
    "red": "#ff6868",
    "cyan": "#39e6eb",
    "purple": "#c792ea",
    "orange": "#ff9f1c",
    "brown": "#b58b5b",
    "white": "#ffffff"
}