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


# # 定义迁移操作
# def add_content_type_column():
#     # 创建迁移器
#     migrator = SqliteMigrator(db)
#
#     migrate(
#         migrator.add_column('collection', 'content_type', CharField(default="wav")),
#     )
#
#     migrate(
#         migrator.add_column('folder', 'content_type', CharField(default="wav")),
#     )


# 检查字段是否已经存在
def field_exists(table_name, field_name):
    cursor = db.execute_sql(f"PRAGMA table_info({table_name});")
    columns = cursor.fetchall()
    return any(column[1] == field_name for column in columns)


# 定义迁移操作
def add_content_type_column_safe():
    # 创建迁移器
    migrator = SqliteMigrator(db)

    # 检查 Collection 表中是否已经存在 content_type 字段
    if not field_exists('collection', 'content_type'):
        migrate(
            migrator.add_column('collection', 'content_type', CharField(default="wav")),
        )
        print("Added 'content_type' column to 'collection' table.")

    # 检查 Folder 表中是否已经存在 content_type 字段
    if not field_exists('folder', 'content_type'):
        migrate(
            migrator.add_column('folder', 'content_type', CharField(default="wav")),
        )
        print("Added 'content_type' column to 'folder' table.")


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


def mig_add_folder_order_for_all():
    the_list = Collection.select().order_by(Collection.created_date)
    for col in the_list:
        mig_add_folder_order(col.id)


# 执行迁移
if __name__ == "__main__":
    db.connect()
    add_content_type_column_safe()
    mig_add_folder_order_for_all()
    db.close()
