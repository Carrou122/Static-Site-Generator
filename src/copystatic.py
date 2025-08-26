import os
import shutil

def copy_static(source_path, dest_path):
    if os.path.exists(dest_path):
        shutil.rmtree(dest_path)
    os.mkdir(dest_path)
    for item in os.listdir(source_path):
        source_item_full_path = os.path.join(source_path, item)
        dest_item_full_path = os.path.join(dest_path, item)
        if os.path.isfile(source_item_full_path):
            shutil.copy(source_item_full_path, dest_item_full_path)
            print(f"Copying file from <{source_item_full_path}> to <{dest_item_full_path}>")
        else:
            os.mkdir(dest_item_full_path)
            copy_static(source_item_full_path, dest_item_full_path)
