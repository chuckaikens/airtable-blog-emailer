#!/usr/bin/env python3
"""Quick test send to your email."""

from gmail_sender import GmailSender

# Send test email
sender = GmailSender()
sender.send_email("cia@tymoo.com", subject="Test: Blog Post Report")