import sys
from peewee import *

db = SqliteDatabase('ooxx.db')

class BaseModel(Model):
    class Meta:
        database = db


class ImageModel(BaseModel):
    author = CharField(null=True)
    url = CharField(null=True)
    number = IntegerField(null=True)
    upvote = IntegerField(null=True)
    downvote = IntegerField(null=True)
    crawl_time = DateTimeField(null=True)


def create_tables():
    db.connect()
    db.create_tables([ImageModel])


def drop_tables():
    db.connect()
    db.drop_tables([ImageModel])


if __name__ == '__main__':
    if sys.argv[1] == 'create':
        create_tables()
    elif sys.argv[1] == 'drop':
        drop_tables()
