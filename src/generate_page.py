from markdown_to_html import markdown_to_html_node, extract_title
import os

def generate_page(from_path, template_path, dest_path):
    current_dir = os.path.dirname(__file__)
    from_path = os.path.join(current_dir,from_path)
    template_path = os.path.join(current_dir,template_path)
    dest_path = os.path.join(current_dir,dest_path)
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    md, tmpl = None, None
    with open(from_path,'r') as f:
        md = f.read()
    with open(template_path,'r') as f:
        tmpl = f.read()
    if md == None or tmpl == None:
        raise Exception("File(s) not found")
    p_node = markdown_to_html_node(md)
    html = p_node.to_html()
    title = extract_title(md)
    tmpl = tmpl.replace("{{ Title }}",title)
    tmpl = tmpl.replace("{{ Content }}",html)
    if not os.path.exists(os.path.dirname(dest_path)):
        os.makedirs(os.path.dirname(dest_path))
    with open(dest_path,'w') as f:
        f.write(tmpl)

def find_md_helper(current_dir,rel_path,locations):
    for item in os.listdir(current_dir):
        full_path = os.path.join(current_dir,item)
        rel_path_ = os.path.join(rel_path,item)
        if os.path.isfile(full_path):
            if full_path.endswith(".md"):
                locations.append(rel_path_)
        else:
            find_md_helper(full_path,rel_path_,locations)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    current_dir = os.path.dirname(__file__)
    dir_path_content = os.path.join(current_dir, dir_path_content)
    template_path = os.path.join(current_dir, template_path)
    dest_dir_path = os.path.join(current_dir, dest_dir_path)
    locations = []
    find_md_helper(dir_path_content,'',locations)
    htmls = []
    for loc in locations:
        from_loc = os.path.join(dir_path_content,loc)
        to_loc = os.path.join(dest_dir_path,loc)
        to_loc = to_loc[:-3]+".html"
        html = generate_page(from_loc, template_path, to_loc)
        htmls.append(html)
    return htmls
