from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from concurrent.futures import ThreadPoolExecutor
import time


def opening_single_browser(page, url):
    chrome_options = Options()
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--headless")
    # driver = webdriver.Chrome(options=chrome_options)
    
    driver = webdriver.Remote(
        command_executor='http://172.40.0.2:4444/wd/hub',
        options=chrome_options
    )

    driver.get(url)
   
    with ThreadPoolExecutor(max_workers=10) as executorx:
        for i in range(1, 11):
            quote_xpath = f"/html/body/div[1]/div[2]/div[1]/div[{i}]/span[1]"
            author_xpath = f"/html/body/div[1]/div[2]/div[1]/div[{i}]/span[2]/small"

            executorx.submit(scraping_single_page,driver, quote_xpath, author_xpath, page, i)
    driver.quit()


def scraping_single_page(driver, quote_xpath, author_xpath, page, i):
    quote_element = driver.find_element(By.XPATH, quote_xpath)
    quote_text = quote_element.text
    
    author_element = driver.find_element(By.XPATH, author_xpath)
    author_name = author_element.text

# Main Code starts from here.
# ============================================================================= 
start_time = time.perf_counter()

urls = ["https://quotes.toscrape.com", "https://quotes.toscrape.com/page/2/",  "https://quotes.toscrape.com/page/3/", "https://quotes.toscrape.com/page/4/",  "https://quotes.toscrape.com/page/5/",  "https://quotes.toscrape.com/page/6/",  "https://quotes.toscrape.com/page/7/",  "https://quotes.toscrape.com/page/8/",  "https://quotes.toscrape.com/page/9/",  "https://quotes.toscrape.com/page/10/"]



with ThreadPoolExecutor(max_workers=5) as executor:
    for page_count, url in enumerate(urls):
        
        executor.submit(opening_single_browser, page_count, url)

end_time = time.perf_counter()
elapsed_time = end_time - start_time

print(f"Elapsed time: {elapsed_time} seconds")
