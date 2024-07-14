import os
import shutil
from textnode import TextNode


def main():
    copy_static("static", "public")


def copy_static(source, destination):
    for item in os.listdir(source):
        src_item = os.path.join(source, item)
        dst_item = os.path.join(destination, item)

        if os.path.isfile(src_item):
            shutil.copy(src_item, dst_item)
        else:
            if os.path.exists(dst_item):
                shutil.rmtree(dst_item)
            if not os.path.exists(dst_item):
                os.mkdir(dst_item)
            copy_static(src_item, dst_item)


main()
