import os
import shutil
from pathlib import Path
from block_functions import markdown_to_html_node, extract_title


def copy_static(source_dir, dest_dir):
    # First clear the destination directory once at the very start, outside of recursion
    if os.path.exists(dest_dir):
        shutil.rmtree(dest_dir)
    os.mkdir(dest_dir)

    # List contents of the source directory
    for item in os.listdir(source_dir):
        source_path = os.path.join(source_dir, item)  # Full path of item in source
        dest_path = os.path.join(dest_dir, item)      # Corresponding path in destination

        if os.path.isfile(source_path):
            shutil.copy(source_path, dest_path)
        elif os.path.isdir(source_path):
            # Create the directory in the destination path
            os.mkdir(dest_path)
            # Recursively copy contents
            copy_static(source_path, dest_path)


def generate_page(from_path, template_path, dest_path):
    print(f"Generating  page from {from_path} to {dest_path} using {template_path}")
    with open(from_path, 'r') as file:
        contents_from = file.read()
        html_node = markdown_to_html_node(contents_from)
        html_content = html_node.to_html()
        title = extract_title(contents_from)

    with open(template_path, 'r') as file:
        contents_template = file.read()
        html = contents_template.replace('{{ Title }}', title).replace('{{ Content }}', html_content)

    directory = os.path.dirname(dest_path)
    if directory:
        os.makedirs(directory, exist_ok=True)
    with open(dest_path, 'w') as file:
        file.write(html)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    for filename in os.listdir(dir_path_content):
        from_path = os.path.join(dir_path_content, filename)
        dest_path = os.path.join(dest_dir_path, filename)
        if os.path.isfile(from_path):
            dest_path = Path(dest_path).with_suffix(".html")
            generate_page(from_path, template_path, dest_path)
        else:
            generate_pages_recursive(from_path, template_path, dest_path)





def main():
    copy_static('static', 'public')
    generate_pages_recursive("./content", "./template.html", "./public")
    

main()