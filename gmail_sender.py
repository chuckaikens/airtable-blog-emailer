#!/usr/bin/env python3
"""
Send blog post reports via Gmail using Google Workspace.
Supports both App Passwords and OAuth2 authentication.
"""

import os
import json
import smtplib
import ssl
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from dotenv import load_dotenv
from email_formatter import create_html_email, create_plain_text_email, load_blog_posts

# Load environment variables
load_dotenv()


class GmailSender:
    """Handle sending emails via Gmail SMTP."""
    
    def __init__(self):
        """Initialize Gmail sender with credentials from environment."""
        self.smtp_server = "smtp.gmail.com"
        self.port = 587  # For TLS
        
        # Get credentials from environment
        self.sender_email = os.getenv('GMAIL_SENDER_EMAIL')
        self.sender_password = os.getenv('GMAIL_APP_PASSWORD')  # App Password, not regular password
        self.sender_name = os.getenv('GMAIL_SENDER_NAME', 'Blog Report System')
        
        if not self.sender_email or not self.sender_password:
            raise ValueError(
                "Missing Gmail credentials. Please set GMAIL_SENDER_EMAIL and GMAIL_APP_PASSWORD in .env\n"
                "Note: You must use an App Password, not your regular Gmail password.\n"
                "See: https://support.google.com/accounts/answer/185833"
            )
    
    def create_message(self, recipient_email, subject=None, cc_emails=None, bcc_emails=None):
        """
        Create the email message with blog post content.
        
        Args:
            recipient_email: Primary recipient email address
            subject: Optional custom subject line
            cc_emails: Optional list of CC recipients
            bcc_emails: Optional list of BCC recipients
        """
        # Load blog posts
        posts = load_blog_posts()
        
        # Create content
        html_content = create_html_email(posts)
        text_content = create_plain_text_email(posts)
        
        # Count statistics for subject
        urgent_count = len([p for p in posts if p['days_until_due'] <= 2])
        
        # Create message
        msg = MIMEMultipart('alternative')
        
        # Set headers
        if not subject:
            if urgent_count > 0:
                subject = f"🔴 {urgent_count} URGENT Posts Due - Weekly Blog Schedule ({len(posts)} total)"
            else:
                subject = f"Weekly Blog Schedule - {len(posts)} Posts Due This Week"
        
        msg['Subject'] = subject
        msg['From'] = f"{self.sender_name} <{self.sender_email}>"
        msg['To'] = recipient_email
        msg['Date'] = datetime.now().strftime('%a, %d %b %Y %H:%M:%S %z')
        
        # Add CC if provided
        if cc_emails:
            if isinstance(cc_emails, list):
                msg['Cc'] = ', '.join(cc_emails)
            else:
                msg['Cc'] = cc_emails
        
        # Add custom headers
        msg['X-Priority'] = '2' if urgent_count > 5 else '3'  # High priority if many urgent posts
        msg['X-Mailer'] = 'Blog Post Reporter via Python'
        
        # Attach text and HTML parts
        text_part = MIMEText(text_content, 'plain')
        html_part = MIMEText(html_content, 'html')
        
        msg.attach(text_part)
        msg.attach(html_part)
        
        # Optionally attach JSON data
        if os.getenv('GMAIL_ATTACH_JSON', 'false').lower() == 'true':
            with open('blog_posts_due.json', 'rb') as f:
                attachment = MIMEBase('application', 'json')
                attachment.set_payload(f.read())
                encoders.encode_base64(attachment)
                attachment.add_header(
                    'Content-Disposition',
                    f'attachment; filename="blog_posts_{datetime.now().strftime("%Y%m%d")}.json"'
                )
                msg.attach(attachment)
        
        return msg, posts
    
    def send_email(self, recipient_email, subject=None, cc_emails=None, bcc_emails=None, test_mode=False):
        """
        Send the email via Gmail SMTP.
        
        Args:
            recipient_email: Primary recipient
            subject: Optional custom subject
            cc_emails: Optional CC recipients
            bcc_emails: Optional BCC recipients
            test_mode: If True, prepare but don't send
        """
        try:
            # Create message
            msg, posts = self.create_message(recipient_email, subject, cc_emails, bcc_emails)
            
            if test_mode:
                print("📧 TEST MODE - Email prepared but not sent")
                print(f"   From: {msg['From']}")
                print(f"   To: {msg['To']}")
                if msg.get('Cc'):
                    print(f"   CC: {msg['Cc']}")
                print(f"   Subject: {msg['Subject']}")
                print(f"   Posts included: {len(posts)}")
                return True
            
            # Create secure SSL context
            context = ssl.create_default_context()
            
            # Connect and send
            print(f"📧 Connecting to Gmail SMTP server...")
            
            with smtplib.SMTP(self.smtp_server, self.port) as server:
                server.starttls(context=context)
                server.login(self.sender_email, self.sender_password)
                
                # Prepare all recipients
                recipients = [recipient_email]
                if cc_emails:
                    if isinstance(cc_emails, list):
                        recipients.extend(cc_emails)
                    else:
                        recipients.append(cc_emails)
                if bcc_emails:
                    if isinstance(bcc_emails, list):
                        recipients.extend(bcc_emails)
                    else:
                        recipients.append(bcc_emails)
                
                # Send email
                server.send_message(msg, to_addrs=recipients)
                
                print(f"✅ Email sent successfully!")
                print(f"   From: {self.sender_email}")
                print(f"   To: {recipient_email}")
                if cc_emails:
                    print(f"   CC: {cc_emails}")
                if bcc_emails:
                    print(f"   BCC: {bcc_emails}")
                print(f"   Subject: {msg['Subject']}")
                print(f"   Posts included: {len(posts)}")
                
                # Log the send
                self._log_send(recipient_email, len(posts))
                
                return True
                
        except smtplib.SMTPAuthenticationError:
            print("❌ Authentication failed!")
            print("   Please check:")
            print("   1. Your email address is correct")
            print("   2. You're using an App Password (not your regular password)")
            print("   3. 2-Step Verification is enabled on your Google account")
            print("\n   To create an App Password:")
            print("   1. Go to https://myaccount.google.com/apppasswords")
            print("   2. Select 'Mail' and your device")
            print("   3. Copy the 16-character password")
            print("   4. Add it to .env as GMAIL_APP_PASSWORD (no spaces)")
            return False
            
        except Exception as e:
            print(f"❌ Error sending email: {e}")
            return False
    
    def _log_send(self, recipient, post_count):
        """Log successful email sends."""
        log_file = 'email_send_log.json'
        
        # Load existing log or create new
        if os.path.exists(log_file):
            with open(log_file, 'r') as f:
                log = json.load(f)
        else:
            log = []
        
        # Add new entry
        log.append({
            'timestamp': datetime.now().isoformat(),
            'recipient': recipient,
            'post_count': post_count,
            'sender': self.sender_email
        })
        
        # Save log
        with open(log_file, 'w') as f:
            json.dump(log, f, indent=2)
    
    def send_to_multiple(self, recipients, subject=None):
        """
        Send to multiple recipients individually.
        
        Args:
            recipients: List of email addresses
            subject: Optional custom subject
        """
        successful = []
        failed = []
        
        for recipient in recipients:
            print(f"\n📧 Sending to {recipient}...")
            if self.send_email(recipient, subject):
                successful.append(recipient)
            else:
                failed.append(recipient)
        
        # Summary
        print("\n" + "=" * 50)
        print("📊 SENDING SUMMARY")
        print("=" * 50)
        print(f"✅ Successful: {len(successful)}")
        for email in successful:
            print(f"   • {email}")
        
        if failed:
            print(f"\n❌ Failed: {len(failed)}")
            for email in failed:
                print(f"   • {email}")
        
        return successful, failed


