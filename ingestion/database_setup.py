from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError

def get_database_connection():
    # Define the database connection string for Windows Authentication
    server = 'CEI3233'  # Replace with your SQL Server instance name
    database = 'LLM_Assignment_DB'
    driver = 'ODBC Driver 17 for SQL Server'
    connection_string = f"mssql+pyodbc://@{server}/{database}?driver={driver}&Trusted_Connection=yes"

    # Create the SQLAlchemy engine
    engine = create_engine(connection_string)
    return engine

def test_connection(engine):
    try:
        # Try executing a simple query to test the connection
        with engine.connect() as connection:
            result = connection.execute(text("SELECT 1"))
            # If successful, this will return a result
            print("Database connection is successful.")
    except SQLAlchemyError as e:
        print(f"Error: {e}")

# Example usage
if __name__ == '__main__':
    engine = get_database_connection()
    test_connection(engine)
