import requests
import json
import os
import time
import re

owner = "mdminhazulhaque"

projects = [
    "ai-prescriptions-scanner",
    "alias-generator",
    "awesome-bangla-parenting",
    "aws-cli-cheatsheet",
    "aws-resource-explorer",
    "aws-resource-watcher",
    "aws-stale-dns-finder",
    "bangladeshi-parcel-tracker",
    "django-baby-log",
    "gcloud-cli-cheatsheet",
    "kube-git-backup",
    "probhat-macos",
    "probhat-web",
    "python-bitbucket-cli",
    "python-bpdb",
    "python-desco",
    "python-dpdc",
    "python-nesco",
    "ruet-thesis-template-latex",
    "ssh-tunnel-manager",
    "traefik-converter",
]

token = os.getenv("GITHUB_TOKEN")

if not token:
    print("❌ Error: GITHUB_TOKEN environment variable is not set")
    exit(1)

headers = {"Authorization": f"Bearer {token}"}

def extract_emoji_and_description(text):
    """Extract emoji from the beginning of description and return both separately"""
    if not text:
        return None, text

    # Match emoji at the start of the string (with optional whitespace)
    # Includes variation selectors (\uFE00-\uFE0F) and zero-width joiner (\u200D) for complete emoji sequences
    emoji_pattern = r'^([\U0001F300-\U0001F9FF\U0001F600-\U0001F64F\U0001F680-\U0001F6FF\U00002600-\U000027BF\u2600-\u26FF\u2700-\u27BF\uFE00-\uFE0F\u200D\U0001F3FB-\U0001F3FF]+)\s*(.*)$'
    match = re.match(emoji_pattern, text)

    if match:
        emoji = match.group(1)
        description = match.group(2).strip()
        return emoji, description

    return None, text.strip() if text else text

data = []
projects_data = []

def fetch_repositories_batch(batch_projects):
    """Fetch repository data for a batch of projects"""
    repositories_query = ""
    for i, p in enumerate(batch_projects):
        repositories_query += f"""
        repo{i}: repository(owner: "{owner}", name: "{p}") {{
            name
            description
            homepageUrl
        }}"""

    query = f"""{{
        {repositories_query}
    }}"""

    response = requests.post("https://api.github.com/graphql", json={'query': query}, headers=headers)
    return response.json()

# Process repositories in batches of 10 to avoid GraphQL complexity limits
batch_size = 10
sorted_projects = sorted(projects)

for i in range(0, len(sorted_projects), batch_size):
    batch = sorted_projects[i:i + batch_size]
    print(f"📦 Processing batch {i//batch_size + 1}: {len(batch)} repositories")
    
    try:
        response_data = fetch_repositories_batch(batch)
        
        if "errors" in response_data:
            print("❌ GraphQL errors:", response_data["errors"])
            # Check if rate limited
            if any("rate limit" in str(error).lower() for error in response_data["errors"]):
                print("⏰ Rate limited, waiting 60 seconds...")
                time.sleep(60)
                response_data = fetch_repositories_batch(batch)  # Retry
        
        repos_data = response_data.get("data", {})
        
        for key, repo_data in repos_data.items():
            if repo_data:  # Check if repository data exists
                # Extract emoji and clean description
                emoji, clean_description = extract_emoji_and_description(repo_data["description"])

                item = {
                    "name": repo_data["name"],
                    "description": repo_data["description"]
                }

                # Only set URL if homepage URL is available (skip repository URL)
                if repo_data["homepageUrl"]:
                    item["url"] = repo_data["homepageUrl"]

                print("🚀", str(item))
                data.append(item)

                # Create projects.json entry
                project_item = {
                    "name": repo_data["name"],
                    "description": clean_description
                }

                if emoji:
                    project_item["emoji"] = emoji

                # Link to demo if homepage exists, otherwise link to GitHub
                if repo_data["homepageUrl"]:
                    project_item["url"] = repo_data["homepageUrl"]
                else:
                    project_item["url"] = f"https://github.com/{owner}/{repo_data['name']}"

                projects_data.append(project_item)
            else:
                print(f"❌ No data found for repository key: {key}")
                
    except Exception as e:
        print(f"❌ Error fetching batch: {e}")
        # Fallback to individual requests for this batch
        print("🔄 Falling back to individual requests for this batch...")
        
        for p in batch:
            item = {
                "name": p
            }

            try:
                query = f"""{{
                    repository(owner: "{owner}", name: "{p}")
                    {{
                        name
                        description
                        homepageUrl
                    }}
                }}"""

                response = requests.post("https://api.github.com/graphql", json={'query': query}, headers=headers)
                repo_data = response.json()["data"]["repository"]

                # Extract emoji and clean description
                emoji, clean_description = extract_emoji_and_description(repo_data["description"])

                item["description"] = repo_data["description"]

                # Only set URL if homepage URL is available (skip repository URL)
                if repo_data["homepageUrl"]:
                    item["url"] = repo_data["homepageUrl"]

                print("🚀", str(item))
                data.append(item)

                # Create projects.json entry
                project_item = {
                    "name": repo_data["name"],
                    "description": clean_description
                }

                if emoji:
                    project_item["emoji"] = emoji

                # Link to demo if homepage exists, otherwise link to GitHub
                if repo_data["homepageUrl"]:
                    project_item["url"] = repo_data["homepageUrl"]
                else:
                    project_item["url"] = f"https://github.com/{owner}/{repo_data['name']}"

                projects_data.append(project_item)

                # Small delay between individual requests
                time.sleep(0.1)

            except Exception as individual_error:
                print(f"❌ Error fetching data for {p}: {individual_error}")
                continue
    
    # Small delay between batches to be respectful to the API
    if i + batch_size < len(sorted_projects):
        time.sleep(1)

with open("projects.json", "w") as fp:
    json.dump(projects_data, fp, indent=2)

print(f"✅ Successfully generated projects.json with {len(projects_data)} projects")