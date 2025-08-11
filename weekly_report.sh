#!/bin/bash
# Weekly Blog Report Script
# Runs every Sunday night to fetch and email blog posts

# Change to the project directory
cd /Users/chuckaikens/Projects/claude-code/weekly-blog-post

# Log the start time
echo "=====================================" >> weekly_report.log
echo "Starting weekly report: $(date)" >> weekly_report.log

# Fetch latest posts from Airtable
echo "Fetching posts from Airtable..." >> weekly_report.log
/usr/bin/python3 fetch_and_export.py >> weekly_report.log 2>&1

# Send email report
echo "Sending email report..." >> weekly_report.log
/usr/bin/python3 send_test.py >> weekly_report.log 2>&1

# Log completion
echo "Report completed: $(date)" >> weekly_report.log
echo "=====================================" >> weekly_report.log
echo "" >> weekly_report.log