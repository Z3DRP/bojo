from typing import Any, Dict, List, NamedTuple

class DbResponse(NamedTuple):
    entityList: List[Dict[str, Any]]
    excCode: int
    exception: str
