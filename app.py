from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import time
import random
from flask import Flask, render_template, request
from selenium.webdriver.chrome.options import Options
import pandas as pd
app = Flask(__name__)
user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0"
    # Add more User-Agents as needed
]
chrome_options = Options()
chrome_options.add_argument(f"user-agent={random.choice(user_agents)}")

@app.route("/", methods=['GET'])
def homepage():
    return render_template("index.html")

@app.route("/review", methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        try:
            driver_path = r"C:\Users\KAMESH\OneDrive\Desktop\DATA SCIENCE\ASSIGNMENT ANSWERS\chromedriver-win64\chromedriver.exe"
            service = Service(driver_path)
            driver = webdriver.Chrome(service=service)
            searchString = request.form['content'].replace(" ", "")
            url='https://www.youtube.com/'+ searchString +'/videos'
            driver.get(url)
            SCROLL_PAUSE_TIME=3
            last_height=driver.execute_script("return document.documentElement.scrolllHeight")
            while True:
                driver.execute_script("window.scrollTo(0,arguments[0]);",last_height)
                time.sleep(SCROLL_PAUSE_TIME)
                new_height=driver.execute_script("return document.documentElement.scrollHeight")
                if new_height == last_height:
                    break
                last_height=new_height
            titles=driver.find_elements(By.ID,"video-title")
            views=driver.find_elements(By.XPATH,'//*[@id="metadata-line"]/span[1]')
            images=driver.find_elements(By.CSS_SELECTOR, 'img.yt-core-image.yt-core-image--fill-parent-height.yt-core-image--fill-parent-width.yt-core-image--content-mode-scale-aspect-fill.yt-core-image--loaded')
            url=driver.find_elements(By.XPATH,'//*[@id="thumbnail"]')
            video_time=driver.find_elements(By.XPATH, '//*[@id="metadata-line"]/span[2]')
            data=[]
            for i,j,k,m,n in zip(titles[:5],views[:5],images[1:6],url[3:8],video_time[:5]):
                 data.append([i.text,j.text,k.get_attribute('src'),m.get_attribute('href'),n.text])
            df=pd.DataFrame(data,columns=['title','views','thumbnail','URL','TIME'])
            df.to_csv("youtube_videos_details.csv")
            html_table = df.to_html(classes='table table-striped', escape=False, index=False)
            driver.quit()
            return render_template('result.html',html_table=html_table)
        except Exception as e:
            return str(e)
    else:
        return render_template('index.html')

if __name__ == "__main__":
    app.run(host="0.0.0.0",debug=True)