import sys
import os

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)

from src.utils.db_connector import get_connection

def execute_sql_file(filepath):
    conn = get_connection()
    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            sql = file.read()
        with conn.cursor() as cursor:
            cursor.execute("SET FOREIGN_KEY_CHECKS=0;")
            for statement in sql.split(';'):
                stmt = statement.strip()
                if stmt:
                    cursor.execute(stmt)
            cursor.execute("SET FOREIGN_KEY_CHECKS=1;")
        conn.commit()
        print("Script SQL ejecutado correctamente")
    except Exception as e:
        print(f"Error ejecutando script SQL: {e}")
        conn.rollback()
        raise
    finally:
        conn.close()

if __name__ == "__main__":
    sql_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'schema.sql'))  # Cambiado aquí
    execute_sql_file(sql_path)
