#!/usr/bin/python3
"""ddb aschelmy definiton"""

import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from models.base_model import Base
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review
from os import getenv


class DBStorage:
    """DBStorage class for managing storage of hbnb models in a MySQL database"""

    __engine = None
    __session = None

    def __init__(self):
        """Initialize DBStorage instance"""
        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'
                                      .format(os.getenv('HBNB_MYSQL_USER'),
                                              os.getenv('HBNB_MYSQL_PWD'),
                                              os.getenv('HBNB_MYSQL_HOST'),
                                              os.getenv('HBNB_MYSQL_DB')),
                                      pool_pre_ping=True)

        if os.getenv('HBNB_ENV') == 'test':
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """Query all objects from the database"""
        objects = {}
        if cls:
            for obj in self.__session.query(cls).all():
                key = obj.__class__.__name__ + '.' + obj.id
                objects[key] = obj
        else:
            for clss in [State, City, User, Place, Review, Amenity]:
                for obj in self.__session.query(clss).all():
                    key = obj.__class__.__name__ + '.' + obj.id
                    objects[key] = obj
        return objects
    def new(self, obj):
        """Add an object to the current database session"""
        if obj:
            self.__session.add(obj)

    def save(self):
        """Commit all changes to the current database session"""
        self.__session.commit()

    def delete(self, obj=None):
        """Delete an object from the current database session"""
        if obj:
            self.__session.delete(obj)

    def reload(self):
        """Create all tables in the database and create the current database session"""
        Base.metadata.create_all(self.__engine)
        Sess = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(Sess)
        self.__session = Session()

    def close(self):
        """private session attribute (self.__session)"""
        self.__session.remove()
