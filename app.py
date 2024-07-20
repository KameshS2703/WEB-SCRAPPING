from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import time
import pandas as pd
from flask import Flask, render_template, request,jsonify
from flask_cors import CORS,cross_origin
import requests
import pymongo
app = Flask(__name__)

@app.route("/", methods = ['GET'])
def homepage():
    return render_template("index.html")

@app.route("/review" , methods = ['POST' , 'GET'])
def index():
    if request.method == 'POST':
        try:
            driver_path = r"C:\Users\KAMESH\OneDrive\Desktop\DATA SCIENCE\ASSIGNMENT ANSWERS\chromedriver-win64\chromedriver.exe"
            service = Service(driver_path)
            driver = webdriver.Chrome(service=service)
            searchString = request.form['content'].replace(" ","")
            url = 'https://www.meesho.com/search?q=' + searchString
            driver.get(url)

            # Scroll parameters
            SCROLL_PAUSE_TIME = 3
            MAX_SCROLL_HEIGHT = 1000  # Adjust this height as needed

            last_height = driver.execute_script("return document.documentElement.scrollHeight")
            scroll_height = 0

            while scroll_height < MAX_SCROLL_HEIGHT:
                driver.execute_script("window.scrollTo(0, arguments[0]);", last_height)
                time.sleep(SCROLL_PAUSE_TIME)
                new_height = driver.execute_script("return document.documentElement.scrollHeight")
                scroll_height = new_height - last_height
                last_height = new_height

            # Extract data
            images_ = driver.find_elements(By.XPATH, '//*[@id="__next"]/div[3]/div/div[1]/div/div[2]/div[1]/img')
            name = driver.find_elements(By.XPATH, '//*[@id="__next"]/div[3]/div/div[2]/div[3]/div/p[1]')
            fabric = driver.find_elements(By.XPATH, '//*[@id="__next"]/div[3]/div/div[2]/div[3]/div/p[2]')
            Amount = driver.find_elements(By.XPATH, '//*[@id="__next"]/div[3]/div/div[2]/div[1]/div[1]/h4')
            country_of_origin = driver.find_elements(By.XPATH, '//*[@id="__next"]/div[3]/div/div[2]/div[3]/div/p[14]')

            data = []
            for i, j, k, m, n in zip(images_[:10], name[:10], fabric[:10], Amount[:10], country_of_origin[:10]):
                data.append([i.get_attribute('src'), j.text, k.text, m.text, n.text])

            df = pd.DataFrame(data, columns=['Image_link', 'Name_of_dress', 'Fabric', 'Amount', 'Country_of_origin'])
            driver.quit()
            mydict = {
                "Product": searchString,
                "Name": [n.text for n in name[:10]],
                "Images": [i.get_attribute('src') for i in images_[:10]],
                "Fabric": [k.text for k in fabric[:10]],
                "Amount": [m.text for m in Amount[:10]],
                "Country_of_origin": [n.text for n in country_of_origin[:10]]}
            client = pymongo.MongoClient("mongodb+srv://kamesh27professional:kameshisprofessional@cluster0.495zhgz.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
            db =client['scrapper_Meesho']
            coll_pw_eng = db['scraper_Meesho']
            coll_pw_eng.insert_many(mydict)

            return render_template('result.html', df=df[0:(len(df)-1)])
        except Exception as e:
            return 'something is wrong'
    else:
        return render_template('index.html')

if __name__=="__main__":
    app.run(host="0.0.0.0")
