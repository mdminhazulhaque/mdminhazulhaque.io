#!/usr/bin/env python3
"""
Generate README.md from projects.json
"""

import json

def generate_readme():
    """Generate README.md from projects data"""

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

    # Generate projects list
    projects_md = []
    for project in projects:
        emoji = project.get('emoji', '📦')
        name = project.get('name', '')
        description = project.get('description', '')
        url = project.get('url', f"https://github.com/mdminhazulhaque/{name}")

        projects_md.append(f"{emoji} [**{name}**]({url}): {description}<br>")

    projects_section = '\n'.join(projects_md)

    # Full README template
    readme_content = f"""# Hi, I'm Minhaz 👋

🏗️ Solutions Architect<br>
🛠️ Platform Engineer

## What I'm up to 👨‍💻

🧱 Building Platforms<br>
📐 Architecting Solutions<br>
🧠 Crafting AI Products<br>
🛡️ Handling Security<br>

## Projects 📂

{projects_section}

## Find me 🌎

🚀 [Website](https://mdminhazulhaque.io)<br>
📝 [Blog](https://blog.mdminhazulhaque.io/)<br>
💼 [LinkedIn](https://www.linkedin.com/in/mdminhazulhaque/)<br>
🐙 [GitHub](https://github.com/mdminhazulhaque)
"""

    # Write output
    with open("README.md", "w") as f:
        f.write(readme_content)

    print("✅ Successfully generated README.md")

if __name__ == "__main__":
    generate_readme()
