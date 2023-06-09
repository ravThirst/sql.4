import os
from db_handler import DbHandler

PASSWORD = os.getenv('PASSWORD')
DBNAME = os.getenv('DBNAME')
DSN = f'postgresql://postgres:{PASSWORD}@localhost:5432/{DBNAME}'

if __name__ == '__main__':
    with DbHandler(DSN) as db:
        db.load_data('tests_data.json')
        db.find_sales(1)
        print('\n')
        db.find_sales('Manning Publications')
