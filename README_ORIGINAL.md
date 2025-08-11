# Airtable Blog Post Fetcher

A Python script that connects to Airtable via API to fetch blog posts due within the next 7 days.

## Features

- 🔗 Connects to Airtable using their REST API
- 📅 Filters blog posts with due dates in the next 7 days
- 📊 Displays posts in a formatted, easy-to-read manner
- 💾 Option to export results to JSON
- 🔒 Secure credential management using environment variables

## Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure Airtable Credentials

1. Copy the example environment file:
   ```bash
   cp .env.example .env
   ```

2. Edit `.env` and add your Airtable credentials:
   - **AIRTABLE_API_KEY**: Get from [Airtable Token Creation](https://airtable.com/create/tokens)
   - **AIRTABLE_BASE_ID**: Found in your base's API documentation (format: `appXXXXXXXXXXXXXX`)
   - **AIRTABLE_TABLE_NAME**: Name of your table (defaults to "Blog Posts")
   - **AIRTABLE_DUE_DATE_FIELD**: Name of your due date field (defaults to "Due Date")

### 3. Airtable Setup

Ensure your Airtable base has a table with at least these fields:
- **Title** (Single line text)
- **Due Date** (Date field)
- **Status** (Single select/text)
- **Author** (Single line text)

Optional fields that will be displayed if present:
- **Category** (Single select/text)
- **Notes** (Long text)
- **Word Count Target** (Number)
- **Priority** (Single select)

## Usage

Run the script:

```bash
python airtable_blog_fetcher.py
```

The script will:
1. Connect to your Airtable base
2. Fetch all blog posts due in the next 7 days
3. Display them sorted by due date
4. Optionally export to a JSON file

## API Token Permissions

When creating your Airtable API token, ensure it has:
- **data.records:read** scope for the base you want to access

## Output Example

```
📝 Blog Posts Due This Week (3 total)
============================================================

📌 How to Use Python with APIs
   Due: 2024-01-15 (2 days)
   Status: In Progress
   Author: John Doe
   Priority: High
   Category: Technical
   Target Word Count: 1500

📌 Marketing Strategy for Q1
   Due: 2024-01-17 (4 days)
   Status: Not Started
   Author: Jane Smith
   Priority: Medium
   Category: Marketing
============================================================
```

## Troubleshooting

### Common Issues

1. **"Missing required environment variables"**
   - Ensure your `.env` file exists and contains valid credentials

2. **"Error fetching data from Airtable"**
   - Verify your API key has proper permissions
   - Check that the base ID and table name are correct
   - Ensure your date field name matches the configuration

3. **No posts showing up**
   - Check that you have posts with due dates in the next 7 days
   - Verify the date field name in your `.env` matches your Airtable schema

## Customization

### Adjusting the Date Range

To change from 7 days to a different range, modify line 44 in `airtable_blog_fetcher.py`:
```python
week_from_now = today + timedelta(days=14)  # For 14 days
```

### Adding Custom Fields

To fetch additional fields from your Airtable, modify the `_process_records` method to include your custom fields:
```python
'custom_field': fields.get('Your Field Name', 'Default Value'),
```

## License

MIT