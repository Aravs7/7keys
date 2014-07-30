__author__ = 'A'

from peewee import *


db = MySQLDatabase('hsync', host="localhost", port=3306, user='root', password='admin')
db.connect()

class MySQLModel(Model):
    """A base model that will use our MySQL database"""
    class Meta:
        database = db
