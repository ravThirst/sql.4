from sqlalchemy.orm import sessionmaker
from tabulate import tabulate
from models import *
import json


class DbHandler:
    def __init__(self, dsn):
        self.__engine = sq.create_engine(dsn)
        self.__create_tables(self.__engine)
        self.__sessionmaker = sessionmaker(bind=self.__engine)
        self.__session = self.__sessionmaker()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.__session.close_all()

    @staticmethod
    def __create_tables(engine) -> None:
        Base.metadata.drop_all(engine)
        Base.metadata.create_all(engine)

    def load_data(self, path: str) -> None:
        with open(path, 'r') as fd:
            data = json.load(fd)
            models = {
                'publisher': Publisher,
                'shop': Shop,
                'book': Book,
                'stock': Stock,
                'sale': Sale,
            }
        for record in data:
            model = models[record.get('model')]
            self.__session.add(model(id=record.get('pk'), **record.get('fields')))
        self.__session.commit()

    def find_sales(self, id_or_name: int or str) -> None:
        select_all = self.__session.query(Book.title, Shop.name, Sale.price, Sale.date_sale)\
                                .join(Publisher).join(Stock).join(Shop).join(Sale)
        if isinstance(id_or_name, int):
            search = select_all.filter(
                Publisher.id == id_or_name).all()
        elif isinstance(id_or_name, str):
            search = select_all.filter(
                Publisher.name == id_or_name).all()
        else:
            raise TypeError("Please provide string or integer")

        headers = ('Book', 'Publisher', 'Price', 'Date')
        print(tabulate(search, headers))
