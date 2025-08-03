from text_and_markdown import *
from html_nodes import *
import os
import shutil

# Paths to the content directories
DIR_STATIC = "static"
DIR_PUBLIC = "public"

def copy_contents(stc, pub):
    # stc = static directory
    # pub = public directory
    if os.path.exists(pub):
        shutil.rmtree(pub)
    os.mkdir(pub)
    copy_files(stc, pub)
    
def copy_files(base_path, dest_path):
    contents = os.listdir(base_path)
    for f in contents:
        file = os.path.join(base_path, f)
        if os.path.isfile(file):
            shutil.copy(file, os.path.join(dest_path, f))
        elif os.path.isdir(file):
            dest = os.path.join(dest_path, f)
            if not os.path.exists(dest):
                os.mkdir(dest)
            copy_files(file, dest)


def main():
    copy_contents(DIR_STATIC, DIR_PUBLIC)

if __name__=="__main__":
    main()