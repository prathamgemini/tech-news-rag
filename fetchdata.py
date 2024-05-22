import requests
import os
from datetime import datetime
from bs4 import BeautifulSoup

api_key = os.environ.get("GUARDIAN_API_KEY")


# Set the base URL for the API
base_url = "http://content.guardianapis.com/search"

# Define the initial query parameters
params = {
    "api-key": api_key,
    "show-fields": "headline,bodyText,webPublicationDate,thumbnail,multimedia",  # Include multimedia field
    "page-size": 200,  # Number of results per page (maximum is 200)
    "from-date": "2023-05-01",  # Start date for the articles (YYYY-MM-DD)
    "order-by": "oldest",  # Order the results by oldest first
    "section": "technology",  # Limit the results to the technology section
    "tag": "technology/technology",  # Limit the results to articles with the technology tag
    "show-elements": "all"  # Include media elements
}

# Create directories to store the articles and media files
os.makedirs("corpus", exist_ok=True)
os.makedirs("media", exist_ok=True)

# Keep track of unique headlines
unique_headlines = set()

# Load existing headlines from the corpus folder
corpus_dir = "corpus"
for filename in os.listdir(corpus_dir):
    if filename.endswith(".html"):
        with open(os.path.join(corpus_dir, filename), "r", encoding="utf-8") as f:
            html = f.read()
            soup = BeautifulSoup(html, "html.parser")
            headline = soup.find("h1").text
            unique_headlines.add(headline)

# Send the initial API request
response = requests.get(base_url, params=params)
data = response.json()

# Extract the initial set of articles and total number of pages
articles = data["response"]["results"]
total_pages = data["response"]["pages"]

# Create a list to store all articles
all_articles = articles

# Fetch additional pages if available
current_page = 2
while current_page <= total_pages:
    params["page"] = current_page
    response = requests.get(base_url, params=params)
    data = response.json()
    articles = data["response"]["results"]
    all_articles.extend(articles)
    current_page += 1

for i, article in enumerate(all_articles, start=1):
    headline = article["fields"]["headline"]
    # Check if the headline is unique
    if headline in unique_headlines:
        print(f"Skipping duplicate article: {headline}")
        continue
    unique_headlines.add(headline)

    body_text = article["fields"]["bodyText"]
    publication_date = article["webPublicationDate"]
    publication_date = datetime.strptime(publication_date, "%Y-%m-%dT%H:%M:%SZ").strftime("%Y-%m-%d")
    thumbnail_url = article["fields"].get("thumbnail")
    multimedia = article["fields"].get("multimedia")

    # Fetch additional metadata
 
    section = article["sectionName"]
    article_url = article["webUrl"]

    article_html = requests.get(article_url).text
    soup = BeautifulSoup(article_html, "html.parser")
    author_link = soup.find("a", rel="author")
    if author_link:
        author_name = author_link.text
    else:
        author_name = "Unknown"

    tag_list = soup.find("ul", class_="dcr-1yfsxuc")
    if tag_list:
        tags = [tag.text.strip() for tag in tag_list.find_all("a")]
    else:
        tags = []
        

    filename = f"corpus/article_{i}.html"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(f"<!DOCTYPE html>\n<html>\n<head>\n<title>{headline}</title>\n</head>\n<body>\n")
        f.write(f"<h1>{headline}</h1>\n")
        f.write(f"<p>Publication Date: {publication_date}</p>\n")
        # f.write(f"<p>Author(s): {', '.join(author_names)}</p>\n")
        f.write(f"<p>Author: {author_name}</p>\n")

        f.write(f"<p>Section: {section}</p>\n")
        f.write(f"<p>Tags: {', '.join(tags)}</p>\n")
        f.write(f"<p>Article URL: <a href='{article_url}' target='_blank'>{article_url}</a></p>\n")
        if thumbnail_url:
            f.write(f"<img src='{thumbnail_url}' alt='Article Image'>\n")
        f.write(f"<p>{body_text}</p>\n")
        if multimedia:
            f.write("<h2>Media</h2>\n")
            for media in multimedia:
                media_type = media.get("type")
                media_url = media.get("url")
                if media_type == "image":
                    f.write(f"<img src='{media_url}' alt='Article Image'>\n")
                elif media_type == "video":
                    f.write(f"<video controls>\n<source src='{media_url}' type='video/mp4'>\n</video>\n")
                elif media_type == "audio":
                    f.write(f"<audio controls>\n<source src='{media_url}' type='audio/mpeg'>\n</audio>\n")
        f.write("</body>\n</html>")
        print(f"Saved article {i} to {filename}")