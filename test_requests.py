import requests
from bs4 import BeautifulSoup

URL = "https://www.firstcry.com/hotwheels/5/0/113?sort=popularity&q=ard-hotwheels&ref2=q_ard_hotwheels&asid=53241"

try:
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    response = requests.get(URL, headers=headers, timeout=10)
    print(f"Status Code: {response.status_code}")
    
    soup = BeautifulSoup(response.content, 'html.parser')
    # Check for list block like in the original scraper
    blocks = soup.find_all('div', class_='list_block')
    print(f"Products found: {len(blocks)}")
    
    if len(blocks) > 0:
        print("First product:", blocks[0].find('a', title=True)['title'])

except Exception as e:
    print(f"Error: {e}")
