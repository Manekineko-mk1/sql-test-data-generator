# sql_generator/sql_generator.py
from pathlib import Path
from typing import List, Tuple
import logging
from .schema_parser import SchemaParser
from .data_generator import DataGenerator
from .exceptions import SchemaError
from .types import Schema, SharedValues, InsertStatements
from .utils import parse_data_type

class SQLGenerator:
    """Generates SQL INSERT statements based on schema and shared fields."""
    
    def __init__(self, schema_dir: str = 'schema', output_dir: str = 'output', num_records: int = 5):
        self.schema_dir = Path(schema_dir)
        self.output_dir = Path(output_dir)
        self.num_records = num_records
        self.output_dir.mkdir(exist_ok=True)
    
    def read_shared_fields(self, shared_fields_file: Path) -> List[str]:
        """Read shared fields from a text file (comma-separated per line)."""
        try:
            with open(shared_fields_file, 'r') as f:
                lines = f.readlines()
            shared_fields = []
            for line in lines:
                fields = [field.strip() for field in line.split(',') if field.strip()]
                shared_fields.extend(fields)
            return shared_fields
        except Exception as e:
            raise SchemaError(f"Error reading shared fields file {shared_fields_file}: {str(e)}")
    
    def validate_shared_fields(self, shared_fields: List[str], schemas: List[Schema]) -> None:
        """Validate that shared fields exist in all schemas and have consistent data types."""
        for field in shared_fields:
            # Check if field exists in all schemas
            for table_name, columns in schemas:
                if field not in columns:
                    raise SchemaError(f"Shared field '{field}' not found in table '{table_name}'")
            
            # Check if data types are consistent across schemas
            data_types = []
            for table_name, columns in schemas:
                data_type = columns[field]
                try:
                    parsed_type = parse_data_type(data_type)
                except ValueError as e:
                    raise SchemaError(f"Invalid data type for field '{field}' in table '{table_name}': {str(e)}")
                data_types.append((table_name, data_type, parsed_type))
            
            # Compare data types and null status
            base_type, length, precision, not_null = data_types[0][2]  # Reference type from first schema
            for table_name, raw_type, (other_base_type, other_length, other_precision, other_not_null) in data_types[1:]:
                if (base_type != other_base_type or
                    length != other_length or
                    precision != other_precision or
                    not_null != other_not_null):
                    raise SchemaError(
                        f"Shared field '{field}' has inconsistent data types: "
                        f"'{data_types[0][1]}' in '{data_types[0][0]}' vs. "
                        f"'{raw_type}' in '{table_name}'"
                    )
    
    def generate_shared_values(self, shared_fields: List[str], schemas: List[Schema]) -> SharedValues:
        """Generate consistent values for shared fields across tables."""
        shared_values = []
        for _ in range(self.num_records):
            record_values = {}
            for field in shared_fields:
                data_type = next(columns[field] for _, columns in schemas if field in columns)
                record_values[field] = DataGenerator.generate_value(data_type)
            shared_values.append(record_values)
        return shared_values
    
    def generate_insert_statements(self) -> InsertStatements:
        """Generate INSERT statements for all schemas, grouped by table."""
        schemas = []
        shared_fields = []
        
        # Parse all schema files
        schema_files = list(self.schema_dir.glob('*.sql'))
        if not schema_files:
            raise SchemaError(f"No schema files found in {self.schema_dir}")
        
        for schema_file in schema_files:
            schemas.append(SchemaParser.parse_schema(schema_file))
        logging.debug(f"All parsed schemas: {schemas}\n")
        
        # Read shared fields if provided
        shared_fields_file = self.schema_dir / 'shared_fields.txt'
        if shared_fields_file.exists():
            shared_fields = self.read_shared_fields(shared_fields_file)
            self.validate_shared_fields(shared_fields, schemas)
        
        # Generate shared values for consistent data
        shared_values = self.generate_shared_values(shared_fields, schemas) if shared_fields else None
        logging.debug(f"Shared values: {shared_values}\n")
        
        # Generate INSERT statements, grouped by table
        insert_statements = []
        for table_name, columns in schemas:
            table_statements = []
            for record_idx in range(self.num_records):
                columns_list = list(columns.keys())
                values = []
                for col in columns_list:
                    if col in shared_fields and shared_values:
                        value = shared_values[record_idx][col]
                    else:
                        value = DataGenerator.generate_value(columns[col])
                    values.append(value)
                insert_sql = f"INSERT INTO {table_name} ({', '.join(columns_list)}) VALUES ({', '.join(values)});"
                table_statements.append(insert_sql)
            insert_statements.append((table_name, table_statements))
        
        return insert_statements
    
    def run(self) -> None:
        """Generate and output INSERT statements."""
        try:
            insert_statements = self.generate_insert_statements()
            
            # Print to console
            for table_name, statements in insert_statements:
                for stmt in statements:
                    logging.info(stmt)
                logging.info("****")
            
            # Write to output file
            output_file = self.output_dir / 'output.sql'
            with open(output_file, 'w') as f:
                for table_name, statements in insert_statements:
                    for stmt in statements:
                        f.write(stmt + '\n')
                    f.write("****\n")
            logging.info(f"\nGenerated INSERT statements written to {output_file}")
        
        except SchemaError as e:
            logging.error(f"Error: {str(e)}")
            exit(1)
        except Exception as e:
            logging.error(f"Unexpected error: {str(e)}")
            exit(1)