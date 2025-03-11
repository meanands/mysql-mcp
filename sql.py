import os
from typing import Any, Dict
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.pool import QueuePool
from mcp.server.fastmcp import FastMCP

# Load environment variables
load_dotenv()

mcp = FastMCP('sql')

# Configure SQLAlchemy engine with connection pooling
def create_db_engine(database: str = None):
    """Create a SQLAlchemy engine for the given database."""
    user = os.getenv('MYSQL_USER')
    password = os.getenv('MYSQL_PASSWORD')
    host = os.getenv('MYSQL_HOST', 'localhost')
    db_url = f"mysql+pymysql://{user}:{password}@{host}"
    if database:
        db_url = f"{db_url}/{database}"
    
    return create_engine(
        db_url,
        poolclass=QueuePool,
        pool_size=5,
        max_overflow=10,
        pool_timeout=30,
        pool_recycle=1800  # Recycle connections after 30 minutes
    )

@mcp.tool()
async def execute(database: str, query: str) -> Dict[str, Any]:
    """Execute a SQL query on the specified database.
    
    Args:
        database: Name of the database to query
        query: SQL query to execute
    
    Returns:
        Dictionary containing query results or error message
    """
    try:
        # Create engine for the specified database
        engine = create_db_engine(database)
        
        # Execute query
        with engine.connect() as conn:
            # Start a transaction
            with conn.begin():
                result = conn.execute(text(query))
                if result.returns_rows:
                    # Convert result to list of dicts
                    columns = result.keys()
                    rows = [dict(zip(columns, row)) for row in result.fetchall()]
                    return {'results': rows}
                else:
                    # For non-SELECT queries (INSERT, UPDATE, etc.)
                    return {
                        'results': {
                            'rowcount': result.rowcount,
                            'message': 'Query executed successfully'
                        }
                    }
                
    except Exception as e:
        return {
            'error': str(e)
        }
    finally:
        # Dispose of the engine to close all connections in the pool
        if 'engine' in locals():
            engine.dispose()

if __name__ == "__main__":
   mcp.run(transport='stdio')
