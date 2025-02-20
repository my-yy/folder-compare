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


def mig1():
    # 创建迁移器
    migrator = SqliteMigrator(db)

    # 定义迁移操作
    folder_order_field = TextField(default="")
    migration = migrator.add_column('collection', 'folder_order', folder_order_field)

    # 执行迁移
    migrate(migration)


# 定义迁移操作
def add_content_type_column():
    # 创建迁移器
    migrator = SqliteMigrator(db)

    migrate(
        migrator.add_column('collection', 'content_type', CharField(default="wav")),
    )

    migrate(
        migrator.add_column('folder', 'content_type', CharField(default="wav")),
    )


def do_connect():
    db.connect()
    db.create_tables([Folder, Collection, FolderCollection])


def mig_add_folder_order(collection_id):
    import json

    collection = Collection.get(Collection.id == collection_id)

    try:
        assert len(collection.folder_order) > 0
        json.loads(collection.folder_order)
        return
    except:
        pass

    folder_list = list((Folder.select()
                        .join(FolderCollection)
                        .join(Collection)
                        .where(Collection.id == collection_id)))

    folder_list = [i.id for i in folder_list]
    collection.folder_order = json.dumps(folder_list)
    collection.save()
    print("update:", collection.name, collection.folder_order)


def mig_all():
    the_list = Collection.select().order_by(Collection.created_date)
    for col in the_list:
        mig_add_folder_order(col.id)


# 执行迁移
if __name__ == "__main__":
    db.connect()
    # add_content_type_column()
    db.close()
