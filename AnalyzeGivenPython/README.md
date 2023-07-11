### Python Virtual ENV setup
1. `python -m pip venv venv` -> Run this command in your empty folder
2. `source /venv/bin/activate` or `source /venv/Script/activate` -> To activate the Environment and make sure `(venv)` is visible in you cli to install new pip packages from the `requirements.txt` file
3. `pip install -r requirements.txt` -> Make sure you are in right folder where requirements file is present
4. `touch original-code.py` -> And save the below first code block

Requirement file 
```
selenium==4.10.0
pymongo==4.4.0
```

### Analyzing the given Script

```python
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from pymongo import MongoClient

chrome_options = Options()
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--headless")

#This code is used to specify, to use local driver.
driver = webdriver.Chrome(options=chrome_options)

driver.get("http://quotes.toscrape.com")
client = MongoClient('mongodb://localhost:27017/')
db = client['mcs_assignment']
collection = db['quotes']


for page in range(10):
    for i in range(1, 11):
        quote_xpath = f"/html/body/div[1]/div[2]/div[1]/div[{i}]/span[1]"
        author_xpath =f"/html/body/div[1]/div[2]/div[1]/div[{i}]/span[2]/small"

        quote_element = driver.find_element(By.XPATH, quote_xpath)
        quote_text = quote_element.text
        
        author_element = driver.find_element(By.XPATH, author_xpath)
        author_name = author_element.text
        
        print(f"PAGE:{page} - QuoteNumber: {i}")
        print("Quote:", quote_text)
        print("Author:", author_name)
        print()

        document = {
        'quote_id': page * 10 + i,
        'quote': quote_text,
        'author': author_name
        }
        collection.insert_one(document)
    try:
        next_button = driver.find_element(By.XPATH, "//li[@class='next']/a")
        next_button.click()
    except:
        print("No more pages available. Exiting loop.")
        break
driver.quit()
```
---

