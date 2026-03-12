import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import time
import re
import urllib.robotparser as robotparser


class WebCrawler:
    def __init__(self, seed_url, max_pages=10, delay=2):
        self.seed_url = seed_url
        self.max_pages = max_pages
        self.delay = delay
        self.visited_urls = set()
        self.index = {}  

       
        self.robot_parser = robotparser.RobotFileParser()
        robots_url = urljoin(seed_url, "/robots.txt")
        self.robot_parser.set_url(robots_url)
        self.robot_parser.read()

    def is_allowed(self, url):
        """Check robots.txt permission"""
        return self.robot_parser.can_fetch("*", url)

    def fetch_page(self, url):
        """Fetch webpage content"""
        try:
            response = requests.get(url, timeout=10, headers={
                "User-Agent": "SimpleWebCrawler/1.0"
            })
            if response.status_code == 200:
                return response.text
        except requests.exceptions.RequestException:
            return None
        return None

    def extract_text(self, html):
        """Extract visible text from HTML"""
        soup = BeautifulSoup(html, "lxml")


        for script in soup(["script", "style"]):
            script.decompose()

        text = soup.get_text(separator=" ")
        text = re.sub(r"\s+", " ", text)
        return text.strip()

    def extract_links(self, html, base_url):
        """Extract and normalize hyperlinks"""
        soup = BeautifulSoup(html, "lxml")
        links = set()

        for tag in soup.find_all("a", href=True):
            full_url = urljoin(base_url, tag["href"])
            parsed = urlparse(full_url)


            if parsed.scheme in ["http", "https"]:
                links.add(full_url)

        return links

    def crawl(self):
        """Start crawling process"""
        urls_to_crawl = [self.seed_url]

        while urls_to_crawl and len(self.visited_urls) < self.max_pages:
            current_url = urls_to_crawl.pop(0)

            if current_url in self.visited_urls:
                continue

            if not self.is_allowed(current_url):
                print(f"Blocked by robots.txt: {current_url}")
                continue

            print(f"Crawling: {current_url}")
            html = self.fetch_page(current_url)

            if html:
                text = self.extract_text(html)
                self.index[current_url] = text
                self.visited_urls.add(current_url)

                links = self.extract_links(html, current_url)
                for link in links:
                    if link not in self.visited_urls:
                        urls_to_crawl.append(link)

            
            time.sleep(self.delay)

        print("\nCrawling completed!")
        print(f"Total pages indexed: {len(self.index)}")

    def display_index(self):
        """Display indexed pages"""
        for url, content in self.index.items():
            print("\nURL:", url)
            print("Indexed Content (first 300 chars):")
            print(content[:300])

if __name__ == "__main__":
    seed_url = "https://example.com"
    crawler = WebCrawler(seed_url, max_pages=5, delay=2)
    crawler.crawl()
    crawler.display_index()
