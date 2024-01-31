import threading
import queue
import requests

q = queue.Queue()
valid_proxies = []
with open("/Users/sushilhome/PycharmProjects/AmazonData/proxy_ser.txt", "r") as f:
    proxies = f.read().split("\n")
    for p in proxies:
        q.put(p)


def check_proxies():
    global q
    while not q.empty():
        proxy = q.get()
        try:
            r = requests.get("https://ipinfo.io/json", proxies={"http": proxy, "https": proxy})
        except:
            continue
        if r.status_code == 200:
            print(proxy)


for _ in range(10):
    threading.Thread(target=check_proxies).start()
