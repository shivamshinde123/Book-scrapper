from flask import Flask, render_template, request
import pymongo
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By

app = Flask(__name__)



@app.route('/')
def index():
    return render_template('index.html')


@app.route('/results',methods=['GET', 'POST'])
def results():
    driver = webdriver.Chrome('C:\\Users\\shiva\\OneDrive\\Desktop\\Scrapper Project\\chromedriver.exe')
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
            except:
                print('Driver could not get to the website')

            try:
                required_genre = driver.find_element(By.LINK_TEXT, genre)
                required_genre.click()
                book_details = []
            except:
                print('Could not click on the genre after opening the website')

            while True:


                try:
                    page_url = driver.current_url
                    page_source = requests.get(page_url).text
                except:
                    print('Error occurred while getting page source from the website')

                try:
                    soup = BeautifulSoup(page_source,'lxml')
                    next_btn = soup.find_all('li', class_ = "next")
                except:
                    print('Some error occured')

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

                        try:
                            book_dict = {book_name:book_name,
                                         book_price:book_price,
                                         book_availability:book_availability}

                            book_details.append(book_dict)

                            collection.insert_one(book_dict)
                        except:
                            print('Could not save the information to the database')
                    
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