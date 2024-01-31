import requests
import mysql.connector
import numpy as np
from bs4 import BeautifulSoup
from multiprocessing import Process
import random
import time
from fake_useragent import UserAgent
from datetime import datetime, timedelta
from itertools import groupby
from operator import itemgetter
from flask import Flask, request, jsonify
from flask_cors import CORS
ua = UserAgent(os='macos')
global_lst=[]

class RealTimeCurrencyConverter():
    def __init__(self, url):
        self.data = requests.get(url).json()
        self.currencies = self.data['rates']

    def convert(self, from_currency, to_currency, amount):
        initial_amount = amount
        if from_currency != 'USD':
            amount = amount / self.currencies[from_currency]
        amount = round(amount * self.currencies[to_currency], 4)
        return amount


urlconverter = 'https://api.exchangerate-api.com/v4/latest/USD'
converter = RealTimeCurrencyConverter(urlconverter)
CurrenceyConversion = converter.convert('USD', 'INR', 1)

with open("/Users/sushilhome/PycharmProjects/AmazonData/valid_proxies", "r") as f:
    proxies = f.read().split("\n")

proxy_counter = random.randrange(178)


# creating databases

def database_creator(db_cursor, dbname):
    try:
        db_cursor.execute(f"CREATE DATABASE {dbname}")
        print(f"Successfully cfeated database {dbname}")
    except Exception as e:
        print(e)


# create basic schemas for individual tables
# amastr=
# flipstr=
# aliexpress=
# forever21=

def create_tables_indb(db_cursor, tablename, arglist):
    try:
        db_cursor.execute(f"CREATE TABLE {tablename} ({arglist})")
        print(f"Sucessfully created table with table name: {tablename}")
    except Exception as e:
        print(e)


def drop_database(db_cursor, databsename):
    try:
        db_cursor.execute(f"DROP DATABSE {databsename}")
        print(f"databse namely {databsename} deleted successfully")
    except Exception as e:
        print(e)


# Creating connection object
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root"
)
Global_Product_DB = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="Global_Product_Search"
)
Amazon_DB = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="Amazon"
)
Flipkart_DB = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="Flipkart"
)
AliExpress_DB = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="AliExpress"
)
Forever21_DB = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="Forever21"
)

# Creating an instance of 'cursor' class
# which is used to execute the 'SQL'
# statements in 'Python'
cursor1 = Amazon_DB.cursor()
cursor2 = Flipkart_DB.cursor()
cursor3 = AliExpress_DB.cursor()
cursor4 = Forever21_DB.cursor()
main_cursor=Global_Product_DB.cursor()

# def save(filename, text):
#     with open(filename,"w",encoding="utf-8") as f:
#         f.write(text)

# def fetch_amazon(url):
#     useragents = [
#         'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.88 Safari/537.36',
#         'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36',
#         'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36',
#         'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4894.117 Safari/537.36',
#         'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4855.118 Safari/537.36',
#         'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36',
#         'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36',
#         'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.88 Safari/537.36',
#         'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4892.86 Safari/537.36',
#         'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4854.191 Safari/537.36',
#         'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4859.153 Safari/537.36',
#         'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.79 Safari/537.36',
#         'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36/null',
#         'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36,gzip(gfe)',
#         'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4895.86 Safari/537.36',
#         'Mozilla/5.0 (Macintosh; Intel Mac OS X 12_3_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36',
#         'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_13) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4860.89 Safari/537.36',
#         'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4885.173 Safari/537.36',
#         'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4864.0 Safari/537.36',
#         'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_12) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4877.207 Safari/537.36',
#         'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36',
#         'Mozilla/5.0 (Macintosh; Intel Mac OS X 12_2_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.60 Safari/537.36',
#         'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36',
#         'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML%2C like Gecko) Chrome/100.0.4896.127 Safari/537.36',
#         'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.133 Safari/537.36',
#         'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_16_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36',
#         'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4872.118 Safari/537.36',
#         'Mozilla/5.0 (Macintosh; Intel Mac OS X 12_3_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.88 Safari/537.36',
#         'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_13) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4876.128 Safari/537.36',
#         'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/537.36 (KHTML%2C like Gecko) Chrome/100.0.4896.127 Safari/537.36',
#         'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36']
#
#     headers = {"User-Agent": useragents[random.randint(0, 30)], "accept-language": "en-US,en;q=0.9",
#                "accept-encoding": "gzip, deflate, br",
#                "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7"}
#
#     resp = requests.get(url, headers=headers)
#     return resp.text

def fetch_amazon(url):
    headers = {"User-Agent": ua.random, "accept-language": "en-US,en;q=0.9",
               "accept-encoding": "gzip, deflate, br",
               "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7"}

    resp = requests.get(url, headers=headers)
    return resp.text


# def fetch(url):
#     global proxy_counter
#     headers = {
#         'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) '
#                       'Chrome/39.0.2171.95 Safari/537.36'}
#     r = requests.get(url, headers=headers, proxies={"http": f"http://{proxies[proxy_counter]}"})
#     # , proxies={"http": proxies[proxy_counter], "https": proxies[proxy_counter]}
#     proxy_counter += 1
#     proxy_counter = proxy_counter % len(proxies)
#     # print(proxy_counter)
#
#     return r.text

