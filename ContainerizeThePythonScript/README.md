### Containerization of Python Script

> Making our script compatible with Selenium grid need some modification because of which you can jump to 3rd section and come back to see why we are point driver to another IP-Address (selenium-hub). This selenium-hub will make sure distributing of multiple concurrent request to selenium-nodes according to availability.


---
### Python Script which will point to Selenium-hub (Used for local testing)

The IP-Address is already preconfigured in `docker-compose.yaml` file using which we can make sure selenium-hub will always get the IP-Address which is configured in main.py in this case. This script is used to just local test.

Python Code
```python
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

```


Dockerfile  
```Dockerfile
FROM python:3.9.17-slim-bullseye

WORKDIR /web-scraping-code-here

COPY main.py .

RUN pip install selenium

CMD ["python", "main.py"]
```

Building Image from the Dockerfile `docker build -t concurrentscrape:1 .`

---
### Python Script which will Dump Quotes in Atlas DB (Final Script)

This is a final Script which will point to `MongoDB Atlas` and send all the quotes to Atlas.

Python Code
```python
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

```

Dockerfile Code
```Dockerfile
```Dockerfile
FROM python:3.9.17-slim-bullseye

WORKDIR /web-scraping-code-here

COPY main.py .

RUN pip install selenium pymongo

CMD ["python", "main.py"]
```

Docker build Command output 

![](assets/Pasted%20image%2020230711180739.png)
