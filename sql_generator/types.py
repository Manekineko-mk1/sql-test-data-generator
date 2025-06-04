# sql_generator/types.py
from typing import Dict, List, Tuple

Schema = Tuple[str, Dict[str, str]]
SharedValues = List[Dict[str, str]]
InsertStatements = List[Tuple[str, List[str]]]