def fetch(url):
    global proxy_counter
    headers = {"User-Agent": ua.random, "accept-language": "en-US,en;q=0.9",
               "accept-encoding": "gzip, deflate, br",
               "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7"}
    r = requests.get(url, headers=headers)
    # , proxies={"http": proxies[proxy_counter], "https": proxies[proxy_counter]}
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
            except:
                brand = np.nan
            try:
                pid = lst[i]["pid"]
            except:
                pid = np.nan
            sql = "INSERT INTO Forever21_Product (pid,Category,title,brand,Url,Price,Stars,Instock) VALUES (%s, %s,%s,%s,%s, %s,%s,%s)"
            val = (pid, Category, title, brand, purl, CurrenceyConversion * price,3.5, instock)
            try:
                cursor4.execute(sql, val)
            except Exception as e:
                print(e)

            Forever21_DB.commit()



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
            # price = temp[i]["typical_price_range"][0]
            price = temp[i]["offer"]["price"]
            print(f"the price of item is :{price}")
        except:
            price = "0.0"
            print("Not recevied as a number")

        if rating is None:
            rating = "0.0"
        sql = "INSERT INTO AliExpress_Product (ItemID,title,brand,Price,ReviewStars,Link,Instock) VALUES (%s, %s,%s,%s,%s,%s,%s)"
        try:
            val = (productid, producttitle, brand, CurrenceyConversion * float(price[1:]), float(rating), prourl,
                   available)
        except:
            val = (
                productid, producttitle, brand, CurrenceyConversion * 32, float(rating), prourl, available)
            print("wrong datatypes input")
        try:
            cursor3.execute(sql, val)
            print("successfully inserted")
        except Exception as e:
            print(e)

        AliExpress_DB.commit()




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
        rating = soup.find("span", {"data-hook": "rating-out-of-text"}).get_text().split(" ")[0]

        print(f"the price ogf phone {rating}")
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

    # if available=="Not Avaliable":
    #     available=False
    # else:
    #     available=True
    s = ""
    if (len(price) <= 3):
        for i in price.split(","):
            s += i
    else:
        for i in price[:len(price) - 1].split(","):
            s += i

    if rating is None:
        rating = "0"
    if len(s) == 0:
        s = "0.0"
    if (rating == " "):
        rating = "0.0"
    print(f"the values of rating before float conversion : {rating}")
    sql = "INSERT INTO Amazon_Product (ProductID, ProductName, Category, Brand, Price, ProductLink, Rating, Availablity) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
    val = (productid, productname, category, brand, float(s), productlink, float(rating), available)
    try:
        cursor1.execute(sql, val)
    except Exception as e:
        print(e)
    Amazon_DB.commit()



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
        price = "0,0"
    try:
        rating = soup.find("div", class_="_3LWZlK").get_text()
        print(float(rating))
    except Exception as e:
        rating = "0.0"

    try:
        brand = title.lstrip().split(" ")[0]

    except Exception as e:
        brand = np.nan
    s = ""
    for i in price[1:].split(","):
        s += i

    sql = "INSERT INTO Flipkart_Product (ItemID,ProductTitle,Category,Brand,Price,ProductLink,Rating,stock) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
    val = (itemid, title, category, brand, float(s), itemurl, float(rating), avialablity)
    try:
        cursor2.execute(sql, val)
    except Exception as e:
        print(e)

    Flipkart_DB.commit()




def amazon_web_runner(links_ama):
    i = 0
    for linkama in links_ama:
        if (i > 2):
            break
        print("Amazon list tuple")
        try:
            content = fetch_amazon(f"https://amazon.in{linkama}")
            extractor_amazon(content, linkama)
        except Exception as e:
            print(e)
            print("Error in link")
        i = i + 1


def flipkart_web_runner(links_flip):
    for linkf in links_flip:
        print("Flipkart list tuple")
        try:
            content2 = fetch(f"https://www.flipkart.com{linkf}")
            extractor_flipkart(content2, linkf)
        except:
            print("Error in link")


def main_database_updataion():
    query = input("Please Enter the product to be searched : ")
    # to flush all dta to fetch new data
    delete_records("AliExpress.AliExpress_Product",cursor3,AliExpress_DB)
    delete_records("Amazon.Amazon_Product",cursor1,Amazon_DB)
    delete_records("Flipkart.Flipkart_Product", cursor2, Flipkart_DB)
    delete_records("Forever21.Forever21_Product", cursor4, Forever21_DB)
    url_ama = f"https://www.amazon.in/s?k={query}"
    url_flip = f"https://www.flipkart.com/search?q={query}"
    text_ama = fetch_amazon(url_ama)
    text_flip = fetch(url_flip)

    links_ama = extract_links_amazon(text_ama)
    links_flip = extract_links_flipkart(text_flip)

    print(links_ama)
    print(links_flip)


    # parallel processing in progress

    # p1 = Process(target=ecommerce, kwargs={"query": query})
    # p2 = Process(target=forever21, kwargs={"query": query})
    p3 = Process(target=amazon_web_runner, kwargs={"links_ama": links_ama})
    p4 = Process(target=flipkart_web_runner, kwargs={"links_flip": links_flip})

    # p1.start()
    # p2.start()
    p3.start()
    p4.start()
    # p1.join()
    # p2.join()
    p3.join()
    p4.join()

    return fetch_allrecords_MV(main_cursor, "Global_Product_Search.Global_Product",query)

