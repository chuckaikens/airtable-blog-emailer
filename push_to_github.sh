#!/bin/bash
# Script to push to GitHub

echo "📦 Preparing to push to GitHub..."

# Initialize git if not already done
if [ ! -d .git ]; then
    git init
    echo "✅ Git initialized"
fi

# Add all safe files (respecting .gitignore)
git add .
echo "✅ Files staged"

# Create initial commit
git commit -m "Initial commit: Airtable to Gmail blog post automation

Features:
- Fetch blog posts from Airtable API
- Filter posts due within 7 days  
- Send formatted HTML emails via Gmail
- Multiple export formats (JSON, CSV, Markdown)
- Automated scheduling support"

echo "✅ Commit created"

echo ""
echo "Now you need to:"
echo "1. Create a new repo on GitHub: https://github.com/new"
echo "2. Copy the repository URL"
echo "3. Run these commands:"
echo ""
echo "git remote add origin YOUR_GITHUB_REPO_URL"
echo "git branch -M main"
echo "git push -u origin main"
echo ""
echo "Example:"
echo "git remote add origin https://github.com/yourusername/airtable-blog-emailer.git"
echo "git branch -M main"
echo "git push -u origin main"