from typing import Any, Dict, NamedTuple

class CurrentItem(NamedTuple):
    item: Dict[str, Any]
    excCode: int