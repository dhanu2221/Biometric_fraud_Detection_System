#!/usr/bin/env python3
"""
Direct Chroma database query script - bypasses SQL Tools extension issues
Usage:
  python query_chroma.py "SELECT * FROM collections;"
  python query_chroma.py < query.sql
"""
import sqlite3
import sys
from pathlib import Path

def query_chroma(sql_query):
    """Execute SQL query directly on Chroma SQLite database"""
    db_path = Path(__file__).parent / "chroma_store" / "chroma.sqlite3"
    
    if not db_path.exists():
        print(f"Error: Database not found at {db_path}")
        sys.exit(1)
    
    try:
        conn = sqlite3.connect(str(db_path))
        conn.row_factory = sqlite3.Row  # Return rows as dictionaries
        cursor = conn.cursor()
        
        cursor.execute(sql_query)
        
        # Fetch results
        rows = cursor.fetchall()
        
        # Print results
        if rows:
            # Get column names
            columns = [description[0] for description in cursor.description]
            
            # Calculate column widths
            col_widths = [len(col) for col in columns]
            for row in rows:
                for i, val in enumerate(row):
                    col_widths[i] = max(col_widths[i], len(str(val)) if val else 4)
            
            # Print header
            header = " | ".join(col.ljust(col_widths[i]) for i, col in enumerate(columns))
            print("\n" + header)
            print("-" * len(header))
            
            # Print rows
            for row in rows:
                print(" | ".join(str(val).ljust(col_widths[i]) if val else "NULL".ljust(col_widths[i]) for i, val in enumerate(row)))
            
            print(f"\n✓ {len(rows)} row(s) returned\n")
        else:
            print("✓ Query executed. No results found.\n")
        
        conn.close()
        
    except sqlite3.Error as e:
        print(f"❌ Database error: {e}\n")
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        # Read from stdin if no args provided
        print("Enter SQL query (press Ctrl+D when done):")
        query = sys.stdin.read().strip()
        if not query:
            query = "SELECT * FROM collections;"
    else:
        query = " ".join(sys.argv[1:])
    
    print(f"📊 Executing: {query}")
    query_chroma(query)
