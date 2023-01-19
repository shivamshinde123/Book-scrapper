
# Book Price Scrapper
![](https://img.shields.io/github/last-commit/shivamshinde123/Book-scrapper)
![](https://img.shields.io/github/languages/count/shivamshinde123/Book-scrapper)
![](https://img.shields.io/github/languages/top/shivamshinde123/Book-scrapper)
![](https://img.shields.io/github/repo-size/shivamshinde123/Book-scrapper)
![](https://img.shields.io/github/directory-file-count/shivamshinde123/Book-scrapper)
![](https://img.shields.io/github/license/shivamshinde123/Book-scrapper)

# Problem Statement
1. This scrapper will scrap the book names and their respective prices based on the genre provided by the user. 

2. Scrapper scraps the data from the website http://books.toscrape.com/

3. Scrapper mainly uses the libraries BeautifulSoup and selenium python to scrap the data.

4. The scrapped data will be extracted as a csv file in the scrappedData folder in the same directory as the project.

5. User will be able to provide the his/her desired genre on the Home html page.

6. The request module will take the genre provided by the user from the html page and scraps the book name and price for that genre from the above mentioned website. The scrapped data will be stored as a csv file in scrappedData folder and it is also showed on the results html page.


## Screenshots

Home Page:

![Home Page](https://i.postimg.cc/tRvbtGCR/Homepage1.png)

Home Page (Selecting a genre):

![Home Page (Selecting a genre)](https://i.postimg.cc/5NHVsK6B/Homepage2.png)

Results Page:

![Results Page](https://i.postimg.cc/CLWVXCqW/Results-Page.png)


## Run Locally

Clone the project

```bash
  git clone https://github.com/shivamshinde123/Book-scrapper
```

Go to the project directory

```bash
  cd Book-scrapper
```

Create a conda environment
```bash
conda create -n environment_name python=3.10
```

Activate the created conda environment

```bash
conda activate environment_name
```

Install dependencies

```bash
  pip install -r requirements.txt
```

After installing the dependencies, open the mongo db compass and create a new connection and then click on connect button.

Opening mongo db compass:

![MongoDB Compass Home Page](https://i.postimg.cc/bYmnxrtG/mongodb-connect1.png)

After clicking on Connect button:

![Clicking on Connect button](https://i.postimg.cc/RVqHXm7g/mongodb-connect2.png)

Come back to the code editor and execute the code

```bash
  python app.py
```

## Authors

- [@ShivamShinde](https://github.com/shivamshinde123)


## 🔗 Links

[![linkedin](https://img.shields.io/badge/linkedin-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/shivamds92722)

[![github-logo.png](https://i.postimg.cc/LhK0xCHs/github-logo.png)](https://github.com/shivamshinde123/)

[![tableau-public-logo.png](https://i.postimg.cc/tRr7ZKBk/tableau-public-logo.png)](https://public.tableau.com/app/profile/shivam.shinde#!/?newProfile=&activeTab=0)

Also check out my website for more projects at [ShivamShinde](http://shivamdshinde.com/)
