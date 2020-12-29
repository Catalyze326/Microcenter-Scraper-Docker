from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium import webdriver
import mysql.connector
import time
import re


def single_store(store):
    driver.get("https://www.microcenter.com/search/search_results.aspx?Ntk=all&sortby=match&N=22+24+23+36+37+38+39+40+41+42+43+44+45+46+47&myStore=true")
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'storeInfo')))
    list_of_stores = driver.find_elements_by_class_name("dropdown-itemLI")
    for current_store in list_of_stores:
        if current_store == store:
            current_store.click()
            break
    while True:
        page_nums = driver.find_element_by_class_name("pages")
        page_nums = page_nums.find_elements_by_tag_name("li")
        if str(page_nums[len(page_nums) - 1].text) != ">": return
        else: page_nums[len(page_nums) - 1].click()
        links = driver.find_elements_by_xpath("//a[contains(@id, 'hypProductH2_')]")
        prices = driver.find_elements_by_xpath("//div[@class='price_wrapper']")
        for link, price in zip(links, prices): send_to_db(parse_item(link, price, store))


def parse_item(link, price, store):
    try:
        open_box_price = price.find_element_by_xpath("//div[@class='clearance']/span").text
        re.sub(r'[^0-9.]', "", open_box_price)
        name = link.get_attribute("data-name")
        price = link.get_attribute("data-price")
        category = link.get_attribute("data-category")
        url = link.get_attribute("href")
        brand = link.get_attribute("data-brand")
        return [name, float(price), float(open_box_price), (open_box_price / price) * 100, category, brand, url, store]
    except NoSuchElementException:
        name = link.get_attribute("data-name")
        price = link.get_attribute("data-price")
        category = link.get_attribute("data-category")
        url = link.get_attribute("href")
        brand = link.get_attribute("data-brand")
        return [name, price, None, None, category, brand, url, store]


def send_to_db(values):
    connection = mysql.connector.connect(
                                user='microcenter',
                                password='2Pn36D3iM8vnTAul',
                                host='mariadb-microcenter',
                                database='microcenter')
    cursor = connection.cursor(prepared=True)
    mysql_insert_stmt = "INSERT INTO microcenter VALUES(%s,%s,%s,%s,%s,%s,%s,%s);"
    cursor.execute(mysql_insert_stmt, values)
    connection.commit()
    print(values)


time.sleep(3)
firefox_options = webdriver.FirefoxOptions()
driver = webdriver.Remote(
    command_executor='http://selenium-microcenter:4444',
    options=firefox_options
)
connection = mysql.connector.connect(
    user='microcenter',
    password='2Pn36D3iM8vnTAul',
    host='mariadb-microcenter',
    database='microcenter')
mysql_insert_stmt = "DROP TABLE microcenter;"
cursor = connection.cursor(prepared=True)
cursor.execute(mysql_insert_stmt)
mysql_insert_stmt = "CREATE TABLE IF NOT EXISTS microcenter (" \
                    " name VARCHAR(256)," \
                    " price DOUBLE," \
                    " open_box_price DOUBLE," \
                    " percent_difference_price DOUBLE," \
                    " category VARCHAR(48)," \
                    " brand VARCHAR(128)," \
                    " url VARCHAR(256)," \
                    " store VARCHAR(32)" \
                    ");"
cursor.execute(mysql_insert_stmt)
connection.commit()
single_store("MD - Parkville")
driver.quit()
