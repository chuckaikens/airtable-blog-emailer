# Gmail Setup Guide for Blog Post Reports

## 🔐 Setting Up Google App Password

Since you're using Google Workspace, you'll need to create an App Password for secure email sending. Regular passwords won't work due to security restrictions.

### Step 1: Enable 2-Step Verification (if not already enabled)

1. Go to your Google Account settings: https://myaccount.google.com/security
2. Click on "2-Step Verification"
3. Follow the prompts to enable it

### Step 2: Create an App Password

1. Go to: https://myaccount.google.com/apppasswords
2. You may need to sign in again
3. Select app: Choose **"Mail"**
4. Select device: Choose **"Other (Custom name)"**
5. Enter a name like: **"Blog Report Sender"**
6. Click **"Generate"**
7. You'll see a 16-character password like: `abcd efgh ijkl mnop`
8. **IMPORTANT**: Copy this password immediately (you won't be able to see it again)

### Step 3: Configure the .env File

Edit your `.env` file and update these values:

```bash
# Your Google Workspace email
GMAIL_SENDER_EMAIL=yourname@yourcompany.com

# The 16-character App Password (remove spaces)
GMAIL_APP_PASSWORD=abcdefghijklmnop

# Optional: How the sender name appears
GMAIL_SENDER_NAME=Blog Report System

# Optional: Attach JSON data file
GMAIL_ATTACH_JSON=false

# Optional: Recipients for automated sending
GMAIL_AUTO_RECIPIENTS=manager@company.com,team@company.com
```

## 📧 Using the Gmail Sender

### Interactive Mode (Default)
```bash
python3 gmail_sender.py
```
This will prompt you for:
- Recipient email
- Optional CC recipients
- Optional custom subject line

### Test Mode
```bash
python3 gmail_sender.py test
```
Prepares the email but doesn't send it (useful for testing configuration)

### Automated Mode
```bash
python3 gmail_sender.py auto
```
Sends to all recipients listed in `GMAIL_AUTO_RECIPIENTS`

### Help
```bash
python3 gmail_sender.py help
```

## 🚀 Complete Workflow

### One-Time Setup
```bash
# 1. Install dependencies
pip3 install -r requirements.txt

# 2. Configure .env with your credentials
# 3. Test the configuration
python3 gmail_sender.py test
```

### Daily/Weekly Use
```bash
# 1. Fetch latest posts from Airtable
python3 fetch_and_export.py

# 2. Send the email report
python3 gmail_sender.py
```

### Automated Workflow (for cron/scheduler)
```bash
# Create a single script that does both
python3 fetch_and_export.py && python3 gmail_sender.py auto
```

## 📅 Setting Up Automated Daily/Weekly Reports

### macOS (using crontab)
```bash
# Edit crontab
crontab -e

# Add this line for daily reports at 9 AM
0 9 * * * cd /Users/chuckaikens/Projects/claude-code/weekly-blog-post && /usr/bin/python3 fetch_and_export.py && /usr/bin/python3 gmail_sender.py auto

# Or weekly on Mondays at 9 AM
0 9 * * 1 cd /Users/chuckaikens/Projects/claude-code/weekly-blog-post && /usr/bin/python3 fetch_and_export.py && /usr/bin/python3 gmail_sender.py auto
```

### Using a Shell Script
Create `send_report.sh`:
```bash
#!/bin/bash
cd /Users/chuckaikens/Projects/claude-code/weekly-blog-post
python3 fetch_and_export.py
python3 gmail_sender.py auto
```

Make it executable:
```bash
chmod +x send_report.sh
```

## 🔍 Troubleshooting

### "Authentication failed" Error
1. Make sure you're using an App Password, not your regular password
2. Verify 2-Step Verification is enabled
3. Check that the App Password was copied correctly (no spaces)
4. Try generating a new App Password

### "Less secure app access" Message
- This is normal when using App Passwords
- Google Workspace may require admin approval for SMTP access
- Contact your Google Workspace admin if needed

### Email Not Sending
1. Check your internet connection
2. Verify the recipient email is correct
3. Check spam/junk folders
4. Try test mode first: `python3 gmail_sender.py test`

### Email Goes to Spam
- This can happen with automated emails
- Ask recipients to mark as "Not Spam"
- Add your sender email to their contacts

## 📊 Viewing Send History

The script logs all successful sends to `email_send_log.json`:
```bash
cat email_send_log.json
```

## 🔒 Security Notes

1. **Never commit your .env file** - It's already in .gitignore
2. **App Passwords are powerful** - Keep them secure
3. **Rotate App Passwords periodically** - Every 3-6 months
4. **Use different App Passwords** for different applications
5. **Revoke App Passwords** you're no longer using

## 💡 Tips

1. **Test first**: Always use test mode when setting up
2. **Start small**: Test with your own email before sending to others
3. **Check formatting**: Open `email_content.html` in a browser to preview
4. **Monitor logs**: Check `email_send_log.json` to verify sends
5. **Be mindful of frequency**: Don't spam - weekly is usually enough

## 📝 Example Session

```bash
# 1. Fetch latest data
$ python3 fetch_and_export.py
🔍 Fetching blog posts from Airtable...
✅ Exported 18 posts to blog_posts_due.json

# 2. Send interactively
$ python3 gmail_sender.py
📧 GMAIL BLOG POST SENDER
==================================================
✅ Logged in as: yourname@company.com

Who should receive the blog post report?
Recipient email: manager@company.com
CC emails (comma-separated, or press Enter to skip): team@company.com
Custom subject (press Enter for default): 

📋 READY TO SEND:
   To: manager@company.com
   CC: team@company.com
   Subject: Default (based on urgency)

Send email? (y/n): y
📧 Connecting to Gmail SMTP server...
✅ Email sent successfully!
   From: yourname@company.com
   To: manager@company.com
   CC: team@company.com
   Subject: 🔴 11 URGENT Posts Due - Weekly Blog Schedule (18 total)
   Posts included: 18
```