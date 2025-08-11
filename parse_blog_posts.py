#!/usr/bin/env python3
"""
Examples of parsing and working with the blog posts JSON file.
"""

import json
from datetime import datetime
from collections import defaultdict

def load_blog_posts(filename="blog_posts_due.json"):
    """Load blog posts from JSON file."""
    with open(filename, 'r') as f:
        return json.load(f)

def example_1_basic_parsing():
    """Example 1: Basic parsing - print all titles."""
    print("\n📚 EXAMPLE 1: All Blog Post Titles")
    print("=" * 50)
    
    posts = load_blog_posts()
    
    for i, post in enumerate(posts, 1):
        print(f"{i}. {post['title']}")

def example_2_filter_by_date():
    """Example 2: Filter posts by due date."""
    print("\n📅 EXAMPLE 2: Posts Due Tomorrow")
    print("=" * 50)
    
    posts = load_blog_posts()
    tomorrow_posts = [p for p in posts if p['days_until_due'] == 1]
    
    for post in tomorrow_posts:
        print(f"• {post['title']}")
        print(f"  Due: {post['due_date']}")
        print(f"  Status: {post['status']}")

def example_3_group_by_date():
    """Example 3: Group posts by due date."""
    print("\n📊 EXAMPLE 3: Posts Grouped by Due Date")
    print("=" * 50)
    
    posts = load_blog_posts()
    
    # Group by due date
    posts_by_date = defaultdict(list)
    for post in posts:
        posts_by_date[post['due_date']].append(post)
    
    # Display grouped posts
    for date in sorted(posts_by_date.keys()):
        print(f"\n📌 {date} ({len(posts_by_date[date])} posts):")
        for post in posts_by_date[date]:
            print(f"  • {post['title']}")

def example_4_priority_posts():
    """Example 4: Find high priority or specific posts."""
    print("\n⚡ EXAMPLE 4: Filter by Priority/Status")
    print("=" * 50)
    
    posts = load_blog_posts()
    
    # Filter not started posts
    not_started = [p for p in posts if p['status'] == 'Not Started']
    print(f"\nNot Started: {len(not_started)} posts")
    
    # Filter by days until due
    urgent = [p for p in posts if p['days_until_due'] <= 2]
    print(f"Urgent (≤2 days): {len(urgent)} posts")
    
    # Show urgent titles
    print("\nUrgent posts:")
    for post in urgent:
        print(f"  • {post['title']} (due in {post['days_until_due']} days)")

def example_5_export_subset():
    """Example 5: Export a subset to a new JSON file."""
    print("\n💾 EXAMPLE 5: Export Filtered Data")
    print("=" * 50)
    
    posts = load_blog_posts()
    
    # Get posts due in next 2 days
    urgent_posts = [p for p in posts if p['days_until_due'] <= 2]
    
    # Export to new file
    with open('urgent_posts.json', 'w') as f:
        json.dump(urgent_posts, f, indent=2, default=str)
    
    print(f"Exported {len(urgent_posts)} urgent posts to 'urgent_posts.json'")

def example_6_create_markdown():
    """Example 6: Create a Markdown report from the JSON."""
    print("\n📝 EXAMPLE 6: Generate Markdown Report")
    print("=" * 50)
    
    posts = load_blog_posts()
    
    # Group by date
    posts_by_date = defaultdict(list)
    for post in posts:
        posts_by_date[post['due_date']].append(post)
    
    # Create markdown content
    markdown = "# Blog Posts Due This Week\n\n"
    markdown += f"*Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}*\n\n"
    markdown += f"**Total Posts:** {len(posts)}\n\n"
    
    for date in sorted(posts_by_date.keys()):
        due_date = datetime.fromisoformat(date)
        markdown += f"## {due_date.strftime('%A, %B %d, %Y')}\n\n"
        
        for post in posts_by_date[date]:
            markdown += f"### {post['title']}\n"
            markdown += f"- **Status:** {post['status']}\n"
            markdown += f"- **Priority:** {post['priority']}\n"
            if post['word_count_target']:
                markdown += f"- **Target Words:** {post['word_count_target']}\n"
            if post['notes']:
                markdown += f"- **Notes:** {post['notes'][:100]}...\n"
            markdown += "\n"
    
    # Save to file
    with open('blog_posts_report.md', 'w') as f:
        f.write(markdown)
    
    print("Created 'blog_posts_report.md'")
    print("\nPreview:")
    print(markdown[:500] + "...")

def example_7_csv_export():
    """Example 7: Export to CSV for spreadsheet use."""
    print("\n📊 EXAMPLE 7: Export to CSV")
    print("=" * 50)
    
    import csv
    
    posts = load_blog_posts()
    
    # Define CSV columns
    fieldnames = ['title', 'due_date', 'days_until_due', 'status', 'priority', 
                  'author', 'category', 'word_count_target']
    
    # Write CSV
    with open('blog_posts.csv', 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames, extrasaction='ignore')
        
        writer.writeheader()
        writer.writerows(posts)
    
    print(f"Exported {len(posts)} posts to 'blog_posts.csv'")
    print("You can open this in Excel, Google Sheets, etc.")

def main():
    """Run all examples."""
    try:
        # Check if JSON file exists
        posts = load_blog_posts()
        print(f"✅ Loaded {len(posts)} blog posts from JSON\n")
        
        # Run examples
        example_1_basic_parsing()
        example_2_filter_by_date()
        example_3_group_by_date()
        example_4_priority_posts()
        example_5_export_subset()
        example_6_create_markdown()
        example_7_csv_export()
        
        print("\n" + "=" * 50)
        print("✨ All examples completed successfully!")
        
    except FileNotFoundError:
        print("❌ Error: blog_posts_due.json not found.")
        print("Please run 'python3 fetch_and_export.py' first to generate the JSON file.")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()