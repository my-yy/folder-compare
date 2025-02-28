from peewee import *
import datetime
from playhouse.migrate import SqliteMigrator, migrate

db = SqliteDatabase('my_database.db')


class BaseModel(Model):
    class Meta:
        database = db


class Folder(BaseModel):
    name = CharField(default="")
    custom_name = CharField(default="")  # 废弃
    desc = CharField(default="")
    path = TextField(default="")
    created_date = DateTimeField(default=datetime.datetime.now)
    is_gt = BooleanField(default=False)  # 废弃
    content_type = CharField(default="wav")  # wav、ckpt


class Collection(BaseModel):
    name = CharField(unique=True)
    desc = TextField(default="")
    created_date = DateTimeField(default=datetime.datetime.now)
    raw_folders = TextField(default="")
    folder_order = TextField(default="")
    content_type = CharField(default="wav")  # wav、ckpt


class FolderCollection(BaseModel):
    folder = ForeignKeyField(Folder, backref='collections')
    collection = ForeignKeyField(Collection, backref='folders')


def do_connect():
    db.connect()
    db.create_tables([Folder, Collection, FolderCollection])


# 执行迁移
if __name__ == "__main__":
    db.connect()
    pass
    db.close()
