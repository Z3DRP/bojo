from typing import Any, Dict, List, NamedTuple

class DbResponse(NamedTuple):
    entityList: List[Dict[str, Any]]
    error: int