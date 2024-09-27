import json
from typing import Optional, Union


def read_json(path: str, encoding: Optional[str] = None) -> Union[list, dict]:
    return json.load(open(path, encoding=encoding))
