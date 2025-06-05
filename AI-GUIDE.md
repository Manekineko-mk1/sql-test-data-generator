# AI Guide for sql-test-data-generator

## Project Overview
- **Purpose**: Generates random SQL `INSERT` statements for testing database schemas, ensuring consistent values for shared fields across tables.
- **Key Features**:
  - Parses SQL `CREATE TABLE` schemas to extract table names and column definitions.
  - Supports data types: `CHAR(n)`, `VARCHAR(n)`, `INT`, `BIGINT`, `BIT`, `DECIMAL(m,n)`, `FLOAT`, `DOUBLE`, `DATE`, `DATETIME`, `BOOLEAN`.
  - Handles single-line SQL comments (`--`) in schemas.
  - Generates consistent values for shared fields listed in `schema/shared_fields.txt`.
  - Outputs `INSERT` statements to `output/output.sql`.
- **Target Use Case**: Developers and testers creating mock data for SQL databases (e.g., MySQL, PostgreSQL).

## Project Structure
- **`generate_sql_inserts.py`**: Entry point script; runs the generator with options like `--num_records` and `--debug`.
- **`sql_generator/`**:
  - `__init__.py`: Marks the package.
  - `schema_parser.py`: Parses SQL schemas, handles `--` comments.
  - `data_generator.py`: Generates random values for SQL data types.
  - `sql_generator.py`: Coordinates parsing and data generation, writes output.
  - `exceptions.py`: Custom exceptions (e.g., `SchemaError`).
  - `types.py`: Type hints for schemas.
  - `utils.py`: Utility functions for parsing and generating SQL.
- **`schema/`**:
  - `*.sql`: Schema files (e.g., `test_schema_1.sql`).
  - `shared_fields.txt`: Lists shared columns (e.g., `TYP_VVCF,weight`).
- **`output/`**: Created automatically, contains `output.sql` (not tracked).
- **`README.md`**: Project documentation, including setup and supported types.

## AI Roles and Responsibilities
- **Code Suggestions**:
  - Suggest new data type handlers in `data_generator.py` (e.g., `TINYINT`, `BIT(n)`).
  - Propose regex improvements in `schema_parser.py` or `data_generator.py`.
  - Follow PEP 8 style, using descriptive variable names (e.g., `base_type`).
- **Debugging Assistance**:
  - Identify issues in SQL parsing (e.g., handling multi-line comments `/* */`).
  - Suggest fixes for errors like `ValueError: Unsupported data type`.
  - Analyze logs when `--debug` is enabled to pinpoint failures.
- **Documentation**:
  - Help update `README.md` with new features (e.g., new data types).
  - Write or refine docstrings in `schema_parser.py`, `data_generator.py`, etc.
  - Ensure consistency with existing style (e.g., Markdown sections).
- **Testing**:
  - Suggest unit tests for `data_generator.py` (e.g., test `BIGINT` range).
  - Assist with `pytest` setup and test cases for new features.
- **Avoid**:
  - Modifying `schema/*.sql` files directly, as they define test cases.
  - Generating code that alters `shared_fields.txt` without user input.
  - Suggesting changes that break shared field consistency across tables.
  - Minimize unnecessary changes to existing codebase.

## AI Interaction Guidelines
- **Prompts**: Use specific prompts like:
  - "Suggest a regex to parse `BIT(8)` in `data_generator.py`."
  - "Write a unit test for `BIGINT` in `data_generator.py`."
- **Context**: Provide:
  - Relevant code snippets (e.g., `data_generator.py`).
  - Debug logs from `--debug` runs.
  - Schema files (e.g., `test_schema_1.sql`) for context.
- **Feedback**: Report AI suggestions that:
  - Misinterpret SQL syntax or data types.
  - Conflict with shared field logic in `sql_generator.py`.

## Notes
- Tested with [e.g., GitHub Copilot, Cursor; update with your IDE’s AI tool].
- AI may struggle with complex SQL constraints (e.g., `FOREIGN KEY`); verify manually.
- Future enhancements may include multi-line comment support (`/* */`) and more data types.