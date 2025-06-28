import requests
from bs4 import BeautifulSoup
from datetime import datetime
import xml.etree.ElementTree as ET

BASE_URL = "https://www.nascollege.org"
NOTICES_URL = f"{BASE_URL}/all-notices.php"

def fetch_notices():
    response = requests.get(NOTICES_URL)
    soup = BeautifulSoup(response.content, 'html.parser')
    notices = []

    links = soup.find_all("a", class_="news_caption")

    for link in links:
        title = link.get_text(strip=True)
        href = link.get("href", "")
        full_url = BASE_URL + "/" + href.lstrip("../").lstrip("/")

        pub_date = datetime.utcnow().strftime("%a, %d %b %Y %H:%M:%S GMT")

        notices.append({
            "title": title,
            "link": full_url,
            "pubDate": pub_date
        })

    return notices[:20]  # ✅ Limit to 20

def generate_rss(notices, output_file="nas_college_feed.xml"):
    rss = ET.Element("rss", version="2.0")
    channel = ET.SubElement(rss, "channel")

    ET.SubElement(channel, "title").text = "NAS College Meerut - Notices"
    ET.SubElement(channel, "link").text = NOTICES_URL
    ET.SubElement(channel, "description").text = "Latest 20 notices from NAS College Meerut"
    ET.SubElement(channel, "language").text = "en-us"

    for item in notices:
        item_el = ET.SubElement(channel, "item")
        ET.SubElement(item_el, "title").text = item["title"]
        ET.SubElement(item_el, "link").text = item["link"]
        ET.SubElement(item_el, "guid").text = item["link"]
        ET.SubElement(item_el, "pubDate").text = item["pubDate"]

    tree = ET.ElementTree(rss)
    tree.write(output_file, encoding="utf-8", xml_declaration=True)
    print(f"RSS feed saved to {output_file}")

if __name__ == "__main__":
    notices = fetch_notices()
    generate_rss(notices)
