# SQL Test Data Generator

This Python tool generates SQL `INSERT` statements with test data based on SQL schema files and optional shared fields. It ensures consistent data for shared fields across tables, making it ideal for generating test data for relational databases with cross-referenced tables. The project uses a modular design for maintainability and extensibility.

## Features
- Parses SQL `CREATE TABLE` statements from `.sql` files in the `schema/` directory.
- Supports shared fields via `schema/shared_fields.txt` (comma-separated fields) to ensure identical values across tables.
- Validates shared fields exist in all specified schemas.
- Generates random test data adhering to schema specifications (e.g., `CHAR(2)` generates 2-character strings).
- Outputs `INSERT` statements to the console and `output/output.sql`, with table statements separated by `****`.
- Configurable number of records per table via `--num_records` (default: 5).
- Debug mode via `--debug` flag to display detailed parsing and generation logs.
- Modular architecture with separate modules for schema parsing, data generation, and SQL generation.

## Requirements
- Python 3.8+
- No external dependencies required.

## Directory Structure
```
sql-test-data-generator/
├── sql_generator/
│   ├── init.py
│   ├── schema_parser.py      # Schema parsing logic
│   ├── data_generator.py     # Random test data generation
│   ├── sql_generator.py      # INSERT statement generation
│   ├── exceptions.py         # Custom exceptions
│   ├── types.py              # Shared type hints
├── schema/
│   ├── test_schema_1.sql     # Example schema file
│   ├── test_schema_2.sql     # Example schema file
│   └── shared_fields.txt     # Optional: Comma-separated shared fields
├── output/
│   └── output.sql            # Generated INSERT statements
├── generate_sql_inserts.py   # Main script
├── README.md                 # This file
├── requirements.txt          # Empty (no dependencies)
└── pyproject.toml            # Optional: Package metadata
```

## Schema File Format
Schema files must contain valid SQL `CREATE TABLE` statements. 

Example (`schema/test_schema_1.sql`):
```sql
CREATE TABLE test_schema_1 (
    schl_id INT,
    TYP_VVCF CHAR(2) NOT NULL,
    weight INT NOT NULL,
    created_date DATE,
    amount DECIMAL(10,2)
);
```

Example (`schema/test_schema_2.sql`):
```sql
CREATE TABLE test_schema_2 (
    ref_id INT,
    TYP_VVCF CHAR(2) NOT NULL,
    weight INT NOT NULL,
    status BOOLEAN,
    code VARCHAR(10)
);
```

## Shared Fields File Format
The `shared_fields.txt` file lists comma-separated field names (one or more lines). 

Example (`schema/shared_fields.txt`):
```
TYP_VVCF, weight
```
Shared fields ensure identical values across tables (e.g., `TYP_VVCF='XI'`, `weight=810` in both `test_schema_1` and `test_schema_2` for the same row).



## Usage
- Place your schema files (`.sql`) in the schema directory.
- Optionally, create a `shared_fields.txt` file in the schema directory listing shared fields.
- Run the script:
```bash
    python generate_sql_inserts.py --num_records 5
```
- The `--num_records` argument is optional (defaults to 5 records per table).
- `--debug`: Enable detailed debug logging (optional).
- The script will:
    - Parse schema files and validate shared fields (if provided).
    - Generate `INSERT` statements with random test data adhering to schema specifications.
    - Ensure shared fields have identical values across tables.
    - Print statements to the console.
    - Save statements to output/output.sql, with table statements separated by `****`.

## Example Output
For `test_schema_1.sql` and `test_schema_2.sql` with shared fields `TYP_VVCF` and `weight`, and `--num_records 3`:

```sql
INSERT INTO test_schema_1 (schl_id, TYP_VVCF, weight, created_date, amount) VALUES (751, 'XI', 810, '2023-03-14', 171.92);
INSERT INTO test_schema_1 (schl_id, TYP_VVCF, weight, created_date, amount) VALUES (244, 'FX', 56, '2020-02-28', 385.41);
INSERT INTO test_schema_1 (schl_id, TYP_VVCF, weight, created_date, amount) VALUES (213, 'gp', 277, '2020-08-22', 92.96);
****
INSERT INTO test_schema_2 (ref_id, TYP_VVCF, weight, status, code) VALUES (100, 'XI', 810, FALSE, 'ZYdnXNpnGs');
INSERT INTO test_schema_2 (ref_id, TYP_VVCF, weight, status, code) VALUES (308, 'FX', 56, TRUE, 'UEtPdQSMvE');
INSERT INTO test_schema_2 (ref_id, TYP_VVCF, weight, status, code) VALUES (374, 'gp', 277, TRUE, 'vwfyhZNTsq');
****
```
With `--debug`, additional logs show schema parsing and shared values:
```
DEBUG: Raw content of schema\test_schema_1.sql: ...
DEBUG: Shared values: [{'TYP_VVCF': "'XI'", 'weight': '810'}, ...]
```

## Error Handling
- Exits with an error message if:
    - Schema files are invalid or missing.
    - Shared fields are not found in all tables.
    - Other parsing or file issues occur.
- Debug logs (with `--debug`) provide detailed diagnostics.

## Customization
- Adjust `--num_records` to control the number of records.
- Modify `sql_generator/data_generator.py` to support additional SQL data types or custom data rules (e.g., specific ranges for `INT`).
- Change schema or output directory paths in `sql_generator/sql_generator.py` if needed.



## Supported Data Types
- `CHAR(n)`, `VARCHAR(n)`: Generates strings of length `n` (or random length for `VARCHAR` if unspecified).
- `INT`, `INTEGER`: Random integers between 1 and 1000.
- `DECIMAL(m,n)`, `FLOAT`, `DOUBLE`: Random decimals with specified precision (default: 2 decimal places).
- `DATE`, `DATETIME`: Random dates between 2020 and 2025.
- `BOOLEAN`: Random `TRUE` or `FALSE`.

## Limitations
- Assumes well-formed `CREATE TABLE` statements; complex constraints (e.g., nested subqueries) may require additional parsing logic.
- Limited data type support (extendable in `data_generator.py`).
- Shared fields must have compatible data types across tables (uses the first encountered type).



## Future Improvements
- Add support for more SQL data types (e.g., `TIMESTAMP`, `JSON`).
- Implement custom value ranges or predefined lists for fields.
- Handle foreign key constraints explicitly.
- Support separate output files per table.
- Add unit tests for modular components.



## Setup
- Create the directory structure as shown above.
- Add schema files and (optionally) `shared_fields.txt` to `schema/`.
- Run the script as described in Usage.

(Optional) If using `pyproject.toml`, install as a package:
```bash
pip install .
```
Then run:
```bash
generate-sql-inserts --num_records 3
```

## License
- MIT License


