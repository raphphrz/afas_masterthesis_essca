import sqlite3
import pandas as pd

class DatabaseExporter:
    def __init__(self, db_path):
        self.db_path = db_path

    def connect(self):
        """Establish a connection to the SQLite database."""
        try:
            self.conn = sqlite3.connect(self.db_path)
            self.cursor = self.conn.cursor()
        except sqlite3.Error as e:
            print(f"Error connecting to database: {e}")
            self.conn = None

    def close(self):
        """Close the database connection."""
        if self.conn:
            self.conn.close()

def export_to_excel(db_path, table_name, output_file):
    """
    Export a specific table from the SQLite database to an Excel file.

    Args:
        db_path (str): Path to the SQLite database file.
        table_name (str): Name of the table to export.
        output_file (str): Path to the output Excel file.
    """
    exporter = DatabaseExporter(db_path)
    exporter.connect()

    if exporter.conn:
        try:
            # Read the table into a pandas DataFrame
            query = f"SELECT * FROM {table_name}"
            df = pd.read_sql_query(query, exporter.conn)

            # Export the DataFrame to an Excel file
            df.to_excel(output_file, index=False)
            print(f"Table '{table_name}' exported successfully to '{output_file}'.")
        except Exception as e:
            print(f"Error exporting table: {e}")
        finally:
            exporter.close()
    else:
        print("Failed to connect to the database.")


if __name__ == "__main__":
    db_path = "../data/portfolio_data.db"
    table_name = "portfolios"
    output_file = "portfolios_export.xlsx"
    export_to_excel(db_path, table_name, output_file)