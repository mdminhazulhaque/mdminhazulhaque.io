import requests
import json
import os

owner = "mdminhazulhaque"

projects = [
    "alias-generator",
    "awesome-bangla-parenting",
    "aws-cli-cheatsheet",
    "aws-stale-dns-finder",
    "django-baby-log",
    "gcloud-cli-cheatsheet",
    "probhat-osx",
    "probhat.im",
    "python-bitbucket",
    "ruet-thesis-template-latex",
    "ssh-tunnel-manager",
    "traefik-converter",
]

token = os.getenv("GH_TOKEN")

headers = {"Authorization": f"Bearer {token}"}

data = []

for p in projects:
    print("🚀", p)

    query = f"""{{
        repository(owner: "{owner}", name: "{p}")
        {{
            openGraphImageUrl
        }}
    }}"""

    item = {
        "name": p
    }

    try:
        response = requests.post("https://api.github.com/graphql", json={'query': query}, headers=headers)
        item["image"] = response.json()["data"]["repository"]["openGraphImageUrl"]
    except:
        pass

    try:
        response = requests.get(f"https://api.github.com/repos/{owner}/{p}/pages", headers=headers)
        item["url"] = response.json()["html_url"]
    except:
        pass

    try:
        response = requests.get(f"https://api.github.com/repos/{owner}/{p}", headers=headers)
        item["description"] = response.json()["description"]
    except:
        pass

    data.append(item)

with open("data.json", "w") as fp:
    json.dump(data, fp, indent=2)
