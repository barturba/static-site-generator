import os
from markdown_blocks import markdown_to_html_node


def extract_title(markdown):
    lines = markdown.split("\n\n")
    first_line = ""
    if len(lines) > 0:
        first_line = lines[0]
    else:
        first_line = markdown

    if first_line.startswith("# "):
        return first_line.strip("# ")
    else:
        raise ValueError("Title doesn't exist")


def generate_page(from_path, template_path, dest_path):
    print(f" * {from_path} {template_path} -> {dest_path}")
    from_file = open(from_path, "r")
    markdown_content = from_file.read()
    from_file.close()

    template_file = open(template_path, "r")
    template = template_file.read()
    template_file.close()

    node = markdown_to_html_node(markdown_content)
    html = node.to_html()

    title = extract_title(markdown_content)
    template = template.replace("{{ Title }}", title)
    template = template.replace("{{ Content }}", html)

    dest_dir_path = os.path.dirname(dest_path)
    if dest_dir_path != "":
        os.makedirs(dest_dir_path, exist_ok=True)
    to_file = open(dest_path, "w")
    to_file.write(template)


def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    if not os.path.exists(dest_dir_path):
        os.mkdir(dest_dir_path)

    # Crawl every entry in the content directory
    for item in os.listdir(dir_path_content):
        item_path = os.path.join(dir_path_content, item)

        # It's a file
        if os.path.isfile(item_path) and item_path.endswith(".md"):
            item_name = item.strip(".md")

            # For each markdown file found, generate a new .html file using the same
            # template.html. The generated pages should be written to the public
            # directory in the same directory structure.

            generate_page(
                os.path.join(dir_path_content, item_name + ".md"),
                template_path,
                os.path.join(dest_dir_path, item_name + ".html"),
            )
        # It's a directory
        else:
            generate_pages_recursive(
                os.path.join(dir_path_content, item),
                template_path,
                os.path.join(dest_dir_path, item),
            )
