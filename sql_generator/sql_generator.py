# sql_generator/sql_generator.py
from pathlib import Path
from typing import List
from .schema_parser import SchemaParser
from .data_generator import DataGenerator
from .exceptions import SchemaError
from .types import Schema, SharedValues, InsertStatements

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
        """Validate that shared fields exist in all schemas."""
        for field in shared_fields:
            for table_name, columns in schemas:
                if field not in columns:
                    raise SchemaError(f"Shared field '{field}' not found in table '{table_name}'")
    
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
        print(f"DEBUG: All parsed schemas: {schemas}\n")
        
        # Read shared fields if provided
        shared_fields_file = self.schema_dir / 'shared_fields.txt'
        if shared_fields_file.exists():
            shared_fields = self.read_shared_fields(shared_fields_file)
            self.validate_shared_fields(shared_fields, schemas)
        
        # Generate shared values for consistent data
        shared_values = self.generate_shared_values(shared_fields, schemas) if shared_fields else None
        print(f"DEBUG: Shared values: {shared_values}\n")
        
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
                    print(stmt)
                print("****")
            
            # Write to output file
            output_file = self.output_dir / 'output.sql'
            with open(output_file, 'w') as f:
                for table_name, statements in insert_statements:
                    for stmt in statements:
                        f.write(stmt + '\n')
                    f.write("****\n")
            print(f"\nGenerated INSERT statements written to {output_file}")
        
        except SchemaError as e:
            print(f"Error: {str(e)}")
            exit(1)
        except Exception as e:
            print(f"Unexpected error: {str(e)}")
            exit(1)