#!/usr/bin/env python3
"""
Airtable Blog Post Fetcher
Fetches blog posts from Airtable that are due within the next 7 days.
"""

import os
import requests
from datetime import datetime, timedelta
from typing import List, Dict, Optional
from dotenv import load_dotenv
import json

# Load environment variables
load_dotenv()


class AirtableBlogFetcher:
    """Handles connection to Airtable and fetching of blog posts."""
    
    def __init__(self):
        """Initialize with Airtable credentials from environment variables."""
        self.api_key = os.getenv('AIRTABLE_API_KEY')
        self.base_id = os.getenv('AIRTABLE_BASE_ID')
        self.table_name = os.getenv('AIRTABLE_TABLE_NAME', 'Blog Posts')
        
        if not self.api_key or not self.base_id:
            raise ValueError("Missing required environment variables: AIRTABLE_API_KEY and AIRTABLE_BASE_ID")
        
        self.headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json'
        }
        
        self.base_url = f'https://api.airtable.com/v0/{self.base_id}/{self.table_name}'
    
    def get_posts_due_this_week(self) -> List[Dict]:
        """
        Fetch blog posts due within the next 7 days.
        
        Returns:
            List of blog post records due this week
        """
        # Calculate date range
        today = datetime.now().date()
        week_from_now = today + timedelta(days=7)
        
        # Format dates for Airtable (ISO 8601)
        today_str = today.isoformat()
        week_str = week_from_now.isoformat()
        
        # Build the filter formula
        # Adjust field name based on your Airtable schema
        due_date_field = os.getenv('AIRTABLE_DUE_DATE_FIELD', 'Due Date')
        filter_formula = f"AND(IS_AFTER({{{due_date_field}}}, '{today_str}'), IS_BEFORE({{{due_date_field}}}, '{week_str}'))"
        
        # Alternative formula if you want to include today's posts:
        # filter_formula = f"AND(NOT({{{due_date_field}}} < '{today_str}'), {{{due_date_field}}} <= '{week_str}')"
        
        params = {
            'filterByFormula': filter_formula,
            'sort[0][field]': due_date_field,
            'sort[0][direction]': 'asc'
        }
        
        try:
            response = requests.get(self.base_url, headers=self.headers, params=params)
            response.raise_for_status()
            
            data = response.json()
            records = data.get('records', [])
            
            return self._process_records(records)
            
        except requests.exceptions.RequestException as e:
            print(f"Error fetching data from Airtable: {e}")
            if hasattr(e.response, 'text'):
                print(f"Response: {e.response.text}")
            return []
    
    def _process_records(self, records: List[Dict]) -> List[Dict]:
        """
        Process and format the raw Airtable records.
        
        Args:
            records: Raw records from Airtable API
            
        Returns:
            Processed list of blog post data
        """
        processed_posts = []
        
        for record in records:
            fields = record.get('fields', {})
            
            # Extract relevant fields - adjust based on your Airtable schema
            post_data = {
                'id': record.get('id'),
                'title': fields.get('Title', 'Untitled'),
                'due_date': fields.get(os.getenv('AIRTABLE_DUE_DATE_FIELD', 'Due Date')),
                'status': fields.get('Status', 'Not Started'),
                'author': fields.get('Author', 'Unassigned'),
                'category': fields.get('Category', ''),
                'notes': fields.get('Notes', ''),
                'word_count_target': fields.get('Word Count Target', 0),
                'priority': fields.get('Priority', 'Medium')
            }
            
            # Calculate days until due
            if post_data['due_date']:
                due_date = datetime.fromisoformat(post_data['due_date']).date()
                days_until_due = (due_date - datetime.now().date()).days
                post_data['days_until_due'] = days_until_due
            
            processed_posts.append(post_data)
        
        return processed_posts
    
    def display_posts(self, posts: List[Dict]) -> None:
        """
        Display the fetched blog posts in a formatted manner.
        
        Args:
            posts: List of processed blog post data
        """
        if not posts:
            print("No blog posts due this week.")
            return
        
        print(f"\n📝 Blog Posts Due This Week ({len(posts)} total)")
        print("=" * 60)
        
        for post in posts:
            print(f"\n📌 {post['title']}")
            print(f"   Due: {post['due_date']} ({post.get('days_until_due', 'N/A')} days)")
            print(f"   Status: {post['status']}")
            print(f"   Author: {post['author']}")
            print(f"   Priority: {post['priority']}")
            
            if post['category']:
                print(f"   Category: {post['category']}")
            
            if post['word_count_target']:
                print(f"   Target Word Count: {post['word_count_target']}")
            
            if post['notes']:
                print(f"   Notes: {post['notes'][:100]}{'...' if len(post['notes']) > 100 else ''}")
        
        print("\n" + "=" * 60)
    
    def export_to_json(self, posts: List[Dict], filename: str = "blog_posts_due.json") -> None:
        """
        Export the fetched posts to a JSON file.
        
        Args:
            posts: List of processed blog post data
            filename: Output filename
        """
        with open(filename, 'w') as f:
            json.dump(posts, f, indent=2, default=str)
        
        print(f"✅ Exported {len(posts)} posts to {filename}")


def main():
    """Main function to run the blog post fetcher."""
    try:
        # Initialize the fetcher
        fetcher = AirtableBlogFetcher()
        
        # Fetch posts due this week
        print("🔍 Fetching blog posts from Airtable...")
        posts = fetcher.get_posts_due_this_week()
        
        # Display the results
        fetcher.display_posts(posts)
        
        # Optionally export to JSON
        if posts:
            export_choice = input("\nExport to JSON file? (y/n): ").lower()
            if export_choice == 'y':
                fetcher.export_to_json(posts)
        
        return posts
        
    except ValueError as e:
        print(f"❌ Configuration Error: {e}")
        print("\nPlease ensure you have set up your .env file with:")
        print("  - AIRTABLE_API_KEY")
        print("  - AIRTABLE_BASE_ID")
        print("  - AIRTABLE_TABLE_NAME (optional, defaults to 'Blog Posts')")
        print("  - AIRTABLE_DUE_DATE_FIELD (optional, defaults to 'Due Date')")
        return []
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return []


if __name__ == "__main__":
    main()