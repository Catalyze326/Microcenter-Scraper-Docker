from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium import webdriver
import mysql.connector
import time
import re

# TODO test if open box is working
# TODO write interface (discord bot)
# TODO clean up database
# TODO update price
# TODO update open box pricing
# TODO add open box to non open box
# TODO remove open box from non open box


def single_store(store):
    driver.get("https://www.microcenter.com/search/search_results.aspx?Ntk=all&sortby=match&N=22+24+23+36+37+38+39+40+41+42+43+44+45+46+47&myStore=true")
    WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, 'storeInfo')))
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
        open_box_price = float(re.sub(r'[^0-9.]', "", open_box_price))
        category = link.get_attribute("data-category")
        price = link.get_attribute("data-price")
        price = float(re.sub(r'[^0-9.]', "", price))
        brand = link.get_attribute("data-brand")
        name = link.get_attribute("data-name")
        url = link.get_attribute("href")
        return [True, name, price, open_box_price, (open_box_price / price) * 100, category, brand, url, store]
    except NoSuchElementException:
        name = link.get_attribute("data-name")
        price = link.get_attribute("data-price")
        price = re.sub(r'[^0-9.]', "", price)
        category = link.get_attribute("data-category")
        url = link.get_attribute("href")
        brand = link.get_attribute("data-brand")
        return [True, name, float(price), None, None, category, brand, url, store]


def send_to_db(values):
    try:
        connection = mysql.connector.connect(
        user='microcenter', password='2Pn36D3iM8vnTAul',
        host='mariadb-microcenter', database='microcenter')
    except:
        connection = mysql.connector.connect(
        user='microcenter', password='2Pn36D3iM8vnTAul',
        host='localhost', database='microcenter')
    cursor = connection.cursor(prepared=True)
    open_box = "AND open_box_price=%s;" if values[4] is not None else ";"
    s_values = [values[1], values[4]] if values[4] is not None else [values[1]]
    mysql_select_stmt = 'SELECT open_box_price, ' \
    'percent_difference_price, price, store FROM ' \
    'microcenter WHERE name=%s ' + open_box
    mysql_insert_stmt = "INSERT INTO microcenter" \
    " VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s);"
    cursor.execute(mysql_insert_stmt, values)
    connection.commit()
    cursor.execute(mysql_select_stmt, s_values)
    results = cursor.fetchone()
    if results is not None:
        for result in results: print(result)
    if results is None:
        print("Results were none")
        cursor.execute(mysql_insert_stmt, values)
        connection.commit()
    # Checks if it is open box in the site and not on the db
    elif results[0] is None and values[4] is not None:
        print("results were not none updating openbox")
        update_open([values[4], values[5], values[1], values[8]])
    # Checks if it is open box in the db and not on the site
    elif results[0] is not None and values[4] is None:
        print("results were not none updating openbox")
        update_open([values[3], values[4], values[1], values[8]])
    else:
        print("Results were not none. Values already exist.")

def update_open(u_values):
    connection = mysql.connector.connect(
    user='microcenter', password='2Pn36D3iM8vnTAul',
    host='mariadb-microcenter', database='microcenter')
    cursor = connection.cursor(prepared=True)
    sql_update_stmt = " UPDATE microcenter SET " \
    "open_box_price=%s, percent_difference_price=%s" \
    " WHERE name=%s AND store=%s;"
    cursor.execute(sql_update_stmt, u_values)


def update_new(open_box, u_values):
    connection = mysql.connector.connect(
    user='microcenter', password='2Pn36D3iM8vnTAul',
    host='mariadb-microcenter', database='microcenter')
    cursor = connection.cursor(prepared=True)
    sql_update_stmt = " UPDATE microcenter SET " \
    "is_new = false WHERE name=%s AND price=%s " + open_box
    cursor.execute(sql_update_stmt, u_values)
    connection.commit()
    connection.close()
    cursor.close()


time.sleep(12)
print("Initiating code:")
firefox_options = webdriver.FirefoxOptions()
driver = webdriver.Remote(
    command_executor='http://selenium-microcenter:4444',
    options=firefox_options
)
connection = mysql.connector.connect(
    user='microcenter', password='2Pn36D3iM8vnTAul',
    host='mariadb-microcenter', database='microcenter')
cursor = connection.cursor(prepared=True)
# mysql_drop_stmt = "DROP TABLE IF EXISTS microcenter;"
# cursor.execute(mysql_drop_stmt)
mysql_create_table_stmt = "CREATE TABLE IF NOT EXISTS microcenter (" \
                    " is_new boolean, " \
                    " name VARCHAR(256)," \
                    " price DOUBLE," \
                    " open_box_price DOUBLE," \
                    " percent_difference_price DOUBLE," \
                    " category VARCHAR(48)," \
                    " brand VARCHAR(128)," \
                    " url VARCHAR(256)," \
                    " store VARCHAR(32)" \
                    ");"
cursor.execute(mysql_create_table_stmt)
connection.commit()
single_store("MD - Parkville")
single_store("MD - Rockville")
single_store("VA - Fairfax")
driver.quit()
