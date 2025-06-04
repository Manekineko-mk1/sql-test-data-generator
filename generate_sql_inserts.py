# generate_sql_inserts.py
import argparse
import logging
from sql_generator import SQLGenerator

def main():
    """Main function to parse arguments and run the SQL generator."""
    parser = argparse.ArgumentParser(description='Generate SQL INSERT statements from schema files.')
    parser.add_argument('--num_records', type=int, default=5, help='Number of records to generate per table (default: 5)')
    parser.add_argument('--debug', action='store_true', help='Enable debug logging')
    args = parser.parse_args()
    
    # Configure logging
    logging.basicConfig(
        level=logging.DEBUG if args.debug else logging.INFO,
        format='%(levelname)s: %(message)s'
    )
    
    generator = SQLGenerator(num_records=args.num_records)
    generator.run()

if __name__ == '__main__':
    main()