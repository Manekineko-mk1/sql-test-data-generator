# sql_generator/utils.py
import re
from typing import Tuple

def parse_data_type(full_data_type: str) -> Tuple[str, int | None, int | None, bool]:
    """
    Parse SQL data type into base type, length, precision, and NOT NULL status.
    
    Args:
        full_data_type: Full SQL data type (e.g., 'DECIMAL(2)', 'INT', 'DECIMAL(5, 3) NOT NULL').
    
    Returns:
        Tuple of (base_type, length, precision, not_null).
    
    Raises:
        ValueError: If the data type format is invalid.
    """
    regex = r'(\w+)\s*(?:\((\d+)\s*(?:,\s*(\d+))?\))?\s*(\bNOT\s+NULL)?'
    type_match = re.match(regex, full_data_type, re.IGNORECASE)
    if not type_match:
        raise ValueError(f"Invalid data type format: {full_data_type}")
    
    base_type = type_match.group(1).upper()
    length = int(type_match.group(2)) if type_match.group(2) else None
    precision = int(type_match.group(3)) if type_match.group(3) else None
    not_null = bool(type_match.group(4))
    
    return base_type, length, precision, not_null