### How Above script is working
1. This Script is scrapping quotes by going to first this web-link [QuotesLinkWebsite](https://quotes.toscrape.com/)
2. As soon as we land on this website we look for **quote_xpath** & **author_xpath** which contain the required details what we want to store in MongoDB Atlas 
3. From there we can see a **Next** button which takes us to next page
4. And we repeat the 2nd step again.

---

This Script is working Linearly instead we can open multiple *Tabs* in browser and scrape the quotes, for example as we can open multiple tabs in browser to view the same webpage but different links in the webpage similarly. And also one more problem we can see our script is looking for quotes one by one from top to bottom, one improvement we can make in this code which will specify that instead of looking to one quotes at a single time look for all the 10 quotes in the website concurrently and for that we would be utilizing `concurrent.futures` module in python which will use Threads.

Let's Add Time in our original script to see how much time it takes
![](assets/Pasted%20image%2020230711145824.png)
This number also depends on internet connection but, we got the baseline for our code which is around `16 seconds`

---
### Adding Code to open multiple web-browser for each different web-links

Right Now we only have 10 web-links and they also follow a simple pattern, for going from 1 to 10th page, So I have written a small python script which will convert all the website links to a list. Then we can copy that link to our main code and instead of pressing **Next** button we can directly tell our script to go, to particular web-link

> Why Extracting this links, while going through `concurrent.futures` documentation, they are also using different links to speed up the process that why extracting all the links. 

```python
for i in range(1, 11):
    print(f'"https://quotes.toscrape.com/page/{i}/", ', end=" ")
```

To open multiple web-browser import `from concurrent.futures import ThreadPoolExecutor` and our resulting code would look like this

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
    
    #This code is used to specify, to use local driver.
    driver = webdriver.Chrome(options=chrome_options)

    driver.get(url)

    for i in range(1, 11):
        quote_xpath = f"/html/body/div[1]/div[2]/div[1]/div[{i}]/span[1]"
        author_xpath =f"/html/body/div[1]/div[2]/div[1]/div[{i}]/span[2]/small"

        quote_element = driver.find_element(By.XPATH, quote_xpath)
        quote_text = quote_element.text
        
        author_element = driver.find_element(By.XPATH, author_xpath)
        author_name = author_element.text

        print(f"PAGE:{page} - QuoteNumber: {i}")
        print("Quote:", quote_text)
        print("Author:", author_name)
        print()
    
    driver.quit()


if __name__ == "__main__":

    start_time = time.perf_counter()

    urls = ["https://quotes.toscrape.com", "https://quotes.toscrape.com/page/2/", "https://quotes.toscrape.com/page/3","https://quotes.toscrape.com/page/4/",  "https://quotes.toscrape.com/page/5/",  "https://quotes.toscrape.com/page/6/",  "https://quotes.toscrape.com/page/7/",  "https://quotes.toscrape.com/page/8/",  "https://quotes.toscrape.com/page/9/",  "https://quotes.toscrape.com/page/10/"]

    with ThreadPoolExecutor(max_workers=10) as executor:

        for page_count, url in enumerate(urls):
            executor.submit(opening_single_browser, page_count, url)

    end_time = time.perf_counter()
    elapsed_time = end_time - start_time

    print(f"Elapsed time: {elapsed_time} seconds")
```

Our this code **Results** looks like this

- This photo shows multiple browsers are opening
  ![](assets/Pasted%20image%2020230711151751.png)
- This photo shows little bit time improvement in our code
 ![Time improvement Photo](assets/Pasted%20image%2020230711151832.png)

---
### Improving code further by trying scraping all the 10 Quotes at one from each webpage

To do this also we will be utilizing our `concurrent.futures` in the code block where we are finding `XPATH` element in the web,
for this we will create a separate function whose task it to take the required element for each page like *(page_number, XPATH for Quote and Author)* and start finding it in the website.

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
    
    #This code is used to specify, to use local driver.
    driver = webdriver.Chrome(options=chrome_options)

    driver.get(url)

    #Because there are 10 Quotes that's why our max_worker=10
    with ThreadPoolExecutor(max_workers=10) as executorx:
        for i in range(1, 11):
            quote_xpath = f"/html/body/div[1]/div[2]/div[1]/div[{i}]/span[1]"
            author_xpath = f"/html/body/div[1]/div[2]/div[1]/div[{i}]/span[2]/small"

            executorx.submit(scraping_single_quote, driver, quote_xpath, author_xpath, page, i)
    
    driver.quit()

def scraping_single_quote(driver, quote_xpath, author_xpath, page, i):
    quote_element = driver.find_element(By.XPATH, quote_xpath)
    quote_text = quote_element.text
    
    author_element = driver.find_element(By.XPATH, author_xpath)
    author_name = author_element.text

    print(f"PAGE:{page} - QuoteNumber: {i}")
    print("Quote:", quote_text)
    print("Author:", author_name)
    print()
    return None

if __name__ == "__main__":

    start_time = time.perf_counter()

    urls = ["https://quotes.toscrape.com", "https://quotes.toscrape.com/page/2/", "https://quotes.toscrape.com/page/3","https://quotes.toscrape.com/page/4/",  "https://quotes.toscrape.com/page/5/",  "https://quotes.toscrape.com/page/6/",  "https://quotes.toscrape.com/page/7/",  "https://quotes.toscrape.com/page/8/",  "https://quotes.toscrape.com/page/9/",  "https://quotes.toscrape.com/page/10/"]

    #Because there are 10 Web-Links that's why our max_worker=10
    with ThreadPoolExecutor(max_workers=10) as executor:

        for page_count, url in enumerate(urls):
            executor.submit(opening_single_browser, page_count, url)

    end_time = time.perf_counter()
    elapsed_time = end_time - start_time

    print(f"Elapsed time: {elapsed_time} seconds")
```

Our this code **Results** looks like this

- Little bit more improvement in our **Time**
 ![](assets/Pasted%20image%2020230711153114.png)
---
