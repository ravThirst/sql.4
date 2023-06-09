import sqlalchemy as sq
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class Publisher(Base):
    __tablename__ = 'publisher'

    id = sq.Column(sq.Integer, primary_key=True)
    name = sq.Column(sq.VARCHAR(100), unique=True)
    book = relationship('Book', back_populates='publisher')

    def __str__(self):
        return f'publisher{self.id} - {self.name}'


class Book(Base):
    __tablename__ = 'book'

    id = sq.Column(sq.Integer, primary_key=True)
    title = sq.Column(sq.VARCHAR(100), nullable=False)
    id_publisher = sq.Column(sq.Integer,
                             sq.ForeignKey('publisher.id'),
                             nullable=False)
    publisher = relationship('Publisher', back_populates='book')
    stock = relationship('Stock', back_populates='book')

    def __str__(self):
        return f'book{self.id} - ({self.title}, {self.id_publisher})'


class Shop(Base):
    __tablename__ = 'shop'

    id = sq.Column(sq.Integer, primary_key=True)
    name = sq.Column(sq.VARCHAR(100), unique=True, nullable=False)
    stock = relationship('Stock', back_populates='shop')


class Stock(Base):
    __tablename__ = 'stock'

    id = sq.Column(sq.Integer, primary_key=True)
    id_book = sq.Column(sq.Integer, sq.ForeignKey('book.id'),
                        nullable=False)
    id_shop = sq.Column(sq.Integer, sq.ForeignKey('shop.id'),
                        nullable=False)
    count = sq.Column(sq.Integer, default=0, nullable=False)
    book = relationship('Book', back_populates='stock')
    shop = relationship('Shop', back_populates='stock')
    sale = relationship('Sale', back_populates='stock')


class Sale(Base):
    __tablename__ = 'sale'

    id = sq.Column(sq.Integer, primary_key=True)
    price = sq.Column(sq.Float, nullable=False)
    date_sale = sq.Column(sq.TIMESTAMP(timezone=False), nullable=False)
    id_stock = sq.Column(sq.Integer, sq.ForeignKey('stock.id'),
                         nullable=False)
    count = sq.Column(sq.Integer, default=0, nullable=False)
    stock = relationship('Stock', back_populates='sale')
