import feedparser  # Assuming you are working with RSS feeds
import re  # For cleaning the title

# Function to clean the title to be used as a valid HTML element identifier
def clean_title(title):
    # Replace spaces with underscores and remove special characters
    cleaned_title = re.sub(r'[^\w\s]', '', title)  # Remove non-alphanumeric characters
    cleaned_title = cleaned_title.replace(" ", "_")  # Replace spaces with underscores
    return cleaned_title

# Function to check if any of the tags are in the text and highlight them
def highlight_tags(text, tags):
    text_lower = text.lower()  # Make search case-insensitive
    for tag in tags:
        tag_lower = tag.lower()
        # If the tag is found in the text, wrap it with <span> for highlighting
        if tag_lower in text_lower:
            # Use regular expressions to replace the tag with a highlighted version
            text = re.sub(f'(?i)({re.escape(tag)})', r'<span style="background-color: yellow; font-weight: bold;">\1</span>', text, flags=re.IGNORECASE)
    return text

# Function to scrape multiple feeds, filter results based on tags, and write to a single HTML file
def generate_combined_html_output(feed_urls, tags):
    try:
        # Start HTML structure for the combined file
        html_output = """
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Combined RSS Feed Results</title>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    background-color: #f9f9f9;
                    margin: 20px;
                }}
                h1 {{
                    color: #333;
                }}
                .feed-section {{
                    margin-bottom: 50px;
                }}
                .feed-section h2 {{
                    font-size: 2em;
                    color: #fff;
                    padding: 10px;
                    background-color: {color};
                }}
                p {{
                    font-size: 1.1em;
                    color: #555;
                }}
                a {{
                    color: #007BFF;
                    text-decoration: none;
                }}
                a:hover {{
                    text-decoration: underline;
                }}
                .entry {{
                    background-color: #fff;
                    border: 1px solid #ddd;
                    padding: 15px;
                    margin-bottom: 10px;
                    border-radius: 5px;
                    box-shadow: 0 0 5px rgba(0,0,0,0.1);
                }}
                .entry h3 {{
                    margin-top: 0;
                }}
                span {{
                    background-color: yellow;
                    font-weight: bold;
                }}
            </style>
        </head>
        <body>
            <h1>Combined RSS Feed Results</h1>
        """

        # Colors to differentiate feed sections
        colors = ['#1abc9c', '#3498db', '#e74c3c', '#9b59b6', '#f39c12', '#2ecc71']

        # Loop through each feed URL
        for i, feed_url in enumerate(feed_urls):
            # Parse the RSS feed
            feed = feedparser.parse(feed_url)

            # Check if feed has a title, otherwise use a fallback name
            if 'title' in feed.feed:
                feed_title = feed.feed.title
            else:
                feed_title = f"RSS_Feed_{i+1}"

            # Clean the feed title to use as an identifier
            feed_id = clean_title(feed_title)

            # Get color for this feed section (cycle through colors list)
            color = colors[i % len(colors)]

            # Add a section for this feed with a different background color
            html_output += f"""
            <div class="feed-section" id="{feed_id}">
                <h2 style="background-color: {color};">{feed_title}</h2>
            """

            # Loop through each entry in the feed
            for entry in feed.entries:
                title = entry.title
                link = entry.link
                summary = entry.summary if 'summary' in entry else ""

                # Highlight tags in title, summary, and link
                title_highlighted = highlight_tags(title, tags)
                summary_highlighted = highlight_tags(summary, tags) if summary else ""
                link_highlighted = highlight_tags(link, tags)

                # Check if the title, summary, or link contains any of the tags
                if (title_highlighted != title or summary_highlighted != summary or link_highlighted != link):
                    # Begin building the HTML block for this entry
                    entry_html = f"""
                    <div class="entry">
                        <h3>Title: {title_highlighted}</h3>
                        <p><strong>Link:</strong> <a href="{link}" target="_blank">{link_highlighted}</a></p>
                    """

                    # Add the summary if it exists
                    if summary_highlighted:
                        entry_html += f"<p><strong>Summary:</strong> {summary_highlighted}</p>"

                    # Close the div for the entry
                    entry_html += "</div>"

                    # Add this entry's HTML to the feed section
                    html_output += entry_html

            # Close the feed section
            html_output += "</div>"

        # Close the overall HTML structure
        html_output += """
        </body>
        </html>
        """

        # Write the combined HTML content to a single file
        with open("combined_feed_output.html", "w", encoding="utf-8") as file:
            file.write(html_output)

        print("Combined HTML file 'combined_feed_output.html' has been generated!")

    except Exception as e:
        print(f"An error occurred: {e}")

# List of URLs to process
urls = [
   "https://krebsonsecurity.com/feed/",
   "https://www.schneier.com/feed/atom/",
   "https://threatpost.com/feed/",
   "https://www.darkreading.com/rss.xml",
   "https://www.bleepingcomputer.com/feed/",
   "https://thehackernews.com/feeds/posts/default",
   "https://www.cyberscoop.com/feed/",
   "https://www.securityweek.com/rss.xml"
]

# List of tags to filter results (case-insensitive)
tags = [
    "cybersecurity", "vulnerability", "IT vulnerability", "OT vulnerability", "IOT vulnerability", " IT ", " OT ", " IOT ",
    "zero-day exploit", "zero-day vulnerability", "zero day exploit", "zero day",
    "data breach", "breach", "data leak", "data compromise",
    "malware", "malware attack", "virus", "trojan", "worm", "spyware", "adware",
    "ransomware", "ransomware incident", "ransom",
    "critical vulnerability", "critical IT vulnerability", "critical OT vulnerability", "critical IOT vulnerability",
    "cyber threat intelligence", " CTI ", "threat intelligence", "threat intel",
    "cyber forensics", "digital forensics", "forensics", "incident analysis",
    "security patch", "patch update", "security update", "patch", "update",
    "phishing", "phishing attack", "spear phishing", "email scam", "social engineering",
    "cloud security", "cloud breach", "cloud data breach", "cloud compromise", "cloud hack"
]

# Generate combined HTML output for all URLs
generate_combined_html_output(urls, tags)
