"""Initializes the project database."""
import psycopg2

def create_tables():
    conn = psycopg2.connect("dbname=tenderhub user=admin password=secret host=localhost")
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS tenders (
            id SERIAL PRIMARY KEY,
            title TEXT NOT NULL,
            description TEXT,
            closing_date DATE
        )
    """)
    conn.commit()
    conn.close()

if __name__ == "__main__":
    create_tables()
    print("✅ Database setup completed.")
