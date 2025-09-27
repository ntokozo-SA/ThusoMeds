#!/usr/bin/env python3
"""
Database migration script to add pregnancy-specific fields to the PatientIntake table.
This script should be run after updating the models.py file with pregnancy fields.
"""

import sqlite3
from datetime import datetime

def migrate_database():
    """Add pregnancy-specific columns to the PatientIntake table"""
    
    # Connect to the database
    conn = sqlite3.connect('hospital.db')
    cursor = conn.cursor()
    
    try:
        # Check if the table exists
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='patient_intake'")
        if not cursor.fetchone():
            print("PatientIntake table does not exist. Please run the main app first to create tables.")
            return
        
        # List of new pregnancy-specific columns to add
        pregnancy_columns = [
            ("is_pregnant", "BOOLEAN DEFAULT 1"),  # All patients are pregnant women
            ("pregnancy_week", "INTEGER"),
            ("trimester", "VARCHAR(20)"),
            ("due_date", "DATE"),
            ("pregnancy_complications", "TEXT"),
            ("previous_pregnancies", "INTEGER DEFAULT 0"),
            ("blood_type", "VARCHAR(10)"),
            ("last_menstrual_period", "DATE")
        ]
        
        # Check existing columns
        cursor.execute("PRAGMA table_info(patient_intake)")
        existing_columns = [row[1] for row in cursor.fetchall()]
        
        # Add new columns that don't exist
        for column_name, column_type in pregnancy_columns:
            if column_name not in existing_columns:
                try:
                    alter_sql = f"ALTER TABLE patient_intake ADD COLUMN {column_name} {column_type}"
                    cursor.execute(alter_sql)
                    print(f"✅ Added column: {column_name}")
                except sqlite3.Error as e:
                    print(f"❌ Error adding column {column_name}: {e}")
            else:
                print(f"ℹ️  Column {column_name} already exists")
        
        # Commit changes
        conn.commit()
        print("🎉 Database migration completed successfully!")
        
        # Show final table structure
        print("\n📋 Final table structure:")
        cursor.execute("PRAGMA table_info(patient_intake)")
        columns = cursor.fetchall()
        for col in columns:
            print(f"  - {col[1]} ({col[2]})")
            
    except sqlite3.Error as e:
        print(f"❌ Database error: {e}")
        conn.rollback()
    finally:
        conn.close()

def backup_database():
    """Create a backup of the database before migration"""
    import shutil
    from datetime import datetime
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_filename = f"hospital_backup_{timestamp}.db"
    
    try:
        shutil.copy2('hospital.db', backup_filename)
        print(f"💾 Database backed up to: {backup_filename}")
        return backup_filename
    except Exception as e:
        print(f"❌ Backup failed: {e}")
        return None

if __name__ == "__main__":
    print("🤱 MamaCare Database Migration - Adding Pregnancy Fields")
    print("=" * 60)
    
    # Create backup first
    backup_file = backup_database()
    
    if backup_file:
        print(f"\n🔄 Starting migration...")
        migrate_database()
    else:
        print("❌ Migration aborted - backup failed")
