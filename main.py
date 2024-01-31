import pymongo
import requests
import numpy as np
from multiprocessing import Process
from bs4 import BeautifulSoup
import random
class RealTimeCurrencyConverter():
    def __init__(self,url):
        self.data= requests.get(url).json()
        self.currencies = self.data['rates']
    def convert(self, from_currency, to_currency, amount): 
            initial_amount = amount 
            if from_currency != 'USD' : 
                amount = amount / self.currencies[from_currency] 
            amount = round(amount * self.currencies[to_currency], 4) 
            return amount   



urlconverter = 'https://api.exchangerate-api.com/v4/latest/USD'
converter = RealTimeCurrencyConverter(urlconverter)
CurrenceyConversion=converter.convert('USD','INR',1)

client=pymongo.MongoClient('mongodb+srv://girisushil:mvOBmHb6t80ho7Pn@shoppingcluster.vxh0ypo.mongodb.net/')
with open("/Users/sushilhome/Desktop/IIA_Project/valid_proxies.txt", "r") as f:
    proxies = f.read().split("\n")

proxy_counter = random.randrange(126)
#  Creating connection object
# creating databse objects
Amazon_DB = client["AmazonDB"]
Flipkart_DB = client["FlipkartDB"]
AliExpress_DB = client["AliexpressDB"]
Forever21_DB = client["Forever21DB"]

# creating product tables
amazon_products = Amazon_DB["Amazon_Product"]
flipkart_products = Flipkart_DB["Flipkart_Product"]
aliexpress_products = AliExpress_DB["AliExpress_Product"]
forever21_products = Forever21_DB["Forever21_Product"]

def fetch_amazon(url):
    useragents = [
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.88 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4894.117 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4855.118 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.88 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4892.86 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4854.191 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4859.153 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.79 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36/null',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36,gzip(gfe)',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4895.86 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 12_3_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_13) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4860.89 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4885.173 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4864.0 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_12) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4877.207 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 12_2_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.60 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML%2C like Gecko) Chrome/100.0.4896.127 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.133 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_16_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4872.118 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 12_3_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.88 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_13) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4876.128 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/537.36 (KHTML%2C like Gecko) Chrome/100.0.4896.127 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36']

    headers = {"User-Agent": useragents[random.randint(0, 30)], "accept-language": "en-US,en;q=0.9",
               "accept-encoding": "gzip, deflate, br",
               "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7"}

    resp = requests.get(url, headers=headers)
    return resp.text


def fetch(url):
    global proxy_counter
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/39.0.2171.95 Safari/537.36'}
    r = requests.get(url, headers=headers, proxies={"http": f"http://{proxies[proxy_counter]}"})
    # , proxies={"http": proxies[proxy_counter], "https": proxies[proxy_counter]}
    proxy_counter += 1
    proxy_counter = proxy_counter % len(proxies)
    # print(proxy_counter)

    return r.text


