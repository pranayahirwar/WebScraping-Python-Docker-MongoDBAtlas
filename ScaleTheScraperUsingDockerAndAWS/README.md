# Index

1. Setting Up Atlas
2. Creating docker-compose.yml for 10 Nodes & 1 Hub
3. Result on Time & Performance improvement 

---
### Setting Up Atlas DB

Sign-up for MongoDB Atlas it's free to run Atlas server until you cross 512MB storage limit and need some extra configurations. 
From there own process is very easy, Mongo's UI will guide you for creating you first *free* cluster, note that **Select Cloud and Location** carefully. If you are running your VMs workload in Cloud for say Azure and now going to create Atlas, always make sure place it in Azure just for performance sake.

- Setting up Database & Collection
  ![](assets/Pasted%20image%2020230711184759.png)

- **Make sure you have WHITE-LISTED your IP-Address**
  ![](assets/Pasted%20image%2020230711184613.png)


---
# Results

### 5 Concurrent.futures & 5 Selenium-chrome-nodes

This Screenshot is taken when Python Script was configured to launch **5** concurrent web-driver requests to selenium-hub and there are 5 selenium-chrome-nodes are running.

![](assets/Pasted%20image%2020230711171635.png)

![](assets/Screenshot%202023-07-11%20163839.png)

---

### 10 Concurrent.futures & 10 Selenium-chrome-nodes

![](assets/Pasted%20image%2020230711182724.png)
![](assets/Pasted%20image%2020230711182726.png)