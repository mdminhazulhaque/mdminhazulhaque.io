#!/usr/bin/env python3
"""
Generate index.html from Jinja2 template using projects.json data
"""

import json
from jinja2 import Template

def render_html():
    """Generate index.html from template and projects data"""

    # Read projects data
    try:
        with open("projects.json", "r") as f:
            projects = json.load(f)
        print(f"✅ Loaded {len(projects)} projects from projects.json")
    except FileNotFoundError:
        print("❌ Error: projects.json not found. Please run fetch_projects.py first.")
        return
    except json.JSONDecodeError as e:
        print(f"❌ Error: Invalid JSON in projects.json: {e}")
        return

    # Read template
    try:
        with open("index.html.j2", "r") as f:
            template_content = f.read()
        print("✅ Loaded template from index.html.j2")
    except FileNotFoundError:
        print("❌ Error: index.html.j2 template not found.")
        return

    # Render template
    template = Template(template_content)
    rendered_html = template.render(projects=projects)

    # Write output
    with open("index.html", "w") as f:
        f.write(rendered_html)

    print("✅ Successfully generated index.html")

if __name__ == "__main__":
    render_html()
