from copystatic import copy_static
from gencontent import generate_page, markdown_to_html_node, convert_block_to_html_node
import os
import shutil
import re 

def main():
    print ("Deleting public directory...")
    if os.path.exists("public"):
        shutil.rmtree("public")

    print("Copying static files to public directory...")
    copy_static("static", "public")

    print("Generating page...")
    generate_page(
            "content/index.md",
            "template.html",
            "public/index.html"
        )

if __name__ == "__main__":
    main()
