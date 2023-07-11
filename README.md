# Scraping Quotes and Saving it MongoDB Atlas

Document contain all the detailed steps which I took for this assignment. So let's go according to the instructions.

For this I have used Azure Virtual Machine but not from AWS, this doesn't mean I don't know AWS. I started my cloud journey with AWS but because my free tier is over I don't want to incur anymore charges. 

1. [Analyze Given Python Code](AnalyzeGivenPython/README.md)
2. [Containerize the Python script](ContainerizeThePythonScript/README.md)
3. [Setup A Selenium Grid Environment](SetUpASeleniumGridEnvironment/README.md)
4. [Scale The Scraper Using Docker And AWS & Setting up Atlas DB](ScaleTheScraperUsingDockerAndAWS/README.md)
5. [IaC Using Terraform](Terraform/README.md)

---
# Results

### 5 concurrent.futures & 5 Selenium-chrome-nodes

This Screenshot is taken when Python Script was configured to launch **5** concurrent web-driver requests to selenium-hub and there are 5 selenium-chrome-nodes are running.

![Pasted image 20230711171635](ScaleTheScraperUsingDockerAndAWS/assets/Pasted%20image%2020230711171635.png)

![Screenshot 2023-07-11 163839](ScaleTheScraperUsingDockerAndAWS/assets/Screenshot%202023-07-11%20163839.png)

---

### 10 Concurrent.futures & 10 Selenium-chrome-nodes
![Pasted image 20230711182724](ScaleTheScraperUsingDockerAndAWS/assets/Pasted%20image%2020230711182724.png)
![Pasted image 20230711182726](ScaleTheScraperUsingDockerAndAWS/assets/Pasted%20image%2020230711182726.png)

---
### MongoDB Atlas Image of Records

**BEFORE**
![Screenshot 2023-07-11 182050](ScaleTheScraperUsingDockerAndAWS/assets/Screenshot%202023-07-11%20182050.png)
**AFTER**

![Screenshot 2023-07-11 182834](ScaleTheScraperUsingDockerAndAWS/assets/Screenshot%202023-07-11%20182834.png)
![](ScaleTheScraperUsingDockerAndAWS/assets/Screenshot%202023-07-11%20190645.png)

![](ScaleTheScraperUsingDockerAndAWS/assets/Screenshot%202023-07-11%20190710.png)