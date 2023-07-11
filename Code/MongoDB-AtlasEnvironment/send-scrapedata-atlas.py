from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from concurrent.futures import ThreadPoolExecutor
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import time

def opening_single_browser(page, url):
    chrome_options = Options()
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--headless")
    
    driver = webdriver.Remote(
        command_executor='http://172.40.0.2:4444/wd/hub',
        options=chrome_options
    )

    driver.get(url)
   
    all_quotes_from_single_page = []
    with ThreadPoolExecutor(max_workers=10) as executorx:
        for i in range(1, 11):
            quote_xpath = f"/html/body/div[1]/div[2]/div[1]/div[{i}]/span[1]"
            author_xpath = f"/html/body/div[1]/div[2]/div[1]/div[{i}]/span[2]/small"

            single_quote = executorx.submit(scraping_single_page, driver, quote_xpath, author_xpath, page, i)
            all_quotes_from_single_page.append(single_quote.result())
    
    driver.quit()
    return all_quotes_from_single_page

def scraping_single_page(driver, quote_xpath, author_xpath, page, i):
    quote_element = driver.find_element(By.XPATH, quote_xpath)
    quote_text = quote_element.text
    
    author_element = driver.find_element(By.XPATH, author_xpath)
    author_name = author_element.text

    document = {
        'quote_id': page * 10 + i,
        'quote': quote_text,
        'author': author_name
    }

    return document


if __name__ == "__main__":
    start_time = time.perf_counter()

    urls = ["https://quotes.toscrape.com", "https://quotes.toscrape.com/page/2/", "https://quotes.toscrape.com/page/3","https://quotes.toscrape.com/page/4/",  "https://quotes.toscrape.com/page/5/",  "https://quotes.toscrape.com/page/6/",  "https://quotes.toscrape.com/page/7/",  "https://quotes.toscrape.com/page/8/",  "https://quotes.toscrape.com/page/9/",  "https://quotes.toscrape.com/page/10/"]
    quotes_data_collections = []

    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = [executor.submit(opening_single_browser, page_count, url) for page_count, url in enumerate(urls)]
        for future in futures:
            result = future.result()
            quotes_data_collections.extend(result)

    end_time = time.perf_counter()
    elapsed_time = end_time - start_time
    print(f"Elapsed time: {elapsed_time} seconds")


    # First Let's check Atlas DB is properly configured or not.
    uri = "mongodb+srv://pranay:dimqhi4cdAVUSTAq@pranay-mcs-assignment.crh92xe.mongodb.net/?retryWrites=true&w=majority"

    # Create a new client and connect to the server
    client = MongoClient(uri, server_api=ServerApi('1'))

    # Send a ping to confirm a successful connection
    try:
        client.admin.command('ping')
        print("Pinged your deployment. You successfully connected to MongoDB!")
    except Exception as e:
        print(e)

    print("Now going to insert in mongodb")
    db = client['mcs_assignment']
    collection = db['quotes']

    for quote_data in quotes_data_collections:
        collection.insert_one(quote_data)
    
    print("Uploaded all data to MongoDB Atlas")