def fetch_allrecords_MV(dbcursor,tablename,query):
    dbcursor.execute(f"SELECT * FROM {tablename} WHERE Availablity=1")

    # This SQL statement selects all data from the CUSTOMER table.
    result = dbcursor.fetchall()
    result_lst=[]
    for i in range(len(result)):
        temp={}
        temp["ID"]=result[i][0]
        temp["Title"] = result[i][1]
        temp["Brand"] = result[i][2]
        temp["Price"] = result[i][3]
        if(temp["Price"]<=0):
            continue
        print(temp["Price"])
        temp["Rating"] = result[i][4]
        temp["url"] = result[i][5]
        temp["Availablity"] = result[i][6]
        temp["DataSource"] = result[i][7]
        result_lst.append(temp)
    print("completed all printing of records for result")
    newlist = sorted(result_lst, key=lambda d: d['Price'])

    # print("The values :!!!!!!!")
    # print(fetch_toprated(newlist))
    # to maintain analytics

    return newlist

def fetch_toprated(newlist):
    res= sorted(newlist, key=lambda d: d['Rating'],reverse=True)
    return res

def fetchmin_resocrds(newlist=global_lst):
    lst=[]
    print(newlist)
    minprice=newlist[0]["Price"]
    lst.append(newlist[0])
    for i in range(1,len(newlist)):
        if(newlist[i]["Price"]==minprice):
            lst.append(newlist[i])
    return lst

def maintain_cache(newlist,query):

    counter = len(newlist)
    price = 0
    rating = 0
    brands = []
    for i in range(counter):
        price = price + newlist[i]["Price"]
        rating = rating + newlist[i]["Rating"]
        if(newlist[i]["Brand"] not in brands):
            brands.append(newlist[i]["Brand"])
    average_price = float(price/counter)
    average_rating = float(rating/counter)
    sql = "INSERT INTO Global_Product_Search.Product_MV (query,AveragePrice,MajorBrand,AverageRating) VALUES (%s,%s,%s,%s)"
    val = (str(query), float(average_price), brands, float(average_rating))
    print(val)
    try:
        main_cursor.execute(sql, val)
    except Exception as e:
        print(e)
    Global_Product_DB.commit()

def delete_records(tablename,dbcursor,db):
    sql=f"DELETE FROM {tablename} "
    dbcursor.execute(sql)
    db.commit()


if __name__ == "__main__":
    main_database_updataion()
    results1 = fetch_allrecords_MV(main_cursor, "Global_Product_Search.Global_Product","phone")
    maintain_cache(results1,"query")
    # print(fetchmin_resocrds(results1))













#
#
# app = Flask(__name__)
# CORS(app)
#
#
# @app.route('/', methods=['GET'])
# def home():
#     data = {'message': 'Hello! Welcome to our backend'}
#     return jsonify(data)
#
#
# @app.route('/api/data', methods=['POST'])
# def process_data():
#     if request.method == 'POST':
#         # Get the data from the request
#         data = request.get_json()
#
#         # Extract the string from the data
#         # print(data)
#         input_string = data.get('inputString', '')
#
#         results=main_database_updataion(input_string)
#         global global_lst
#         global_lst = results
#         print(global_lst)
#         # new_string=str(results)
#         # Return the string in the response as JSON
#         response_data = {'results': results}
#         # response_data = {'outputString': input_string}
#         return jsonify(response_data)
#
# @app.route('/api/getMinPrice', methods=['POST'])
# def process_data1():
#     if request.method == 'POST':
#         # Get the data from the request
#         data = request.get_json()
#
#         # Extract the string from the data
#         # print(data)
#         input_string = data.get('inputString', '')
#         results=fetchmin_resocrds()
#
#
#         # new_string=str(results)
#         # Return the string in the response as JSON
#         response_data = {'results': results}
#         # response_data = {'outputString': input_string}
#         return jsonify(response_data)
#
# @app.route('/api/getTopRated', methods=['POST'])
# def process_data2():
#     if request.method == 'POST':
#         # Get the data from the request
#         data = request.get_json()
#
#         # Extract the string from the data
#         # print(data)
#         input_string = data.get('inputString', '')
#
#         results=main_database_updataion(input_string)
#         global_lst = results
#         print(global_lst)
#         # new_string=str(results)
#         # Return the string in the response as JSON
#         response_data = {'results': results}
#         # response_data = {'outputString': input_string}
#         return jsonify(response_data)
#
#
# if __name__ == '__main__':
#     app.run(debug=True)