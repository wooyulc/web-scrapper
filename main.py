# dealing multiple pages with Selenium
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time

options = Options()
#options.headless = True
options.add_argument('window-size=1920x1080')

web = "https://www.audible.com/adblbestsellers?ref=a_search_t1_navTop_pl0cg1c0r0&pf_rd_p=1bb99d4d-8ec8-42a3-bb35-704e849c2bc6&pf_rd_r=5Y8NXMAXHA2ZAFWWNT45&pageLoadId=hg6SuvkcTJZvZ1N8&creativeId=1642b4d1-12f3-4375-98fa-4938afc1cedc"
driver = webdriver.Chrome(options=options)
driver.get(web)
driver.maximize_window()

# pagination
pagination = driver.find_element(By.XPATH, '//ul[contains(@class, "pagingElements")]')
pages = pagination.find_elements(By.TAG_NAME, 'li')
last_page = int(pages[-2].text)

current_page = 1
book_title = []
book_author = []
book_length = []

while current_page <= last_page:
    container = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CLASS_NAME, 'adbl-impression-container')))
    # container = driver.find_element(By.CLASS_NAME, 'adbl-impression-container')
    # products = container.find_elements(By.XPATH, './/li[contains(@class, "productListItem")]')
    products = WebDriverWait(container, 5).until(EC.presence_of_all_elements_located((By.XPATH, './/li[contains(@class, "productListItem")]')))
    print(product.find_element(By.XPATH, './/h3[contains(@class, "bc-heading")]').text)
    for product in products:
        book_title.append(product.find_element(By.XPATH, './/h3[contains(@class, "bc-heading")]').text)
        book_author.append(product.find_element(By.XPATH, './/li[contains(@class, "authorLabel")]').text)
        book_length.append(product.find_element(By.XPATH, './/li[contains(@class, "runtimeLabel")]').text)

    current_page += 1

    try:
        next_page = driver.find_element(By.XPATH, '//span[contains(@class, "nextButton")]')
        next_page.click()
    except:
        pass


driver.quit()

df_books = pd.DataFrame({'title': book_title, 'author': book_author, 'book_length': book_length}).sort_values(by=['book_length'])
df_books.to_csv('multiple_page.csv', index=False)
