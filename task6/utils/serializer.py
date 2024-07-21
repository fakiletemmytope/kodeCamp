from typing import List, Any, Dict

async def serialize(lists: List[Any], obj: Any) -> Dict[str, Any]:
    serialized = {}
    for l in lists:
        serialized[l] = getattr(obj, l, None)  # Use getattr to fetch the attribute value from the object
    return serialized