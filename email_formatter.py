#!/usr/bin/env python3
"""
Format blog posts for email delivery - creates both HTML and plain text versions.
"""

import json
from datetime import datetime
from collections import defaultdict
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

def load_blog_posts(filename="blog_posts_due.json"):
    """Load blog posts from JSON file."""
    with open(filename, 'r') as f:
        return json.load(f)

def create_html_email(posts):
    """Create HTML formatted email content."""
    # Group posts by date
    posts_by_date = defaultdict(list)
    for post in posts:
        posts_by_date[post['due_date']].append(post)
    
    # Count statistics
    total_posts = len(posts)
    urgent_posts = len([p for p in posts if p['days_until_due'] <= 2])
    not_started = len([p for p in posts if p['status'] == 'Not Started'])
    
    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
                line-height: 1.6;
                color: #333;
                max-width: 800px;
                margin: 0 auto;
                padding: 20px;
            }
            h1 {
                color: #2c3e50;
                border-bottom: 3px solid #3498db;
                padding-bottom: 10px;
            }
            h2 {
                color: #34495e;
                margin-top: 30px;
                background: #ecf0f1;
                padding: 10px;
                border-left: 4px solid #3498db;
            }
            .stats {
                background: #f8f9fa;
                border: 1px solid #dee2e6;
                border-radius: 5px;
                padding: 15px;
                margin: 20px 0;
            }
            .stat-item {
                display: inline-block;
                margin-right: 30px;
                font-size: 16px;
            }
            .stat-number {
                font-size: 24px;
                font-weight: bold;
                color: #3498db;
            }
            .post-card {
                background: white;
                border: 1px solid #e1e4e8;
                border-radius: 5px;
                padding: 15px;
                margin: 10px 0;
                box-shadow: 0 1px 3px rgba(0,0,0,0.1);
            }
            .post-title {
                font-size: 18px;
                font-weight: bold;
                color: #2c3e50;
                margin-bottom: 10px;
            }
            .post-meta {
                font-size: 14px;
                color: #666;
                line-height: 1.8;
            }
            .urgent {
                background: #fff3cd;
                border-color: #ffc107;
            }
            .label {
                display: inline-block;
                padding: 2px 8px;
                border-radius: 3px;
                font-size: 12px;
                font-weight: bold;
                text-transform: uppercase;
                margin-right: 5px;
            }
            .label-urgent {
                background: #dc3545;
                color: white;
            }
            .label-soon {
                background: #ffc107;
                color: #333;
            }
            .label-medium {
                background: #6c757d;
                color: white;
            }
            .footer {
                margin-top: 40px;
                padding-top: 20px;
                border-top: 1px solid #dee2e6;
                font-size: 12px;
                color: #6c757d;
                text-align: center;
            }
        </style>
    </head>
    <body>
    """
    
    # Header
    html += f"""
        <h1>📝 Weekly Blog Post Schedule</h1>
        <p><strong>Report Generated:</strong> {datetime.now().strftime('%B %d, %Y at %I:%M %p')}</p>
        
        <div class="stats">
            <div class="stat-item">
                <div class="stat-number">{total_posts}</div>
                <div>Total Posts Due</div>
            </div>
            <div class="stat-item">
                <div class="stat-number" style="color: #dc3545;">{urgent_posts}</div>
                <div>Urgent (≤2 days)</div>
            </div>
            <div class="stat-item">
                <div class="stat-number" style="color: #ffc107;">{not_started}</div>
                <div>Not Started</div>
            </div>
        </div>
    """
    
    # Posts by date
    for date in sorted(posts_by_date.keys()):
        due_date = datetime.fromisoformat(date)
        date_str = due_date.strftime('%A, %B %d, %Y')
        
        # Calculate urgency
        days_until = (due_date.date() - datetime.now().date()).days
        
        html += f'<h2>{date_str}'
        if days_until <= 1:
            html += ' <span class="label label-urgent">URGENT</span>'
        elif days_until <= 2:
            html += ' <span class="label label-soon">DUE SOON</span>'
        html += '</h2>\n'
        
        for post in posts_by_date[date]:
            card_class = 'post-card urgent' if post['days_until_due'] <= 2 else 'post-card'
            
            html += f'<div class="{card_class}">\n'
            html += f'  <div class="post-title">{post["title"]}</div>\n'
            html += '  <div class="post-meta">\n'
            html += f'    <strong>Status:</strong> {post["status"]} | '
            html += f'    <strong>Priority:</strong> {post["priority"]} | '
            html += f'    <strong>Days Until Due:</strong> {post["days_until_due"]}<br>\n'
            
            if post['author'] != 'Unassigned':
                html += f'    <strong>Author:</strong> {post["author"]}<br>\n'
            
            if post['category']:
                html += f'    <strong>Category:</strong> {post["category"]}<br>\n'
            
            if post['word_count_target']:
                html += f'    <strong>Target Word Count:</strong> {post["word_count_target"]}<br>\n'
            
            if post['notes']:
                notes_preview = post['notes'][:150] + '...' if len(post['notes']) > 150 else post['notes']
                html += f'    <strong>Notes:</strong> {notes_preview}<br>\n'
            
            html += '  </div>\n'
            html += '</div>\n'
    
    # Footer
    html += """
        <div class="footer">
            <p>This report was automatically generated from Airtable data.</p>
            <p>To update the data, please visit your <a href="https://airtable.com/appfjLaSUBn8FUYYz/tblrH6OO1ulOnDS4S">Airtable Base</a></p>
        </div>
    </body>
    </html>
    """
    
    return html

def create_plain_text_email(posts):
    """Create plain text formatted email content."""
    # Group posts by date
    posts_by_date = defaultdict(list)
    for post in posts:
        posts_by_date[post['due_date']].append(post)
    
    # Statistics
    total_posts = len(posts)
    urgent_posts = len([p for p in posts if p['days_until_due'] <= 2])
    not_started = len([p for p in posts if p['status'] == 'Not Started'])
    
    text = "WEEKLY BLOG POST SCHEDULE\n"
    text += "=" * 60 + "\n\n"
    text += f"Report Generated: {datetime.now().strftime('%B %d, %Y at %I:%M %p')}\n\n"
    
    text += "SUMMARY\n"
    text += "-" * 30 + "\n"
    text += f"Total Posts Due: {total_posts}\n"
    text += f"Urgent (≤2 days): {urgent_posts}\n"
    text += f"Not Started: {not_started}\n\n"
    
    # Posts by date
    for date in sorted(posts_by_date.keys()):
        due_date = datetime.fromisoformat(date)
        date_str = due_date.strftime('%A, %B %d, %Y')
        days_until = (due_date.date() - datetime.now().date()).days
        
        text += "\n" + "=" * 60 + "\n"
        text += date_str
        if days_until <= 1:
            text += " [URGENT]"
        elif days_until <= 2:
            text += " [DUE SOON]"
        text += "\n" + "=" * 60 + "\n\n"
        
        for i, post in enumerate(posts_by_date[date], 1):
            text += f"{i}. {post['title']}\n"
            text += f"   Status: {post['status']}\n"
            text += f"   Priority: {post['priority']}\n"
            text += f"   Days Until Due: {post['days_until_due']}\n"
            
            if post['author'] != 'Unassigned':
                text += f"   Author: {post['author']}\n"
            
            if post['category']:
                text += f"   Category: {post['category']}\n"
            
            if post['word_count_target']:
                text += f"   Target Words: {post['word_count_target']}\n"
            
            if post['notes']:
                notes_preview = post['notes'][:100] + '...' if len(post['notes']) > 100 else post['notes']
                text += f"   Notes: {notes_preview}\n"
            
            text += "\n"
    
    text += "\n" + "-" * 60 + "\n"
    text += "This report was automatically generated from Airtable data.\n"
    text += "To update: https://airtable.com/appfjLaSUBn8FUYYz/tblrH6OO1ulOnDS4S\n"
    
    return text

def save_email_content(html_content, text_content):
    """Save email content to files for review."""
    # Save HTML version
    with open('email_content.html', 'w') as f:
        f.write(html_content)
    
    # Save text version
    with open('email_content.txt', 'w') as f:
        f.write(text_content)
    
    print("✅ Email content saved:")
    print("   - email_content.html (for HTML email)")
    print("   - email_content.txt (for plain text email)")

def create_email_draft():
    """Create a draft email with both HTML and plain text parts."""
    posts = load_blog_posts()
    
    # Create email content
    html_content = create_html_email(posts)
    text_content = create_plain_text_email(posts)
    
    # Save to files
    save_email_content(html_content, text_content)
    
    # Create MIME message
    msg = MIMEMultipart('alternative')
    msg['Subject'] = f"Weekly Blog Posts Due - {len(posts)} Posts This Week"
    msg['From'] = "your-email@example.com"  # Update this
    msg['To'] = "recipient@example.com"  # Update this
    
    # Attach parts
    text_part = MIMEText(text_content, 'plain')
    html_part = MIMEText(html_content, 'html')
    
    msg.attach(text_part)
    msg.attach(html_part)
    
    # Optionally attach the JSON file
    with open('blog_posts_due.json', 'rb') as f:
        attachment = MIMEBase('application', 'json')
        attachment.set_payload(f.read())
        encoders.encode_base64(attachment)
        attachment.add_header(
            'Content-Disposition',
            'attachment; filename="blog_posts_due.json"'
        )
        msg.attach(attachment)
    
    # Save the complete email message
    with open('email_draft.eml', 'wb') as f:
        f.write(msg.as_bytes())
    
    print("\n📧 Email draft created: email_draft.eml")
    print("   You can open this in your email client or copy the content")
    
    return msg

def create_gmail_url(posts):
    """Create a Gmail compose URL with the email content."""
    import urllib.parse
    
    text_content = create_plain_text_email(posts)
    
    # Create Gmail compose URL
    subject = f"Weekly Blog Posts Due - {len(posts)} Posts This Week"
    body = text_content[:1900]  # Gmail URL limit
    
    gmail_url = "https://mail.google.com/mail/?view=cm&fs=1"
    gmail_url += f"&su={urllib.parse.quote(subject)}"
    gmail_url += f"&body={urllib.parse.quote(body)}"
    
    print("\n🔗 Gmail Compose URL:")
    print("   Open this URL in your browser to compose the email in Gmail:")
    print(f"   {gmail_url[:100]}...")
    
    # Save full URL to file
    with open('gmail_compose_url.txt', 'w') as f:
        f.write(gmail_url)
    print("   Full URL saved to: gmail_compose_url.txt")

def main():
    """Main function to create email-ready content."""
    try:
        posts = load_blog_posts()
        print(f"\n📊 Processing {len(posts)} blog posts for email...")
        
        # Create and save email content
        html_content = create_html_email(posts)
        text_content = create_plain_text_email(posts)
        save_email_content(html_content, text_content)
        
        # Create email draft
        create_email_draft()
        
        # Create Gmail compose URL
        create_gmail_url(posts)
        
        print("\n✨ Email formatting complete!")
        print("\nYou can now:")
        print("1. Open 'email_content.html' in a browser to preview the HTML email")
        print("2. Copy 'email_content.txt' for plain text email")
        print("3. Open 'email_draft.eml' in your email client")
        print("4. Use the Gmail compose URL to send via Gmail")
        
    except FileNotFoundError:
        print("❌ Error: blog_posts_due.json not found.")
        print("Please run 'python3 fetch_and_export.py' first.")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()