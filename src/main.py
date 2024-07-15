import os
import shutil
from markdown_blocks import markdown_to_html_node
from textnode import TextNode


def main():
    delete_and_recreate_dir("public")
    copy_static("static", "public")
    generate_page("content/index.md", "template.html", "public/index.html")


def delete_and_recreate_dir(directory):
    print("delete_and_recreate_dir:")
    if os.path.exists(directory):
        shutil.rmtree(directory)
    if not os.path.exists(directory):
        os.mkdir(directory)


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


def extract_title(markdown):
    # extract the title
    lines = markdown.split("\n\n")
    first_line = ""
    if len(lines) > 0:
        first_line = lines[0]
    else:
        first_line = markdown

    # if there is no title, raise an exception
    if first_line.startswith("# "):
        return first_line.strip("# ")
    else:
        raise ValueError("Title doesn't exist")
    # strip leading # and any leading or trailing whitespace


def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    markdown_string = ""
    # read the markdown file
    with open(from_path, "r") as f:
        markdown_string = f.read()
    # print(f"DEBUG:  markdown_string: {markdown_string}")

    template_string = ""
    # read the template file
    with open(template_path, "r") as f:
        template_string = f.read()
    # print(f"DEBUG:  template_string: {template_string}")

    html_output = markdown_to_html_node(markdown_string).to_html()
    # print(f"DEBUG:  html_output: {html_output}")

    # extract the title
    title = extract_title(markdown_string)
    # print(f"DEBUG:  title: {title}")

    # replace title and content tags with actual input
    template_string = template_string.replace("{{ Title }}", title)
    # print(f"DEBUG:  template_string: {template_string}")

    template_string = template_string.replace("{{ Content }}", html_output)
    # print(f"DEBUG:  template_string: {template_string}")

    output_file_name_parts = from_path.split(".md")
    output_file_dirs = ""
    if len(output_file_name_parts) == 2:
        output_file_dirs = output_file_name_parts[0]
    # print(f"DEBUG:  output_file_name: {output_file_name}")

    # TODO: get output dir name
    # TODO: make all ancestor directories recursively up to the output path
    os.makedirs(output_file_dirs, exist_ok=True)

    # TODO: write the output file out to the dest_path
    f = open(dest_path, "a")
    f.write(template_string)
    f.close()

    # TODO: write the output file out to the dest_path

    # os.makedirs(name, mode=0o777, exist_ok=False)¶


main()
