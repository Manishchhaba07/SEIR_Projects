import requests
from bs4 import BeautifulSoup


def web_scraping(url):
    response = requests.get(url)
    
    if response.status_code == 403:
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
        response = requests.get(url, headers=headers)

    return BeautifulSoup(response.text, "lxml")


def all_titles(soup):
    titles = soup.find_all("title")
    for title in titles:
        return [title.get_text()]

def all_links(soup):
    return [
        link.get_text(strip=True)
        for link in soup.find_all('a')
        if link.get_text(strip=True)
    ]

def url_body(soup):
    body = soup.body
    return body.get_text(separator = " ", strip = True)

def page_body(soup):
    body = soup.body
    text = body.get_text(separator=" ")
    
    words = []
    current_word = ""

    for ch in text:
        if ch.isalnum():
            current_word += ch.lower()
        else:
            if current_word:
                words.append(current_word)
                current_word = ""

    if current_word:
        words.append(current_word)

    return words

def count_frequency(text_list):
    freq = {}
    for item in text_list:
        if item in freq:
            freq[item] += 1
        else:
            freq[item] = 1
    return freq


def word_hash(word):
    p = 53
    m = 2**64
    
    hash_value = 0
    power = 1

    for ch in word:
        hash_value = (hash_value + ord(ch) * power) % m
        power = (power * p) % m

    return hash_value

def compute_simhash(freq_dict):
    V = [0] * 64

    for word in freq_dict:
        weight = freq_dict[word]
        h = word_hash(word)

        for i in range(64):
            bit = (h >> i) & 1

            if bit == 1:
                V[i] += weight
            else:
                V[i] -= weight

    fingerprint = 0

    for i in range(64):
        if V[i] > 0:
            fingerprint += (1 << i)

    return fingerprint


def common_bits(hash1, hash2):
    xor = hash1 ^ hash2
    ones_bit = 0
    for i in range(0,64):
        if (xor & 1 == 1):
            ones_bit += 1
        xor = xor >> 1

    return 64 - ones_bit

url1 = "https://en.wikipedia.org/wiki/Wikipedia"
url2 = "https://en.wikipedia.org/wiki/India"

soup1 = web_scraping(url1)
soup2 = web_scraping(url2)

words1 = page_body(soup1)
words2 = page_body(soup2)

freq1 = count_frequency(words1)
freq2 = count_frequency(words2)

simhash1 = compute_simhash(freq1)
simhash2 = compute_simhash(freq2)

common_bits = common_bits(simhash1, simhash2)

print("Title 1:", all_titles(soup1))
print("Title 2:", all_titles(soup2))

# print("Body 1:", url_body(soup1))
# print("Body 2:", url_body(soup2))

print("Simhash 1:", simhash1)
print("Simhash 2:", simhash2)

print("Number of common bits:", common_bits)
