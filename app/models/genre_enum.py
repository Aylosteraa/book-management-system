from enum import Enum


class GenreEnum(str, Enum):
    FICTION = "fiction"
    FANTASY = "fantasy"
    SCI_FI = "sci_fi"
    HORROR = "horror"
    HISTORY = "history"
    BIOGRAPHY = "biography"
    ROMANCE = "romance"