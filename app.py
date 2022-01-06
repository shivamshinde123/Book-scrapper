from flask import Flask, render_template, request
import pymongo
import requests
from bs4 import BeautifulSoup
import os
import itertools
from selenium import webdriver
from selenium.webdriver.common.by import By

app = Flask(__name__)



@app.route('/')
def index():
    return render_template('index.html')


@app.route('/results',methods=['GET', 'POST'])
def results():
    basedir = os.path.abspath(os.path.dirname(__file__))
    driver = webdriver.Chrome(basedir+"\\chromedriver.exe")
    if request.method == 'POST':
        genre = request.form['genre']
        try:
            try:
                client = pymongo.MongoClient("mongodb://localhost:27017/")
                database = client['Book Collection']
                collection = database['book_collection_for_'+genre]
            except:
                print('Could not connect to the database')

            try:
                url = "http://books.toscrape.com/"
                driver.get(url)
                driver.maximize_window()
            except:
                print('Driver could not get to the website')

            try:
                required_genre = driver.find_element(By.LINK_TEXT, genre)
                required_genre.click()
                book_details = []
            except:
                print('Could not click on the genre after opening the website')

            while True:
                page_url = driver.current_url
                page_source = requests.get(page_url).text
                soup = BeautifulSoup(page_source, 'lxml')
                next_btn = soup.find_all('li', class_="next")
                no_of_book_on_the_page = len(soup.find_all('article', class_ = "product_pod"))
                try:
                    for i in range(0,no_of_book_on_the_page):
                        try:
                            book_block = driver.find_elements(By.CSS_SELECTOR,"article.product_pod")[i]
                            book_block.find_elements(By.TAG_NAME,"a")[1].click()
                        except:
                            print("Could not go to the book home page")

                        try:
                            book_name = driver.find_element(By.CSS_SELECTOR," div[class='col-sm-6 product_main'] h1").text
                            book_price = driver.find_element(By.CSS_SELECTOR,".price_color").text
                        except:
                            print("Could not get the book name and book price")

                        try:
                            book_dict = {'Book Name':book_name,
                                         'Book Price':book_price}
                            book_details.append(book_dict)
                        except:
                            print("Could not add the book name and price to the book_details list")


                        try:
                            driver.back()
                        except:
                            print("Could not go back to the genre home page")

                    if len(next_btn) > 0:
                        next_button = driver.find_element(By.LINK_TEXT,'next')
                        next_button.click()
                    else:
                        break

                except:
                    driver.quit()
                    print('Could not find any books on the given genre')

            driver.quit()
            return render_template('results.html', book_details=book_details,genre=genre)



        except:
            driver.quit()
            print("Some error occurred while connecting the database")



    else:
        driver.quit()
        return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)