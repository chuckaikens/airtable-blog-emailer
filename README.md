# 📧 Airtable Blog Post Email Automation

Automatically fetch blog posts from Airtable and send beautifully formatted email reports via Gmail. Perfect for content managers, editorial teams, and anyone tracking deadlines in Airtable.

![Python](https://img.shields.io/badge/python-3.9%2B-blue)
![Airtable](https://img.shields.io/badge/Airtable-API-18BFFF)
![Gmail](https://img.shields.io/badge/Gmail-SMTP-EA4335)

## ✨ Features

- 🔗 **Airtable Integration**: Fetches posts with due dates from your Airtable base
- 📅 **Smart Filtering**: Automatically finds posts due in the next 7 days
- 📧 **Professional Emails**: Sends HTML-formatted emails with urgency indicators
- 🚨 **Priority Highlighting**: Color-codes urgent posts (red for <2 days, yellow for soon)
- 📊 **Multiple Export Formats**: JSON, CSV, Markdown, HTML, and plain text
- 🔐 **Secure**: Uses environment variables for credentials (never committed to git)
- ⏰ **Schedulable**: Can be automated with cron for weekly reports

## 📸 Example Output

The email report includes:
- Summary statistics (total posts, urgent items, status)
- Posts organized by due date
- Visual urgency indicators
- Mobile-responsive HTML design

## 🚀 Quick Start

### Prerequisites

- Python 3.9+
- Airtable account with a base containing blog posts
- Gmail account with 2-Step Verification enabled
- Google App Password for Gmail SMTP

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/airtable-blog-emailer.git
cd airtable-blog-emailer
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Set up credentials**
```bash
# Copy the example environment file
cp .env.example .env

# Edit .env with your credentials
nano .env  # or use your preferred editor
```

4. **Configure your credentials in `.env`**
```env
# Airtable Settings
AIRTABLE_API_KEY=patXXXXX.XXXXXXXXX  # Personal Access Token
AIRTABLE_BASE_ID=appXXXXXXXXXXXXX    # Your base ID
AIRTABLE_TABLE_NAME=tblXXXXXXXXXX    # Your table name/ID
AIRTABLE_DUE_DATE_FIELD=Due Date     # Your date field name

# Gmail Settings
GMAIL_SENDER_EMAIL=you@company.com
GMAIL_APP_PASSWORD=xxxx xxxx xxxx xxxx  # 16-char app password
```

## 📖 Usage

### Basic Usage

1. **Fetch posts from Airtable**
```bash
python3 fetch_and_export.py
```

2. **Send email report**
```bash
python3 gmail_sender.py
```

3. **All-in-one command**
```bash
python3 fetch_and_export.py && python3 gmail_sender.py
```

### Advanced Usage

**Parse and analyze posts:**
```bash
python3 parse_blog_posts.py  # Creates CSV, Markdown, and filtered JSON
```

**Test email without sending:**
```bash
python3 gmail_sender.py test
```

**Send to multiple recipients automatically:**
```bash
# Add to .env:
# GMAIL_AUTO_RECIPIENTS=manager@company.com,team@company.com

python3 gmail_sender.py auto
```

**Create email content without sending:**
```bash
python3 email_formatter.py  # Generates HTML and text versions
```

## 🔑 Setting Up Credentials

### Airtable Personal Access Token

1. Go to [Airtable Token Creation](https://airtable.com/create/tokens)
2. Click "Create new token"
3. Add scope: `data.records:read`
4. Add your specific base to the access list
5. Copy the token (starts with `pat`)

### Gmail App Password

1. Enable [2-Step Verification](https://myaccount.google.com/security) on your Google account
2. Go to [App Passwords](https://myaccount.google.com/apppasswords)
3. Select "Mail" and "Other (Custom name)"
4. Name it "Blog Report Sender"
5. Copy the 16-character password

## 📅 Scheduling Automated Reports

### macOS/Linux (using cron)

```bash
# Edit crontab
crontab -e

# Add this line for weekly reports on Sunday at 9 PM
0 21 * * 0 cd /path/to/project && python3 fetch_and_export.py && python3 gmail_sender.py auto
```

### Using the included shell script

```bash
# Make executable
chmod +x weekly_report.sh

# Test it
./weekly_report.sh

# Add to cron for Sunday nights at 8 PM
0 20 * * 0 /path/to/project/weekly_report.sh
```

## 📁 Project Structure

```
.
├── airtable_blog_fetcher.py  # Core Airtable API integration
├── email_formatter.py         # HTML/text email formatting
├── gmail_sender.py           # Gmail SMTP sender
├── parse_blog_posts.py       # Data parsing and export utilities
├── fetch_and_export.py       # Quick fetch and export script
├── send_test.py             # Simple test sender
├── weekly_report.sh         # Automation shell script
├── requirements.txt         # Python dependencies
├── .env.example            # Template for credentials
├── .gitignore             # Protects sensitive files
└── README.md              # This file
```

## 🛡️ Security

- **Never commit `.env`** - It's gitignored by default
- **Use App Passwords** - Never use your real Gmail password
- **Rotate credentials** - Change App Passwords every 3-6 months
- **Check before committing** - Always run `git status` first

## 🎨 Customization

### Adjust the date range (default: 7 days)

Edit `airtable_blog_fetcher.py` line 44:
```python
week_from_now = today + timedelta(days=14)  # Change to 14 days
```

### Add custom Airtable fields

Edit the `_process_records` method in `airtable_blog_fetcher.py`:
```python
'custom_field': fields.get('Your Field Name', 'Default'),
```

### Change email styling

Edit the HTML template in `email_formatter.py` to match your brand colors and styling.

## 🐛 Troubleshooting

| Issue | Solution |
|-------|----------|
| "Authentication failed" | Ensure you're using an App Password, not your Gmail password |
| "No posts showing" | Check your date field name matches `AIRTABLE_DUE_DATE_FIELD` |
| "401 Unauthorized" | Your Airtable token may be expired or incorrect |
| Email goes to spam | Ask recipients to mark as "Not Spam" and add sender to contacts |

## 📝 Examples

### Filter urgent posts only
```python
from airtable_blog_fetcher import AirtableBlogFetcher

fetcher = AirtableBlogFetcher()
posts = fetcher.get_posts_due_this_week()
urgent = [p for p in posts if p['days_until_due'] <= 2]
print(f"Found {len(urgent)} urgent posts")
```

### Send with custom subject
```python
from gmail_sender import GmailSender

sender = GmailSender()
sender.send_email(
    "manager@company.com",
    subject="⚠️ Editorial Calendar - Immediate Action Required",
    cc_emails=["editor@company.com"]
)
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- Built with [Airtable API](https://airtable.com/developers/web/api/introduction)
- Email sending via [Gmail SMTP](https://support.google.com/mail/answer/7126229)
- Inspired by the need for better editorial calendar management

## 💡 Future Enhancements

- [ ] Slack integration for notifications
- [ ] Microsoft Teams webhook support
- [ ] Custom email templates
- [ ] Dashboard web interface
- [ ] Support for multiple Airtable bases
- [ ] Automatic status updates back to Airtable

## 📧 Support

For issues, questions, or suggestions, please open an issue on GitHub.

---

Made with ❤️ for content teams everywhere