from copystatic import copy_static
from gencontent import generate_page, markdown_to_html_node, convert_block_to_html_node
from pathlib import Path
import os
import shutil
import re 

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    for item in os.listdir(dir_path_content):
        current_item_path = os.path.join(dir_path_content, item)
        if os.path.isfile(current_item_path):
            if current_item_path.endswith(".md"):
                current_item_path_obj = Path(current_item_path)
                dir_path_content_obj = Path(dir_path_content)
                dest_dir_path_obj = Path(dest_dir_path)
                relative_path = current_item_path_obj.relative_to(dir_path_content_obj)
                html_relative_path = relative_path.with_suffix(".html")
                dest_path_final = dest_dir_path_obj / html_relative_path
                os.makedirs(dest_path_final.parent, exist_ok=True)
                generate_page(current_item_path, template_path, dest_path_final)
            else:
                continue
        else:
            generate_pages_recursive(current_item_path, template_path, os.path.join(dest_dir_path, item))

def main():
    print ("Deleting public directory...")
    if os.path.exists("public"):
        shutil.rmtree("public")

    print("Copying static files to public directory...")
    copy_static("static", "public")

    print("Generating page...")
    generate_pages_recursive(
            "content",
            "template.html",
            "public"
        )

if __name__ == "__main__":
    main()
