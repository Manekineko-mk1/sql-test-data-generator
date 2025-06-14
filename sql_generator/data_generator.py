# sql_generator/data_generator.py
import random
import string
from datetime import datetime, timedelta
from .utils import parse_data_type

class DataGenerator:
    """Generates random test data based on column data type specifications."""
    
    @staticmethod
    def generate_value(full_data_type: str) -> str:
        """
        Generate a random value based on the full SQL data type specification.
        
        Args:
            full_data_type: Full SQL data type (e.g., 'CHAR(2) NOT NULL', 'VARCHAR(50)', 'DECIMAL(5, 3)').
        
        Returns:
            A string representation of the generated value.
        """
        try:
            base_type, length, precision, _ = parse_data_type(full_data_type)
        except ValueError:
            return "'Unknown'"
        
        if base_type in ('CHAR', 'VARCHAR'):
            gen_length = length if length else random.randint(5, 20)
            value = ''.join(random.choices(string.ascii_letters, k=gen_length))
            return f"'{value}'"
        elif base_type in ('INT', 'INTEGER'):
            return str(random.randint(1, 1000))
        elif base_type == 'BIGINT':
            return str(random.randint(1, 1000000000))  # Up to 1 billion
        elif base_type == 'BIT':
            return str(random.randint(0, 1))  # 0 or 1
        elif base_type in ('DECIMAL', 'FLOAT', 'DOUBLE'):
            if base_type == 'DECIMAL' and length:
                # For DECIMAL(M) or DECIMAL(M,D), M is total digits, D is max decimal places
                decimal_places = precision if precision is not None else 0  # Default to 0 if precision is None
                integer_digits = length - decimal_places  # Digits before decimal
                if integer_digits < 0:
                    return "'0.0'"  # Invalid DECIMAL specification
                # Generate integer part (up to integer_digits)
                max_integer = 10 ** integer_digits - 1 if integer_digits > 0 else 0
                integer_part = random.randint(0, max_integer)
                if decimal_places == 0:
                    return str(integer_part)
                # Generate decimal part (0 to D digits)
                decimal_digits = random.randint(0, decimal_places)  # Random number of decimal places
                if decimal_digits == 0:
                    return str(integer_part)
                decimal_part = ''.join(str(random.randint(0, 9)) for _ in range(decimal_digits))
                value = f"{integer_part}.{decimal_part}"
                return str(value)
            elif base_type == 'DECIMAL':
                # Handle DECIMAL without length as DECIMAL(10,0)
                max_integer = 10 ** 10 - 1  # Up to 10 digits
                return str(random.randint(0, max_integer))
            else:
                # Fallback for FLOAT, DOUBLE
                scale = precision if precision else 2
                value = round(random.uniform(0, 1000), scale)
                return str(value)
        elif base_type in ('DATE'):
            start_date = datetime(2020, 1, 1)
            days_offset = random.randint(0, 365 * 5)
            random_date = start_date + timedelta(days=days_offset)
            return f"'{random_date.strftime('%Y-%m-%d')}'"
        elif base_type in ('DATETIME'):
            start_date = datetime.now() - timedelta(days=(365 * 5))
            days_offset = random.randint(0, 365 * 5)
            random_date = start_date + timedelta(days=days_offset)
            return f"'{random_date.strftime('%Y-%m-%d')}'"
        elif base_type == 'BOOLEAN':
            return random.choice(['TRUE', 'FALSE'])
        else:
            return "'Unknown'"