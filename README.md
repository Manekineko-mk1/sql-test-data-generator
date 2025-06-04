# SQL Test Data Generator

This Python script generates SQL `INSERT` statements with test data based on provided SQL schema files and optional shared fields. It ensures consistent data for shared fields across tables, making it ideal for generating test data for relational databases with cross-referenced tables.

## Features
- Parses SQL `CREATE TABLE` statements from `.sql` files in the `schema` directory.
- Reads shared fields from a `shared_fields.txt` file (comma-separated fields per line).
- Validates that shared fields exist in all specified schemas.
- Generates random test data strictly adhering to schema specifications (e.g., `CHAR(2)` generates 2-character strings).
- Ensures identical values for shared fields across tables to support cross-referencing.
- Outputs `INSERT` statements to the console and to `output/output.sql`, with statements for different tables separated by `****`.
- Configurable number of records per table via a command-line argument (default: 5).

## Requirements
- Python 3.8+
- No external dependencies required.

## Directory Structure
```
sql-test-data-generator/
├── schema/
│   ├── SCHL_MENSUEL.sql          # Example schema file
│   ├── REFERENCE_MENSUEL.sql     # Example schema file
│   └── shared_fields.txt         # Optional: Comma-separated shared fields
├── output/
│   └── output.sql                # Generated INSERT statements
├── generate_sql_inserts.py       # Main script
├── README.md                     # This file
└── requirements.txt              # Empty (no dependencies)
```


## Schema File Format
Schema files should contain valid SQL `CREATE TABLE` statements. Example (`schema/SCHL_MENSUEL.sql`):
```sql
CREATE TABLE SCHL_MENSUEL (
    id INT,
    TYP_VVCF CHAR(2) NOT NULL,
    created_date DATE,
    amount DECIMAL(10,2)
);
```

## Shared Fields File Format
The shared_fields.txt file should list comma-separated field names (one or more lines). 

Example:
```
id,TYP_VVCF
```

## Usage
- Place your schema files (`.sql`) in the schema directory.
- Optionally, create a `shared_fields.txt` file in the schema directory listing shared fields.
- Run the script:
```bash
    python generate_sql_inserts.py --num_records 5
```
- The `--num_records` argument is optional (defaults to 5 records per table).
- The script will:
    - Parse schema files and validate shared fields (if provided).
    - Generate INSERT statements with random test data adhering to schema specifications.
    - Ensure shared fields have identical values across tables.
    - Print statements to the console.
    - Save statements to output/output.sql, with table statements separated by `****`.

## Example Output
For schemas `SCHL_MENSUEL` and `REFERENCE_MENSUEL` with shared fields `id` and `TYP_VVCF`:
```sql
INSERT INTO SCHL_MENSUEL (id, TYP_VVCF, created_date, amount) VALUES (123, 'AB', '2022-07-15', 456.78);
INSERT INTO SCHL_MENSUEL (id, TYP_VVCF, created_date, amount) VALUES (456, 'XY', '2021-03-22', 789.12);
****
INSERT INTO REFERENCE_MENSUEL (id, TYP_VVCF, status) VALUES (123, 'AB', TRUE);
INSERT INTO REFERENCE_MENSUEL (id, TYP_VVCF, status) VALUES (456, 'XY', FALSE);
****
```

## Error Handling
- Exits with an error message if:
    - Schema files are invalid or missing.
    - Shared fields are not found in all tables.
    - Other parsing or file issues occur.
- Provides clear error messages for debugging.

## Customization
- Modify the num_records parameter via the --num_records command-line argument.
- Extend DataGenerator.generate_value in generate_sql_inserts.py to support additional SQL data types or custom data generation rules.
- Adjust the schema or output directory paths in the script if needed.

## Supported Data Types
- CHAR(n), VARCHAR(n): Generates strings of length n (or random length for VARCHAR if unspecified).
- INT, INTEGER: Random integers between 1 and 1000.
- DECIMAL(m,n), FLOAT, DOUBLE: Random decimals with specified precision (default: 2 decimal places).
- DATE, DATETIME: Random dates between 2020 and 2025.
- BOOLEAN: Random TRUE or FALSE.

## Limitations
- Basic schema parsing; assumes well-formed CREATE TABLE statements without complex constraints.
- Limited set of supported SQL data types (extendable in DataGenerator).
- Assumes shared fields have compatible data types across tables (uses the first encountered type).

## Future Improvements
- Support additional SQL data types (e.g., TIMESTAMP, BLOB).
- Add custom data generation rules (e.g., specific ranges for INT).
- Handle foreign key constraints explicitly.
- Allow separate output files per table.

## Setup
- Clone the repository:
```bash
git clone https://github.com/your-username/sql-test-data-generator.git
```
- Create schema files and (optionally) shared_fields.txt in the schema directory.
- Run the script as described in the Usage section.

## License
- MIT License


