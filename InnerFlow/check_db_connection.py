# check_db_connection.py

import os
import django

# Django settings 모듈을 불러오기 위해 환경 변수 설정
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'InnerFlow.settings')
django.setup()

from django.db import connection

def check_database_connection():
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT 1")
        print("Database connection successful!")
    except Exception as e:
        print("Error connecting to database:", str(e))

if __name__ == "__main__":
    check_database_connection()
