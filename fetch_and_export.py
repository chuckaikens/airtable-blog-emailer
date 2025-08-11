#!/usr/bin/env python3
"""
Non-interactive version of the Airtable blog fetcher that automatically exports to JSON.
"""

from airtable_blog_fetcher import AirtableBlogFetcher

def main():
    """Run the fetcher and automatically export to JSON."""
    try:
        # Initialize the fetcher
        fetcher = AirtableBlogFetcher()
        
        # Fetch posts due this week
        print("🔍 Fetching blog posts from Airtable...")
        posts = fetcher.get_posts_due_this_week()
        
        # Display the results
        fetcher.display_posts(posts)
        
        # Automatically export to JSON
        if posts:
            fetcher.export_to_json(posts)
            print(f"\n📊 Summary: {len(posts)} blog posts due this week")
        
        return posts
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return []

if __name__ == "__main__":
    main()