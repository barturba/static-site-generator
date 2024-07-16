import os
import shutil


def copy_files_recursive(source_dir_path, dest_dir_path):
    if not os.path.exists(dest_dir_path):
        os.mkdir(dest_dir_path)
    for item in os.listdir(source_dir_path):
        src_item = os.path.join(source_dir_path, item)
        dst_item = os.path.join(dest_dir_path, item)

        if os.path.isfile(src_item):
            shutil.copy(src_item, dst_item)
        else:
            copy_files_recursive(src_item, dst_item)
