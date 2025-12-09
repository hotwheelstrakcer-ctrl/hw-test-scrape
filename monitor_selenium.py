import time
import sys
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
from colorama import init, Fore, Style

init()

URL = "https://www.firstcry.com/hotwheels/5/0/113?sort=popularity&q=ard-hotwheels&ref2=q_ard_hotwheels&asid=53241"
seen_products = {}

def setup_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless") # Run in headless mode
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--log-level=3") # Suppress logs
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    
    # PERFORMANCE OPTIMIZATION: Disable images
    prefs = {"profile.managed_default_content_settings.images": 2}
    chrome_options.add_experimental_option("prefs", prefs)
    
    # Suppress "DevTools listening on..."
    chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver

def scroll_to_bottom(driver):
    last_height = driver.execute_script("return document.body.scrollHeight")
    
    while True:
        # Scroll down to bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # Wait to load page (reduced from 2s to 0.5s for speed)
        time.sleep(0.5)

        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            # Try one more small wait to be sure, but shorter
            time.sleep(1.0)
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
        last_height = new_height

def parse_page(html):
    soup = BeautifulSoup(html, 'html.parser')
    products = {}
    
    blocks = soup.find_all('div', class_='list_block')
    
    for block in blocks:
        try:
            # Find link
            link_tag = block.find('a', href=True)
            if not link_tag:
                continue
                
            href = link_tag['href']
            
            # Name
            title_tag = block.find('a', title=True)
            name = title_tag['title'] if title_tag else link_tag.text.strip()
            
            # If name is still empty, try image alt
            if not name:
                img = block.find('img', alt=True)
                if img:
                    name = img['alt']
            
            # Stock Status Logic
            add_to_cart_btn = block.find('div', class_='ga_bn_btn_addcart')
            
            block_text = block.text.lower()
            text_indicates_oos = "out of stock" in block_text or "sold out" in block_text or "notify me" in block_text
            
            is_in_stock = bool(add_to_cart_btn) and not text_indicates_oos
            
            pid = href
            
            # Image URL
            img_tag = block.find('img', src=True)
            image_url = img_tag['src'] if img_tag else ''

            products[pid] = {
                'name': name,
                'in_stock': is_in_stock,
                'link': href,
                'image': image_url
            }
            
        except Exception as e:
            continue
            
    return products
