from jinja2 import Environment, FileSystemLoader
import json

environment = Environment(loader=FileSystemLoader("templates/"))
template = environment.get_template("index.html")

with open("data.json", "r") as fp:
    projects = json.load(fp)

content = template.render(projects=projects)

with open("./public/index.html", "w") as html:
    html.write(content)

print("Build successful! Check the public/index.html file.")