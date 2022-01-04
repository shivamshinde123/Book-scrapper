from flask import Flask, render_template, request
import pymongo
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By

app = Flask(__name__)

driver = webdriver.Chrome('C:\\Users\\shiva\\OneDrive\\Desktop\\Scrapper Project\\chromedriver.exe')

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/results',methods=['GET', 'POST'])
def results():
    if request.method == 'POST':
        genre = request.form['genre']
        try:
            conn = pymongo.MongoClient("mongodb+srv://ShivamShinde:S#ivam123@cluster0.9jrmh.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
            db = conn['Book Collection']
            collection = db['book_collection_for_'+genre]

            try:
                url = "http://books.toscrape.com/"
                driver.get(url)
            except:
                print('Driver could not get to the website')

            required_genre = driver.find_element(By.LINK_TEXT, genre)
            required_genre.click()
            book_details = []

            while True:
                page_url = driver.current_url()

                try:
                    page_source = requests.get(page_url)
                except:
                    print('Error occurred while getting page source from the website')

                soup = BeautifulSoup(page_source,'lxml')
                next_btn = soup.find_all('li', class_ = "next")

                try:
                    book_blocks = soup.find_all('article',class_ = "product_pod")
                    for block in book_blocks:

                        try:
                            book_name = block.h3.a.text
                        except:
                            print('Having some error while obtaining book name')

                        try:
                            book_price = block.h3.next_sibling.p.text
                        except:
                            print('Having some error obtaining book price')

                        try:
                            book_availability = block.h3.next_sibling.p.next_sibling.i.next_sibling.text
                        except:
                            print("Having some error while checking books' availability")

                        book_dict = {book_name:book_name,
                                     book_price:book_price,
                                     book_availability:book_availability}

                        book_details.append(book_dict)

                        collection.insert_one(book_dict)
                    
                    if len(next_btn) > 0:
                        next_button = driver.find_element(By.LINK_TEXT,'next')
                        next_button.click()
                    else:
                        break

                except:
                    driver.quit()
                    print('Could not find any books on the given genre')

            driver.quit()
            return render_template('results.html', book_details=book_details)



        except:
            driver.quit()
            print("Some error occurred while connecting the database")



    else:
        driver.quit()
        return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)