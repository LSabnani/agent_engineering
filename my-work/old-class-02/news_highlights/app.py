import os
import requests
import xml.etree.ElementTree as ET
from flask import Flask, jsonify, render_template, request

app = Flask(__name__)

# Topic mapping for Google News RSS feeds using headlines section topic pattern
TOPIC_FEEDS = {
    "top": "https://news.google.com/rss?hl=en-US&gl=US&ceid=US:en",
    "world": "https://news.google.com/rss/headlines/section/topic/WORLD?hl=en-US&gl=US&ceid=US:en",
    "business": "https://news.google.com/rss/headlines/section/topic/BUSINESS?hl=en-US&gl=US&ceid=US:en",
    "technology": "https://news.google.com/rss/headlines/section/topic/TECHNOLOGY?hl=en-US&gl=US&ceid=US:en",
    "sports": "https://news.google.com/rss/headlines/section/topic/SPORTS?hl=en-US&gl=US&ceid=US:en",
    "science": "https://news.google.com/rss/headlines/section/topic/SCIENCE?hl=en-US&gl=US&ceid=US:en",
    "health": "https://news.google.com/rss/headlines/section/topic/HEALTH?hl=en-US&gl=US&ceid=US:en"
}

SEARCH_FEED_URL = "https://news.google.com/rss/search?q={query}&hl=en-US&gl=US&ceid=US:en"

@app.route('/')
def home():
    """Renders the dashboard homepage."""
    return render_template('index.html')

@app.route('/api/news', methods=['GET'])
def get_news():
    """
    Fetches news from Google News RSS based on topic or search query.
    Returns parsed JSON array of articles.
    """
    topic = request.args.get('topic', 'top').lower()
    query = request.args.get('q', '').strip()

    # Determine which URL to fetch from
    if query:
        feed_url = SEARCH_FEED_URL.format(query=requests.utils.quote(query))
    else:
        feed_url = TOPIC_FEEDS.get(topic, TOPIC_FEEDS["top"])

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
    }

    try:
        response = requests.get(feed_url, headers=headers, timeout=10)
        if response.status_code != 200:
            return jsonify({
                "status": "error",
                "message": f"Failed to retrieve feed. Status code: {response.status_code}"
            }), response.status_code

        # Parse XML
        root = ET.fromstring(response.content)
        articles = []

        for item in root.findall(".//item"):
            title_el = item.find("title")
            link_el = item.find("link")
            pub_date_el = item.find("pubDate")
            source_el = item.find("source")

            title = title_el.text if title_el is not None else "No Title"
            url = link_el.text if link_el is not None else "#"
            pub_date = pub_date_el.text if pub_date_el is not None else ""
            source = source_el.text if source_el is not None else "Google News"

            # Parse publisher out of the title if present
            # Google news title format: "Headline Text - Publisher Name"
            headline = title
            publisher = source
            if " - " in title:
                parts = title.rsplit(" - ", 1)
                # Ensure the last part isn't empty and matches roughly what we expect
                if len(parts) == 2 and len(parts[1].strip()) > 0:
                    headline = parts[0].strip()
                    publisher = parts[1].strip()

            articles.append({
                "title": headline,
                "url": url,
                "published": pub_date,
                "source": publisher
            })

        return jsonify({
            "status": "success",
            "topic": topic if not query else f"search: {query}",
            "count": len(articles),
            "articles": articles
        })

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

if __name__ == '__main__':
    # Run the webapp locally on port 5000
    app.run(host='127.0.0.1', port=5000, debug=True)
