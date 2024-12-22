import time
from typing import List
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.remote.webelement import WebElement

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
from webdriver_manager.firefox import GeckoDriverManager
import pandas as pd
import os
EMAIL =os.getenv('EMAIL')
PASSWORD =os.getenv('PASSWORD')

CATEGORIES = [
    "https://www.amazon.in/gp/bestsellers/watches/ref=zg_bs_watches_sm",
    "https://www.amazon.in/gp/bestsellers/electronics/ref=zg_bs_electronics_sm",
    "https://www.amazon.in/gp/bestsellers/automotive/ref=zg_bs_automotive_sm",
    "https://www.amazon.in/gp/bestsellers/beauty/ref=zg_bs_beauty_sm",
    "https://www.amazon.in/gp/bestsellers/books/ref=zg_bs_books_sm",
    "https://www.amazon.in/gp/bestsellers/garden/ref=zg_bs_nav_garden_0",
    "https://www.amazon.in/gp/bestsellers/apparel/ref=zg_bs_nav_apparel_0",
    "https://www.amazon.in/gp/bestsellers/office/ref=zg_bs_nav_office_0",
    "https://www.amazon.in/gp/bestsellers/sports/ref=zg_bs_nav_sports_0",
    "https://www.amazon.in/gp/bestsellers/jewelry/ref=zg_bs_nav_jewelry_0",
]

def init_firefox_driver() -> webdriver.Firefox:
    firefox_options = Options()
    firefox_options.add_argument("--headless")
    service = Service(GeckoDriverManager().install())
    driver = webdriver.Firefox(service=service, options=firefox_options)
    return driver

def login_amazon(driver: webdriver.Firefox):
    print("Logging in to Amazon...")
    driver.get("https://www.amazon.in/ap/signin?openid.pape.max_auth_age=0&openid.return_to=https%3A%2F%2Fwww.amazon.in%2Fgp%2Fbestsellers%2Fkitchen%2Fref%3Dnav_ya_signin&openid.identity=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.assoc_handle=inflex&openid.mode=checkid_setup&openid.claimed_id=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.ns=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0")
    time.sleep(3)
    driver.find_element(By.ID, "ap_email").send_keys(EMAIL)
    driver.find_element(By.ID, "continue").click()
    time.sleep(2)
    driver.find_element(By.ID, "ap_password").send_keys(PASSWORD)
    driver.find_element(By.ID, "signInSubmit").click()
    time.sleep(5)
    print("Login successful!")
def get_element_safely(driver_or_element, by, value, default=None):
    """Safely get an element with error handling."""
    try:
        element = driver_or_element.find_element(by, value)
        return element.text if element else default
    except (NoSuchElementException, StaleElementReferenceException):
        return default
def parse_product_data(product: WebElement) -> dict:
    try:
        title_element = product.find_element(By.CLASS_NAME, "_cDEzb_p13n-sc-css-line-clamp-3_g3dy1")
        title = title_element.text
    except NoSuchElementException:
        title = None

    try:
        url_element = product.find_element(By.CLASS_NAME, "a-link-normal")
        url = url_element.get_attribute("href")
    except NoSuchElementException:
        url = None

    try:
        price_element = product.find_element(By.CLASS_NAME, "_cDEzb_p13n-sc-price_3mJ9Z")
        price = price_element.text
    except NoSuchElementException:
        price = None

    try:
        discount_element = product.find_element(By.CLASS_NAME, "aok-offscreen")
        discount_text = discount_element.text
        discount = discount_text.split("with")[-1].strip() if "with" in discount_text else None
    except NoSuchElementException:
        discount = None

    try:
        img_element = product.find_element(By.TAG_NAME, "img")
        img_url = img_element.get_attribute("src")
        description = img_element.get_attribute("alt")
    except NoSuchElementException:
        img_url = None
        description = None

    try:
        ship_from_element = product.find_element(By.ID, "price-shipping-message")
        ship_from = ship_from_element.text
    except NoSuchElementException:
        ship_from = None

    try:
        sold_by_element = product.find_element(By.CSS_SELECTOR, "#sellerProfileTriggerId, #merchant-info a")
        sold_by = get_element_safely(driver, By.CSS_SELECTOR, "#sellerProfileTriggerId, #merchant-info a")
    except NoSuchElementException:
        sold_by = None

    return {
        "Title": title,
        "URL": url,
        "Price": price,
        "Discount": discount,
        "Image URL": img_url,
        "Description": description,
        "Ships From": ship_from,
        "Sold By": sold_by,
    }

def get_products_from_page(url: str, driver: webdriver.Firefox) -> List[dict]:
    print(f"Scraping category: {url}")
    driver.get(url)
    time.sleep(5)
    product_elements = driver.find_elements(By.ID, "gridItemRoot")
    products = []
    for product in product_elements:
        try:
            parsed_product = parse_product_data(product)
            products.append(parsed_product)
        except Exception as e:
            print(f"Error parsing product: {e}")
    return products

def save_to_csv(data: List[dict], filename="amazon_products.csv") -> None:
    df = pd.DataFrame(data)
    df.to_csv(filename, index=False)
    print(f"Data saved to {filename}")

def save_to_json(data: List[dict], filename="amazon_products.json") -> None:
    df = pd.DataFrame(data)
    df.to_json(filename, orient='records', lines=True)
    print(f"Data saved to {filename}")

def main():
    driver = init_firefox_driver()
    try:
        login_amazon(driver)
        all_products = []
        for category in CATEGORIES:
            products = get_products_from_page(category, driver)
            all_products.extend(products)
    finally:
        driver.quit()


    save_to_json(all_products)

if __name__ == "__main__":
    main()
