from peewee import *
import datetime
from playhouse.migrate import SqliteMigrator, migrate

db = SqliteDatabase('my_database.db')


class BaseModel(Model):
    class Meta:
        database = db


class Folder(BaseModel):
    name = CharField(default="")
    custom_name = CharField(default="")
    desc = CharField(default="")
    path = TextField(default="")
    created_date = DateTimeField(default=datetime.datetime.now)
    is_gt = BooleanField(default=False)


class Collection(BaseModel):
    name = CharField(unique=True)
    desc = TextField(default="")
    created_date = DateTimeField(default=datetime.datetime.now)
    raw_folders = TextField(default="")
    folder_order = TextField(default="")



class FolderCollection(BaseModel):
    folder = ForeignKeyField(Folder, backref='collections')
    collection = ForeignKeyField(Collection, backref='folders')


def mig1():
    # 创建迁移器
    migrator = SqliteMigrator(db)

    # 定义迁移操作
    folder_order_field = TextField(default="")
    migration = migrator.add_column('collection', 'folder_order', folder_order_field)

    # 执行迁移
    migrate(migration)


db.connect()
db.create_tables([Folder, Collection, FolderCollection])

# 关闭数据库连接
# db.close()
