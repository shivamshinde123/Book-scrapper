
# Book Name and Price Scrapping based on the genre provided
1. This scrapper will scrap the book names and their respective prices based on the genre provided by the user

2. Scrapper scraps the data from the website http://books.toscrape.com/

3. Scrapper mainly uses the libraries BeautifulSoup and selenium python to scrap the data.

4. The scrapped data will be extracted as a csv file in the scrappedData folder in the same directory as the project.

5. User will be able to provide the his/her desired genre on the Home html page.

6. The request module will take the genre provided by the user from the html page and scraps the book name and price for that genre from the above mentioned website. The scrapped data will be stored as a csv file in scrappedData folder.


## Screenshots

Home Page Screenshot 1:
[![Homepage1.png](https://i.postimg.cc/jd7LfWsK/Homepage1.png)](https://postimg.cc/PPdXs5pF)

Home Page Screenshot 2:
[![Homepage2.png](https://i.postimg.cc/4nk4P5JG/Homepage2.png)](https://postimg.cc/cthN4fgk)

Results Page Screenshot:
[![Results-Page.png](https://i.postimg.cc/KvD4f6gs/Results-Page.png)](https://postimg.cc/nCMHcw2v)


## Run Locally

Clone the project

```bash
  git clone https://github.com/shivamshinde123/Book-scrapper
```

Go to the project directory

```bash
  cd Book-scrapper
```

Please put the chromedriver compatible with the chrome browser on your computer in the root directory of the project.

Please create a directory named "scrappedData" in the root directory of the project to store the scrapped data

Create a conda environment
```bash
conda create -n environment_name
```

Activate the created conda environment

```bash
conda activate environment_name
```

Install dependencies

```bash
  pip install -r requirements.txt
```

Execute the code

```bash
  python app.py
```

## Authors

- [@ShivamShinde](https://github.com/shivamshinde123)


## 🔗 Links

[![linkedin](https://img.shields.io/badge/linkedin-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/shivamds92722)

[![github-logo.png](https://i.postimg.cc/LhK0xCHs/github-logo.png)](https://github.com/shivamshinde123/)

[![tableau-public-logo.png](https://i.postimg.cc/tRr7ZKBk/tableau-public-logo.png)](https://public.tableau.com/app/profile/shivam.shinde#!/?newProfile=&activeTab=0)