# sql_generator/schema_parser.py
import re
from pathlib import Path
from .exceptions import SchemaError
from .types import Schema

class SchemaParser:
    """Parses SQL schema files to extract table names and column definitions."""
    
    @staticmethod
    def parse_schema(file_path: Path) -> Schema:
        """
        Parse a SQL schema file to extract table name and columns with their full data type specifications.
        
        Args:
            file_path: Path to the schema file.
        
        Returns:
            Tuple of table name and dictionary of column names to full data type strings.
        
        Raises:
            SchemaError: If file is invalid or schema cannot be parsed.
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            print(f"DEBUG: Raw content of {file_path}:\n{content}\n")
            
            # Extract table name
            table_match = re.search(r'CREATE\s+TABLE\s+(\w+)\s*\(', content, re.IGNORECASE)
            if not table_match:
                raise SchemaError(f"No valid CREATE TABLE statement found in {file_path}")
            table_name = table_match.group(1)
            print(f"DEBUG: Extracted table name: {table_name}")
            
            # Extract column section, accounting for nested parentheses
            column_content = ""
            paren_count = 0
            in_columns = False
            i = 0
            while i < len(content):
                if content[i] == '(' and not in_columns:
                    in_columns = True
                    i += 1
                    continue
                if in_columns:
                    if content[i] == '(':
                        paren_count += 1
                    elif content[i] == ')':
                        if paren_count == 0:
                            break
                        paren_count -= 1
                    column_content += content[i]
                i += 1
            column_content = column_content.strip()
            print(f"DEBUG: Extracted column content:\n{column_content}\n")
            
            if not column_content:
                raise SchemaError(f"No columns found in {file_path}")
            
            # Split column definitions by commas, respecting nested parentheses
            columns_list = []
            current = ''
            paren_count = 0
            for char in column_content:
                if char == '(':
                    paren_count += 1
                elif char == ')':
                    paren_count -= 1
                elif char == ',' and paren_count == 0:
                    if current.strip():
                        columns_list.append(current.strip())
                    current = ''
                    continue
                current += char
            if current.strip():
                columns_list.append(current.strip())
            print(f"DEBUG: Split column definitions: {columns_list}\n")
            
            columns = {}
            for column_def in columns_list:
                column_def = column_def.strip()
                print(f"DEBUG: Processing column definition: {column_def}")
                if not column_def or column_def.upper().startswith(('PRIMARY', 'FOREIGN', 'CONSTRAINT')):
                    print(f"DEBUG: Skipping non-column definition: {column_def}")
                    continue
                # Parse column name and data type
                parts = re.match(r'(\w+)\s+(.+)', column_def, re.IGNORECASE)
                if parts:
                    column_name = parts.group(1).strip('`')
                    data_type_full = parts.group(2).strip().upper()
                    columns[column_name] = data_type_full
                    print(f"DEBUG: Parsed column: {column_name} = {data_type_full}")
                else:
                    print(f"DEBUG: Failed to parse column definition: {column_def}")
            
            if not columns:
                raise SchemaError(f"No valid columns parsed in {file_path}")
            print(f"DEBUG: Final parsed columns: {columns}\n")
            
            return table_name, columns
        except Exception as e:
            raise SchemaError(f"Error parsing schema {file_path}: {str(e)}")