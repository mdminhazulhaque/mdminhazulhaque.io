# mdminhazulhaque.io

A simple portfolio website showcasing my GitHub projects.

## Features

- Automatically fetches project data from GitHub using GraphQL API
- Displays project cards with images, descriptions, and links
- Responsive design
- Deployed on GitHub Pages

## Development

The site uses a Python script to generate project data:

```bash
# Set GitHub token (for local development)
export GITHUB_TOKEN=your_token_here

# Generate project data
python3 gen-data.py
```

## Deployment

The site automatically deploys to GitHub Pages when changes are pushed to the `master` branch.

## Tech Stack

- HTML, CSS, JavaScript
- Python (for data generation)
- GitHub GraphQL API
- GitHub Pages