def forever21(query):
    url = "https://apidojo-forever21-v1.p.rapidapi.com/products/search"

    querystring = {"query": f"{query}", "rows": "60", "start": "0"}

    headers = {
        "X-RapidAPI-Key": "f614473df0msh7eb0e24dc0ba4e4p17abadjsna81253b52b1c",
        "X-RapidAPI-Host": "apidojo-forever21-v1.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)
    instock = True
    Category = "Fashion"
    data = response.json()
    if "message" in data.keys():
        print("No results")
    else:
        rspnse = data["response"]
        lst = rspnse["docs"]
        for i in range(len(lst)):
            try:
                price = lst[i]["sale_price"]
            except:
                price = 0.0
            try:
                title = lst[i]["title"]
            except:
                title = np.nan
            try:
                purl = lst[i]["url"]
            except:
                purl = np.nan
            try:
                brand = lst[i]["brand"]
                print(brand)
            except:
                brand = np.nan
            try:
                pid = lst[i]["pid"]
            except:
                pid = np.nan
            proddict={"pid":pid,"CategoryName":Category,"tite":title,"Brand":brand,"Url":purl,"Price":CurrenceyConversion*price,"Instock":instock}
            forever21_products.insert_one(proddict)




def ecommerce(query):
    url = "https://real-time-product-search.p.rapidapi.com/search"

    querystring = {"q": f"{query}", "country": "us", "language": "en"}

    headers = {
        "X-RapidAPI-Key": "981b621b8amsh9947c2adbf92fa8p15f05cjsnb48be365696e",
        "X-RapidAPI-Host": "real-time-product-search.p.rapidapi.com"
    }
    response = requests.get(url, headers=headers, params=querystring)


    lst = response.json()
    temp = lst["data"]
    available = True
    for i in range(len(temp)):
        try:
            productid = temp[i]["product_id"]
        except:
            productid = np.nan

        try:
            producttitle = temp[i]["product_title"]
        except:
            producttitle = np.nan

        try:
            rating = temp[i]["product_rating"]
        except:
            rating = "0"

        brand = producttitle.split(" ")[0]

        try:
            prourl = temp[i]["product_page_url"]
        except:
            prourl = np.nan

        try:
            product_photo = temp[i]["product_photos"][0]
        except:
            product_photo = np.nan

        try:
            price = temp[i]["typical_price_range"][0]
        except:
            price = "0.0"

        if rating is None:
            rating="0.0"

        proddict={"ItemID":productid,"title":producttitle,"brand":brand,"Link":prourl,"Price":CurrenceyConversion*float(price[1:]),"ReviewStars":float(rating),"Instock":available}
        aliexpress_products.insert_one(proddict)


def extract_links_amazon(html):
    links = []
    soup = BeautifulSoup(html, 'html.parser')
    for link in soup.find_all("a"):
        linkhref = link.get("href")
        if linkhref is not None:
            if "/dp/" in linkhref:
                links.append(linkhref)

    return links


def extractor_amazon(html, li):
    productlink = f"https://www.amazon.in{li}"
    endidx = li.find("/ref=")
    startidx = li.find("dp/")
    productid = li[startidx + 3: endidx]
    # instock = True
    category = "generic"
    soup = BeautifulSoup(html, 'html.parser')
    try:
        productname = soup.find("span", {"id": "productTitle"}).get_text().strip()
    except Exception as e:
        productname = np.nan
    try:
        price = soup.find("span", class_="a-price-whole").get_text()
        
    except Exception as e:
        price = "0,0."
    try:
        rating = soup.find("i", {"class": "a-icon-star"}).get_text().split(" ")[0]
    except:
        rating = "0.0"
    try:
        brand = productname.lstrip().split(" ")[0]
    except Exception as e:
        brand = np.nan
    try:
        available = soup.find("div", attrs={'id': 'availability'})
        available = available.find("span").string.strip()
        available = True

    except AttributeError:
        available = False
    
    s = ""
    if(len(price)<=3):
        for i in price.split(","):
            s += i
    else:
        for i in price[:len(price) - 1].split(","):
            s += i
    
    if rating is None:
        rating="0"
    if len(s)==0:
        s="0.0"
    
    
    proddict={"ProductID":productid,"ProductName":productname,"Category":category,"Brand":brand,"Price":s,"ProductLink":productlink,"Rating":float(rating),"Availablity":available}
    amazon_products.insert_one(proddict)


def extract_links_flipkart(html):
    links = []
    soup = BeautifulSoup(html, 'html.parser')
    for link in soup.find_all("a", class_="_1fQZEK"):
        linkhref = link.get("href")
        if linkhref is not None:
            links.append(linkhref)
    for link in soup.find_all("a", class_="s1Q9rs"):
        linkhref = link.get("href")
        if linkhref is not None:
            links.append(linkhref)
    for link in soup.find_all("a", class_="IRpwTa"):
        linkhref = link.get("href")
        if linkhref is not None:
            links.append(linkhref)

    return links


def extractor_flipkart(html, li):
    category = "generic"
    itemurl = f"https://www.flipkart.com{li}"
    endidx = li.find("&lid=")
    startidx = li.find("pid=")
    itemid = li[startidx + 4: endidx]
    soup = BeautifulSoup(html, 'html.parser')
    avialablity = True

    try:
        title = soup.find("span", class_="B_NuCI").get_text().strip()
    except Exception as e:
        title = np.nan
    try:
        price = soup.find("div", class_="_30jeq3 _16Jk6d").get_text()
    except Exception as e:
        price = "r0,0"
    try:
        rating = soup.find("div", class_="_2d4LTz").get_text()
    except Exception as e:
        rating = "0.0"

    try:
        brand = title.lstrip().split(" ")[0]

    except Exception as e:
        brand = np.nan
    s = ""
    for i in price[1:].split(","):
        s += i
    
    proddict={"ItemID":itemid,"ProductTitle":title,"Category":category,"Brand":brand,"Price":float(s),"ProductLink":itemurl,"Rating":float(rating),"Stock":avialablity}
    flipkart_products.insert_one(proddict)

def amazon_web_runner(links_ama):
    for linkama in links_ama:
        print("Amazon list tuple")
        content = fetch_amazon(f"https://amazon.in{linkama}")
        extractor_amazon(content, linkama)

def flipkart_web_runner(links_flip):
     for linkf in links_flip:
        print("Flipkart list tuple")
        content2 = fetch(f"https://www.flipkart.com{linkf}")
        extractor_flipkart(content2, linkf)



if __name__ == "__main__":
    
    query = input("Please Enter the product to be searched : ")
    
#     client=pymongo.MongoClient('mongodb+srv://girisushil:mvOBmHb6t80ho7Pn@shoppingcluster.vxh0ypo.mongodb.net/')

   
    url_ama = f"https://www.amazon.in/s?k={query}"
    url_flip = f"https://www.flipkart.com/search?q={query}"
    text_ama = fetch_amazon(url_ama)
    text_flip = fetch(url_flip)

    links_ama = extract_links_amazon(text_ama)
    links_flip = extract_links_flipkart(text_flip)

    # print(links_ama)
    # print(links_flip)
    
   # parallel processing in progress
    
    p1 = Process(target = ecommerce, kwargs={"query":query})
    p2 = Process(target = forever21, kwargs={"query":query})
    p3=Process(target=amazon_web_runner,kwargs={"links_ama":links_ama})
    p4=Process(target=flipkart_web_runner,kwargs={"links_flip":links_flip})

    p1.start()
    p2.start()
    p3.start()
    p4.start()
    p1.join()
    p2.join()
    p3.join()
    p4.join()


    
