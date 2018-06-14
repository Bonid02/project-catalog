#!/usr/bin/ python

import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()


class User(Base):
    """Class for User

    Initially this will be used to create user table
    User data will be stored in table name user

    """

    __tablename__ = 'user'
    NAME = Column(String(80), nullable=False)
    EMAIL = Column(String(50), nullable=False)
    PICTURE = Column(String(150))
    ID = Column(Integer, primary_key=True)


class Category(Base):
    """Class for Category

    Initially this will be used to create category table
    Different types of category will be stored in category table

    """

    __tablename__ = 'category'
    NAME = Column(String(80), nullable=False)
    DESCRIPTION = Column(String(250))
    ID = Column(Integer, primary_key=True)

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'id': self.ID,
            'name': self.NAME,
            'description': self.DESCRIPTION
        }


class Item(Base):
    """Class for Item

    Initially this will be used to create item table
    Item data will be stored in table name item

    """

    __tablename__ = 'item'
    NAME = Column(String(80), nullable=False)
    DESCRIPTION = Column(String(250))
    QUANTITY = Column(Integer)
    ID = Column(Integer, primary_key=True)
    IMAGE_URL = Column(String(1500))
    CATEGORY_ID = Column(Integer, ForeignKey('category.ID'))

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'id': self.ID,
            'name': self.NAME,
            'description': self.DESCRIPTION,
            'quantity': self.QUANTITY,
            'image_url': self.IMAGE_URL,
            'category_id': self.CATEGORY_ID
        }

# Create database name inventory.db
engine = create_engine('sqlite:///inventory.db')

Base.metadata.create_all(engine)
