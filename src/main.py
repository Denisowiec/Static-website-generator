from text_and_markdown import *
from html_nodes import *
import os, sys, shutil

# Paths to the content directories
DIR_STATIC = "static"
DIR_PUBLIC = "docs"
DIR_CONTENT = "content"

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

def generate_page(from_path, template_path, dest_path, base_path):
    print(f"Generating page from '{from_path}' to '{dest_path}' using '{template_path}'")
    
    with open(from_path, "r") as file:
        md = file.read()
    
    with open(template_path, "r") as file:
        template = file.read()
    
    title = extract_title(md)
    md_converted_to_nodes = markdown_to_html_node(md)
    html = md_converted_to_nodes.to_html()

    content = template.replace("{{ Title }}", title)
    content = content.replace("{{ Content }}", html)
    content = content.replace('href="/', f'href="{base_path}')
    content = content.replace('src="/', f'src="{base_path}')

    with open(dest_path, "w") as file:
        file.write(content)

def generate_pages_recursive(from_path, template_path, dest_path, base_path):

    contents = os.listdir(from_path)
    for f in contents:
        file = os.path.join(from_path, f)
        if os.path.isdir(file):
            dest = os.path.join(dest_path, f)
            if not os.path.exists(dest):
                os.mkdir(dest)
            generate_pages_recursive(file, template_path, dest,base_path)
        elif os.path.isfile(file):
            if file[-2:] == "md":
                name = os.path.basename(file)[:-3]
                generate_page(file, template_path, os.path.join(dest_path, name + ".html"), base_path)



def main():
    if len(sys.argv) > 1:
        basepath = sys.argv[1]
    else:
        basepath = "/"

    copy_contents(DIR_STATIC, DIR_PUBLIC)
    generate_pages_recursive(DIR_CONTENT, "template.html", DIR_PUBLIC, basepath)

if __name__=="__main__":
    main()