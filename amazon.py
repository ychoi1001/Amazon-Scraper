# **************************************************
# Olivia Choi
# Date: 2025-03-13
# Description: Scrapes product data including ASIN, 
# Title, Brand, Amazon Choice, Star Rating, 
# Rating Count, Rufus Question 2, Coupon Discounts, 
# and Scrape Time
# **************************************************

# Import necessary packages
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from openpyxl import Workbook
from getpass import getpass
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd

# Set up Chrome options
# Customize the behavior of the Chrome browser when you launch it with WebDriver
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--start-maximized")
chrome_options.add_argument("--headless")  # Operates in the background without showing the browser window
chrome_options.add_argument("--disable-gpu")  # Disable GPU acceleration

# Initialize the WebDriver to automate interactions with a web browser
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

# Amazon login credentials
amazon_email = input("Enter your Amazon email: ")
amazon_password = getpass("Enter your Amazon password: ")

# Function to Log in to Amazon
def amazon_login():
    driver.get("https://www.amazon.com/gp/sign-in.html")
    time.sleep(3)

    try:
        # Enter email
        email_input = driver.find_element(By.ID, "ap_email") # Locate email input field
        email_input.send_keys(amazon_email) # Enter email
        email_input.send_keys(Keys.RETURN) # Press Enter key
        time.sleep(3)

        # Enter password
        password_input = driver.find_element(By.ID, "ap_password")
        password_input.send_keys(amazon_password)
        password_input.send_keys(Keys.RETURN)
        time.sleep(5)

        # Wait for an element that confirms login
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "nav-link-accountList"))  
        )
        print("Login successful!")

    except Exception as e:
        print(f"Login failed: {e}")
        driver.quit()

# Function to extract ASIN from URL
# https://www.amazon.com/dp/B0CCW6WLJ9
def get_asin_from_url(url):
    if "/dp/" in url:
        asin = url.split("/dp/")[1].split("/")[0]
        return asin
    return "N/A"

# Load the Excel file
df = pd.read_excel("url.xlsx") # can also index sheet by name or fetch all sheets

# Extract URLs from the 'url' column and convert to a Python list
product_urls = df["url"].dropna().tolist()

# Set up Excel workbook
wb = Workbook()
ws = wb.active
ws.append(["ASIN", "Title", "Brand", "Amazon Choice", "Star Rating", "Rating Count", "Rufus Question #2", "Coupon Discount", "Scrape Time"])

# Function to scrape product data
def scrape_amazon_product(url):
    # Open URL
    driver.get(url)
    time.sleep(3)

    # Get ASIN
    asin = get_asin_from_url(url)
    
    # try:
    #     asin2 = driver.find_element(By.XPATH, "//th[text() = ' ASIN ' ]/following-sibling::td").text
    # except:
    #     asin2 = "N/A"

    # Extract Product Title
    try:
        title = driver.find_element(By.ID, "productTitle").text.strip()
    except:
        title = "N/A"

    # Extract Brand Name
    try:
        brand = driver.find_element(By.ID, "bylineInfo").text.replace("Visit the ", "").replace(" Store", "")
    except:
        brand = "N/A"

    # Check for Amazon's Choice label
    try:
        amazon_choice = driver.find_element(By.CLASS_NAME, 'ac-badge-wrapper')
        amazon_choice_exists = "Yes" if amazon_choice else "No"
    except:
        amazon_choice_exists = "No"

    # Extract Star Rating
    try:
        star_rating = driver.find_element(By.CSS_SELECTOR, "#acrPopover span.a-size-base.a-color-base")
        star_rating = float(star_rating.text.strip())
    except:
        star_rating = "N/A"

    # Extract Rating Count
    try:
        rating_count = driver.find_element(By.ID, "acrCustomerReviewText").text.split()[0]
        rating_count = int(rating_count.split()[0].replace(',', ''))
    except:
        rating_count = "N/A"

    # Extract the second rufus question
    try:
        # Find all the question buttons
        question_buttons = driver.find_elements(By.CSS_SELECTOR, 'span.a-declarative button.small-widget-pill')
        second_rufus_question = question_buttons[1].text if len(question_buttons) > 1 else "N/A"
    except:
        second_rufus_question = "N/A"

    # Extract Coupon Discount
    try:
        coupon_discount_text = driver.find_element(By.XPATH, "//label[contains(@id, 'couponText')]").text.strip()
        
        # Split the text and check for percentage
        # parts = ["Apply", "25%", "off", "coupon"]
        parts = coupon_discount_text.split()
        if len(parts) > 1 and '%' in parts[1]:
            coupon_discount = parts[1]
        else:
            coupon_discount = "N/A"
    except:
        coupon_discount = "N/A"

    # Scrape Time
    scrape_time = time.strftime("%Y-%m-%d %H:%M:%S")

    # Returns a list 
    return [asin, title, brand, amazon_choice_exists, star_rating, rating_count, second_rufus_question, coupon_discount, scrape_time]

# Run the scraper
amazon_login()

for i, url in enumerate(product_urls, start=1):
    print(f"Scraping link {i}...")
    product_data = scrape_amazon_product(url)
    ws.append(product_data)
    print(f"Scraped: {product_data}")

# Save to Excel
wb.save("amazon_data.xlsx")
print("Data saved to amazon_data.xlsx")

# Close the driver
driver.quit()
