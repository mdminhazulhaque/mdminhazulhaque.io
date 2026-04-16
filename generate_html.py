#!/usr/bin/env python3
"""
Generate index.html from Jinja2 template using projects.json data
"""

import json
from jinja2 import Template


def emoji_to_github_img(emoji):
    """Convert a Unicode emoji character to a GitHub CDN <img> tag."""
    # Strip variation selectors (U+FE0E, U+FE0F)
    cleaned = emoji.replace("\ufe0e", "").replace("\ufe0f", "")
    # Build codepoint string (hyphen-separated for multi-codepoint emoji like ZWJ sequences)
    codepoints = "-".join(f"{ord(c):x}" for c in cleaned)
    url = f"https://github.githubassets.com/images/icons/emoji/unicode/{codepoints}.png"
    return f'<img class="g-emoji" src="{url}" alt="{emoji}">'


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

    # Convert emoji to GitHub CDN images
    for project in projects:
        project["emoji_img"] = emoji_to_github_img(project["emoji"])

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
