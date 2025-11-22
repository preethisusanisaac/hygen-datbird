# app/utils/parsing.py
import re
from typing import Optional, Tuple


def parse_budget(text: str) -> Tuple[Optional[float], Optional[float]]:
    """
    Very simple budget parser.
    Examples:
      "50 lakhs" -> (5000000, None)
      "50-70L"   -> (5000000, 7000000)
    For MVP: rough parsing is enough.
    """
    text = text.lower().replace(" ", "")
    # Handle range like 50-80l or 50l-80l
    m = re.match(r"(\d+)[lLkK]?-?(\d+)?[lLkK]?", text)
    if not m:
        # Just single number
        m2 = re.search(r"(\d+)", text)
        if not m2:
            return None, None
        val = float(m2.group(1))
        # Assume lakhs if > 50
        if val < 1000:
            val = val * 100000  # treat as lakhs
        return val, None

    v1 = float(m.group(1))
    v2 = float(m.group(2)) if m.group(2) else None

    # Assume lakhs
    v1 = v1 * 100000
    if v2 is not None:
        v2 = v2 * 100000

    return v1, v2
