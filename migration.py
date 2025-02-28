from utils.db_util import *
import json
import shutil


# 检查字段是否已经存在
def field_exists(table_name, field_name):
    cursor = db.execute_sql(f"PRAGMA table_info({table_name});")
    columns = cursor.fetchall()
    return any(column[1] == field_name for column in columns)


# 定义迁移操作
def add_content_type_column():
    # 创建迁移器
    migrator = SqliteMigrator(db)

    # 增加 collection.content_type 字段
    if not field_exists('collection', 'content_type'):
        migrate(
            migrator.add_column('collection', 'content_type', CharField(default="wav")),
        )
        print("Added 'content_type' column to 'collection' table.")

    # 增加 folder.content_type
    if not field_exists('folder', 'content_type'):
        migrate(
            migrator.add_column('folder', 'content_type', CharField(default="wav")),
        )
        print("Added 'content_type' column to 'folder' table.")


def handle_single_add_folder_order(collection_id):
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


def add_folder_orders():
    the_list = Collection.select().order_by(Collection.created_date)
    for col in the_list:
        handle_single_add_folder_order(col.id)


def override_name_by_custom_name():
    # 去除custom_name字段，将custom_name的值赋给name字段
    the_list = Folder.select().order_by(Folder.created_date)
    for folder in the_list:
        if folder.name is not None and len(folder.name) > 0:
            continue

        if folder.custom_name != folder.name:
            folder.name = folder.custom_name
            folder.save()
            print("update folder name:", folder.name)


# 执行迁移
if __name__ == "__main__":
    formatted_date = datetime.datetime.now().strftime('%m%d_%H%M%S')
    shutil.copy('my_database.db', f'my_database_备份{formatted_date}.db')

    db.connect()
    add_content_type_column()
    add_folder_orders()
    override_name_by_custom_name()
    db.close()
    print("Migration completed.")
