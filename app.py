from flask import Flask, render_template, request
import pandas as pd
import pymongo
import requests
from bs4 import BeautifulSoup
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

app = Flask(__name__,template_folder='templates',static_folder='static')


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/results',methods=['GET', 'POST'])
def results():
    ## Getting the path of the current file
    basedir = os.path.abspath(os.path.dirname(__file__))
    
    ## Creating a chrome driver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    if request.method == 'POST':
        ## Getting the genre provided by the user from the html form
        genre = request.form['genre']

        ##creating two lists: one for all the book names and other for all the book prices
        book_name_list = []
        book_price_list = []
        try:
            # Connecting to the pymongo atlas        
            client = pymongo.MongoClient("mongodb://localhost:27017")

            # Creating a database which will store the book details
            database_name = "Book_Collection"
            database = client[database_name]

            # Creating a collection for the genre provided by the user
            collection_name = "book_collection_for_"+str(genre)
            collection = database[collection_name]

            # Finding the number of documents in a collection for the genre provided by user
            ids = []
            for doc in collection.find():
                ids += [doc['_id']]
            collection_length = len(ids)

            # Checking whether the database contains the books details for genre provided by the user
            if collection_length >0:
                driver.quit()
                ## Adding the book name and price to the lists to use those list to get scrapped data in csv format later
                for doc in collection.find():
                    book_name_list.append(doc['Book Name'])
                    book_price_list.append(doc['Book Price'])
                ## creating a csv file of the scrapped data
                dataframe = pd.DataFrame({"Book Name": book_name_list, "Book Price": book_price_list})

                dataframe.to_csv(os.path.join(basedir,"scrappedData","booksOnGenre{}.csv".format(genre)))
                return render_template('results.html', book_details=list(collection.find({})),genre=genre)

            # If database does not have the data related to the genre provided by the data then browser will be opened to scrape the data
            else:
                try:
                    ## Opening the website using chrome driver
                    url = "http://books.toscrape.com/"
                    driver.get(url)

                    ## Maximizing the browser window
                    driver.maximize_window()
                except:
                    print('Driver could not get to the website')

                try:
                    ## Clicking on the genre provided by the user on the website home page
                    required_genre = driver.find_element(By.LINK_TEXT, genre)
                    required_genre.click()
                    book_details = []
                except:
                    print('Could not click on the genre after opening the website home page')

                while True:
                    ## Getting the url for the page opened for the genre provided by the user
                    page_url = driver.current_url

                    ## Getting the page source for the same page
                    page_source = requests.get(page_url).text
                    ## Creating soup object using the page source
                    soup = BeautifulSoup(page_source, 'lxml')
                    next_btn = soup.find_all('li', class_="next")

                    ## Finding the number of books on the page for provided genre
                    no_of_book_on_the_page = len(soup.find_all('article', class_ = "product_pod"))


                    try:
                        for i in range(0,no_of_book_on_the_page):
                            try:
                                ## clicking on the particular book
                                book_block = driver.find_elements(By.CSS_SELECTOR,"article.product_pod")[i]
                                book_block.find_elements(By.TAG_NAME,"a")[1].click()
                            except:
                                print("Could not go to the book home page")

                            try:
                                ## Finding the book name and book price
                                book_name = driver.find_element(By.CSS_SELECTOR," div[class='col-sm-6 product_main'] h1").text
                                book_price = driver.find_element(By.CSS_SELECTOR, ".price_color").text
                                ## Adding the book name and price to the lists to use those list to get scrapped data in csv format later
                                ## Adding book name to the book_name_list
                                book_name_list.append(book_name)
                                ## Adding book price to the book_price_list
                                book_price_list.append(book_price)

                            except:
                                print("Could not get the book name and book price")

                            try:
                                ## creating a dictionary of book name and book price and then adding it to book_details list and mongo db collection for the genre
                                book_dict = {'Book Name':book_name,
                                             'Book Price':book_price}
                                book_details.append(book_dict)
                                collection.insert_one(book_dict)
                            except:
                                print("Could not add the book name and price to the book_details list and the book_details collection in the mongo db")


                            try:
                                ## Going back to the genre home page
                                driver.back()
                            except:
                                print("Could not go back to the genre home page")

                        ## Checking whether the present page has any next button and it is present clicking on it to get to the next page
                        if len(next_btn) > 0:
                            next_button = driver.find_element(By.LINK_TEXT,'next')
                            next_button.click()
                        else:
                            break

                    except:
                        driver.quit()
                        print('Could not find any books on the given genre')

                driver.quit()
                dataframe = pd.DataFrame({"Book Name":book_name_list,"Book Price":book_price_list})
                dataframe.to_csv(os.path.join(basedir,"scrappedData","booksOnGenre{}.csv".format(genre)))
                return render_template('results.html', book_details=book_details,genre=genre)



        except:
            driver.quit()
            print("Some unknown error occurred")



    else:
        driver.quit()
        return render_template('index.html')


if __name__ == '__main__':
    app.run()