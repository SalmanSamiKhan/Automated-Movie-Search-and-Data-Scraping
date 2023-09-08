# Import
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.select import Select
from bs4 import BeautifulSoup as bs
import requests
import pandas as pd

# Part 1 - Browser Automation with Selenium

options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True)
options.add_argument("--start-maximized")
driver = webdriver.Chrome(options=options)
wait = WebDriverWait(driver, 10)
driver.get("http:www.imdb.com")
driver.implicitly_wait(5)

# search = driver.find_element(By.XPATH, "//input[@id='suggestion-search']")
# search.send_keys("Godfather")

# All Dropdown
all_dropdown = driver.find_element(
    By.XPATH, "//span[@class='ipc-btn__text'][normalize-space()='All']"
)
# driver.implicitly_wait(5)
all_dropdown.click()

advanced_search = driver.find_element(
    By.XPATH,
    "//a[@class='ipc-list__item searchCatSelector__item']//span[@role='presentation'][normalize-space()='']",
)
advanced_search.click()

advanced_title_search = driver.find_element(By.XPATH, '//*[@id="main"]/div[2]/div[1]/a')
advanced_title_search.click()

title_type_1 = driver.find_element(By.ID, "title_type-1")
title_type_1.click()

# title_type_3 = driver.find_element(By.ID,'title_type-3')
# title_type_3.click()

release_date_min = driver.find_element(By.NAME, "release_date-min")
release_date_min.send_keys(1980)

release_date_max = driver.find_element(By.NAME, "release_date-max")
release_date_max.send_keys(2023)

rating_min = driver.find_element(By.NAME, "user_rating-min")
rating_min.click()
rating_min_dropdown = Select(rating_min)
rating_min_dropdown.select_by_visible_text("6.0")

rating_max = driver.find_element(By.NAME, "user_rating-max")
rating_max.click()
rating_max_dropdown = Select(rating_max)
rating_max_dropdown.select_by_visible_text("10")

# genre_1 = driver.find_element(By.ID,'genres-6')
# genre_1.click()
genre_2 = driver.find_element(By.ID, "genres-24")
genre_2.click()
# genre_3 = driver.find_element(By.ID,'genres-26')
# genre_3.click()

title_group_1 = driver.find_element(By.ID, "groups-7")
title_group_1.click()

language = driver.find_element(By.NAME, "languages")
language_dropdown = Select(language)
language_dropdown.select_by_visible_text("English")

page_count = driver.find_element(By.ID, "search-count")
page_count_dropdown = Select(page_count)
page_count_dropdown.select_by_visible_text("250 per page")

submit = driver.find_element(By.XPATH, '(//button[@type="submit"])[2]')
submit.click()

current_url = driver.current_url

sort_by_rating = driver.find_element(By.XPATH, "//a[normalize-space()='User Rating']")
sort_by_rating.click()

# Part 2 - Data Extraction with Beautiful Soup

# Response
response = requests.get(current_url)

# Soup Object
soup = bs(response.content, "html.parser")

# All movie list
list_items = soup.find_all("div", {"class": "lister-item"})

# List Comprehension

# All fields
title = [result.find("h3").find("a").get_text().strip() for result in list_items]
year = [
    result.find("h3")
    .find("span", {"class": "lister-item-year"})
    .get_text()
    .replace("(", "")
    .replace(")", "")
    .replace("I", "")
    for result in list_items
]
runtime = [
    result.find("p").find("span", {"class": "runtime"}).get_text().strip()
    for result in list_items
]
genre = [
    result.find("span", {"class": "genre"}).get_text().strip() for result in list_items
]
rating = [
    result.find("div", {"class": "ratings-imdb-rating"}).get_text().strip()
    for result in list_items
]

# Dataframe
pd.set_option("display.max_rows", None)
pd.set_option("display.max_columns", None)

df = pd.DataFrame(
    {
        "Title": title,
        "Year": year,
        "Duration": runtime,
        "Genre": genre,
        "Rating": rating,
    }
)

# Convert the 'Value' column to numeric dtype
df["Year"] = pd.to_numeric(df["Year"], errors="coerce")
df["Rating"] = pd.to_numeric(df["Rating"], errors="coerce")


df.to_excel("movie_list.xlsx", index=False)
