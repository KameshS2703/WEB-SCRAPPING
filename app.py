from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import time
import pandas as pd
from flask import Flask, render_template, request,jsonify
from flask_cors import CORS,cross_origin
import requests
import pymongo
import random
from selenium.webdriver.chrome.options import Options

app = Flask(__name__)
user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0"
    # Add more User-Agents as needed
]
chrome_options = Options()
chrome_options.add_argument(f"user-agent={random.choice(user_agents)}")
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
            url = 'https://www.bigbasket.com/ps/?q=' + searchString
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
            images_ = driver.find_elements(By.CSS_SELECTOR, 'img')
            name = driver.find_elements(By.XPATH, '//*[@id="siteLayout"]/div/div/section[1]/div[2]/section[1]/h1')
            Amount = driver.find_elements(By.XPATH, '//*[@id="siteLayout"]/div/div/section[1]/div[2]/section[1]/table/tr[2]/td[1]')
            

            data = []
            for i, j, k in zip(images_[:10], name[:10], Amount[:10]):
                data.append([i.get_attribute('src'), j.text, k.text])

            df = pd.DataFrame(data, columns=['Image_Link', 'Name_Of_Product', 'Amount_Of_Product'])
            driver.quit()
            
            

            return render_template('result.html',df[0:(len(df)-1)])
        except Exception as e:
            return e
    else:
        return render_template('index.html')

if __name__=="__main__":
    app.run(host="0.0.0.0",debug=True)
