#!/usr/bin/env python3
"""
Database migration script to add new AI classification columns
"""

import sqlite3
import os
from pathlib import Path

def migrate_database():
    """Add new columns to the patient_intake table"""
    
    db_path = Path(__file__).parent / "hospital.db"
    
    if not db_path.exists():
        print("Database doesn't exist yet. It will be created when you start the Flask app.")
        return
    
    print(f"Migrating database: {db_path}")
    
    try:
        conn = sqlite3.connect(str(db_path))
        cursor = conn.cursor()
        
        # Check if new columns already exist
        cursor.execute("PRAGMA table_info(patient_intake)")
        columns = [column[1] for column in cursor.fetchall()]
        
        print(f"Existing columns: {columns}")
        
        # Add new columns if they don't exist
        new_columns = [
            ("severity_level", "VARCHAR(20)"),
            ("ticket_number", "VARCHAR(10)"),
            ("color_code", "VARCHAR(1)"),
            ("ai_analysis", "TEXT")
        ]
        
        for column_name, column_type in new_columns:
            if column_name not in columns:
                print(f"Adding column: {column_name}")
                cursor.execute(f"ALTER TABLE patient_intake ADD COLUMN {column_name} {column_type}")
            else:
                print(f"Column {column_name} already exists")
        
        conn.commit()
        print("Migration completed successfully!")
        
    except sqlite3.Error as e:
        print(f"Database error: {e}")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    migrate_database()
