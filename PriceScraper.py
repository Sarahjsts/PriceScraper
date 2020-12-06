from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By 
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from flask import Flask, request, render_template
import cgi
import csv
import pandas as pd

#User input
materials = {}


app = Flask(__name__)

@app.route('/')
def my_form():
    return render_template('PriceScraper.html')

if __name__ == '__main__':
    app.run()

@app.route('/', methods=['POST'])
def my_form_post():
    variable = request.form['url']
    return variable
'''userDone = False

while (userDone is False):
    userEnteredMats = input("Please enter required material: ")
    userEnteredQuantity = int(input("Please enter quantity: "))

    materials[userEnteredMats] = userEnteredQuantity

    isUserDone = input("Anything else? Y/N")
    if (isUserDone == "N"):
        userDone = True
'''

userEnteredWebsite = my_form_post()
driver = webdriver.Chrome()
driver.get(userEnteredWebsite)

components = driver.find_element_by_id('components')
supplies = components.find_elements_by_class_name('part-name')
quantity = components.find_elements_by_css_selector('td[style="width:10%;min-width:20px;text-align:center;vertical-align:middle"]')

for supply in supplies:
    materials[supply.text] = int(quantity[supplies.index(supply)].text)

print(materials)

itemsAndPrices = {}
for mat in materials:
    driver = webdriver.Chrome()
    driver.get('https://www.adafruit.com')
    search = driver.find_element_by_id('search')
    search.send_keys(mat)
    search.send_keys(Keys.RETURN)

    try:
        results = WebDriverWait(driver, 3).until(
            EC.presence_of_element_located((By.ID, "is-hits"))
        )   
        products = results.find_elements_by_tag_name('a')
        print(products[1].text)
            
    
        prices = results.find_elements_by_class_name("normal-price")
        print(prices[0].text)
        
       # if (mat == products[1].text):
        itemsAndPrices[products[1].text] = prices[0].text

        driver.close()
        continue

    except:
        driver.quit()

print(itemsAndPrices)

x = pd.Series(data=itemsAndPrices).to_frame()
x.to_csv('open.csv')
print(x)