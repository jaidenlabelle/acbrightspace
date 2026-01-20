from typing import Any, ClassVar


class Route:
    BASE: ClassVar[str] = "https://brightspace.algonquincollege.com"

    def __init__(self, method: str, path: str, **parameters: Any) -> None:
        self.method = method
        self.path = path

        if parameters:
            self.url = f"{self.BASE}{self.path.format(**parameters)}"
        else:
            self.url = f"{self.BASE}{self.path}"
