import requests
from bs4 import BeautifulSoup

def web_scraping(url):
    response = requests.get(url)
    
    if response.status_code == 403:
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) " "Chrome/120.0.0.0 Safari/537.36"}
        response = requests.get(url, headers=headers)

    return BeautifulSoup(response.text, "lxml")


def all_titles(soup):
    titles = soup.find_all("title")
    for title in titles:
        return title.get_text()


def page_body(soup):
    body = soup.body
    return body.get_text(separator="\n", strip=True)

def all_links(soup):
    return [
    link.get_text(strip = True)
    for link in soup.find_all('a')
    if link.get_text(strip = True)
    ]


url = "https://en.wikipedia.org/wiki/Wikipedia"
soup = web_scraping(url)

# print(all_titles(soup))
# print(page_body(soup))
# print(all_links(soup))

# print(web_scraping("https://en.wikipedia.org/wiki/Wikipedia"))
