import requests
import json
import os
import time
from PIL import Image
from urllib.parse import urlparse
import io

owner = "mdminhazulhaque"

projects = [
    "alias-generator",
    "awesome-bangla-parenting",
    "aws-cli-cheatsheet",
    "aws-resource-watcher",
    "aws-stale-dns-finder",
    "bangladeshi-parcel-tracker",
    "django-baby-log",
    "gcloud-cli-cheatsheet",
    "probhat-macos",
    "probhat-web",
    "python-bitbucket-cli",
    "ruet-thesis-template-latex",
    "ssh-tunnel-manager",
    "traefik-converter",
    "python-desco",
    "python-bpdb",
    "python-nesco",
    "kube-git-backup",
    "aws-resource-explorer",
]

token = os.getenv("GITHUB_TOKEN")

if not token:
    print("❌ Error: GITHUB_TOKEN environment variable is not set")
    exit(1)

headers = {"Authorization": f"Bearer {token}"}

# Create images directory if it doesn't exist
os.makedirs("images", exist_ok=True)

def download_and_process_image(image_url, repo_name):
    """Download image, convert to WebP, resize to 640x320, and save locally"""
    if not image_url:
        return None
    
    try:
        # Download the image
        response = requests.get(image_url, timeout=30)
        response.raise_for_status()
        
        # Open image with PIL
        img = Image.open(io.BytesIO(response.content))
        
        # Convert to RGB if necessary (for WebP compatibility)
        if img.mode in ('RGBA', 'LA', 'P'):
            img = img.convert('RGB')
        
        # Resize to 640x320
        img = img.resize((640, 320), Image.Resampling.LANCZOS)
        
        # Save as WebP
        local_filename = f"images/{repo_name}.webp"
        img.save(local_filename, 'WEBP', quality=85, optimize=True)
        
        print(f"📸 Downloaded and processed image for {repo_name}")
        return local_filename
        
    except Exception as e:
        print(f"❌ Error processing image for {repo_name}: {e}")
        return None

data = []

def fetch_repositories_batch(batch_projects):
    """Fetch repository data for a batch of projects"""
    repositories_query = ""
    for i, p in enumerate(batch_projects):
        repositories_query += f"""
        repo{i}: repository(owner: "{owner}", name: "{p}") {{
            name
            openGraphImageUrl
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
                # Download and process the image
                local_image_path = download_and_process_image(repo_data["openGraphImageUrl"], repo_data["name"])
                
                item = {
                    "name": repo_data["name"],
                    "description": repo_data["description"]
                }
                
                # Set local image path if download was successful
                if local_image_path:
                    item["image"] = local_image_path
                
                # Only set URL if homepage URL is available (skip repository URL)
                if repo_data["homepageUrl"]:
                    item["url"] = repo_data["homepageUrl"]
                    
                print("🚀", str(item))
                data.append(item)
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
                        openGraphImageUrl
                        description
                        homepageUrl
                    }}
                }}"""

                response = requests.post("https://api.github.com/graphql", json={'query': query}, headers=headers)
                repo_data = response.json()["data"]["repository"]
                
                # Download and process the image
                local_image_path = download_and_process_image(repo_data["openGraphImageUrl"], repo_data["name"])
                
                item["description"] = repo_data["description"]
                
                # Set local image path if download was successful
                if local_image_path:
                    item["image"] = local_image_path
                
                # Only set URL if homepage URL is available (skip repository URL)
                if repo_data["homepageUrl"]:
                    item["url"] = repo_data["homepageUrl"]
                    
                print("🚀", str(item))
                data.append(item)
                
                # Small delay between individual requests
                time.sleep(0.1)
                    
            except Exception as individual_error:
                print(f"❌ Error fetching data for {p}: {individual_error}")
                continue
    
    # Small delay between batches to be respectful to the API
    if i + batch_size < len(sorted_projects):
        time.sleep(1)

with open("data.json", "w") as fp:
    json.dump(data, fp, indent=2)

print(f"✅ Successfully processed {len(data)} repositories and saved to data.json")
