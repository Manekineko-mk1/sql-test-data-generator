# sql_generator/data_generator.py
import re
import random
import string
from datetime import datetime, timedelta

class DataGenerator:
    """Generates random test data based on column data type specifications."""
    
    @staticmethod
    def generate_value(full_data_type: str) -> str:
        """
        Generate a random value based on the full SQL data type specification.
        
        Args:
            full_data_type: Full SQL data type (e.g., 'CHAR(2) NOT NULL', 'VARCHAR(50)', 'INT').
        
        Returns:
            A string representation of the generated value.
        """
        # Parse the data type
        type_match = re.match(r'(\w+)(\((\d+)(,(\d+))?\))?(\s+NOT\s+NULL)?', full_data_type, re.IGNORECASE)
        if not type_match:
            return "'Unknown'"
        
        base_type = type_match.group(1).upper()
        length = int(type_match.group(3)) if type_match.group(3) else None
        precision = int(type_match.group(5)) if type_match.group(5) else None
        
        if base_type in ('CHAR', 'VARCHAR'):
            gen_length = length if length else random.randint(5, 20)
            value = ''.join(random.choices(string.ascii_letters, k=gen_length))
            return f"'{value}'"
        elif base_type in ('INT', 'INTEGER'):
            return str(random.randint(1, 1000))
        elif base_type in ('DECIMAL', 'FLOAT', 'DOUBLE'):
            scale = precision if precision else 2
            value = round(random.uniform(0, 1000), scale)
            return str(value)
        elif base_type in ('DATE', 'DATETIME'):
            start_date = datetime(2020, 1, 1)
            days_offset = random.randint(0, 365 * 5)
            random_date = start_date + timedelta(days=days_offset)
            return f"'{random_date.strftime('%Y-%m-%d')}'"
        elif base_type == 'BOOLEAN':
            return random.choice(['TRUE', 'FALSE'])
        else:
            return "'Unknown'"