def interactive_send():
    """Interactive mode for sending emails."""
    print("\n📧 GMAIL BLOG POST SENDER")
    print("=" * 50)
    
    try:
        sender = GmailSender()
        print(f"✅ Logged in as: {sender.sender_email}")
        
        # Get recipient
        print("\nWho should receive the blog post report?")
        recipient = input("Recipient email: ").strip()
        
        if not recipient:
            print("❌ No recipient provided")
            return
        
        # Optional CC
        cc_input = input("CC emails (comma-separated, or press Enter to skip): ").strip()
        cc_emails = [e.strip() for e in cc_input.split(',')] if cc_input else None
        
        # Optional custom subject
        custom_subject = input("Custom subject (press Enter for default): ").strip()
        subject = custom_subject if custom_subject else None
        
        # Confirm before sending
        print("\n📋 READY TO SEND:")
        print(f"   To: {recipient}")
        if cc_emails:
            print(f"   CC: {', '.join(cc_emails)}")
        print(f"   Subject: {subject or 'Default (based on urgency)'}")
        
        confirm = input("\nSend email? (y/n): ").lower()
        
        if confirm == 'y':
            sender.send_email(recipient, subject, cc_emails)
        else:
            print("📧 Email cancelled")
            
    except ValueError as e:
        print(f"❌ Configuration Error: {e}")
    except KeyboardInterrupt:
        print("\n\n📧 Email cancelled")
    except Exception as e:
        print(f"❌ Error: {e}")


def automated_send():
    """Automated sending using configuration from environment."""
    try:
        sender = GmailSender()
        
        # Get recipients from environment
        recipients = os.getenv('GMAIL_AUTO_RECIPIENTS', '').split(',')
        recipients = [r.strip() for r in recipients if r.strip()]
        
        if not recipients:
            print("❌ No recipients configured in GMAIL_AUTO_RECIPIENTS")
            return
        
        print(f"📧 Automated sending to {len(recipients)} recipient(s)")
        
        # Send to all recipients
        sender.send_to_multiple(recipients)
        
    except Exception as e:
        print(f"❌ Error in automated send: {e}")


def main():
    """Main function with mode selection."""
    import sys
    
    # Check for command line arguments
    if len(sys.argv) > 1:
        mode = sys.argv[1].lower()
        
        if mode == 'auto':
            automated_send()
        elif mode == 'test':
            # Test mode - prepare but don't send
            try:
                sender = GmailSender()
                test_email = sys.argv[2] if len(sys.argv) > 2 else "test@example.com"
                sender.send_email(test_email, test_mode=True)
            except Exception as e:
                print(f"❌ Test failed: {e}")
        elif mode == 'help':
            print("Usage:")
            print("  python3 gmail_sender.py          # Interactive mode")
            print("  python3 gmail_sender.py auto     # Automated send to configured recipients")
            print("  python3 gmail_sender.py test     # Test mode (prepare but don't send)")
            print("  python3 gmail_sender.py help     # Show this help")
        else:
            print(f"Unknown mode: {mode}")
            print("Use 'python3 gmail_sender.py help' for usage")
    else:
        # Default to interactive mode
        interactive_send()


if __name__ == "__main__":
    main()