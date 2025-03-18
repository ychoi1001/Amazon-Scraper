# Amazon-Scraper

## Description

This project scrapes product data from Amazon including ASIN, Title, Brand, Amazon Choice, Star Rating, Rating Count, Rufus Question #2, Coupon Discounts, and Scrape Time. The product URLs are read from an Excel file, and the data is saved in an Excel sheet for further analysis.

## Features

- Scrapes Amazon product pages using Selenium WebDriver
- Extracts important product details such as ASIN, Title, Brand, Star Rating, and more
- Handles login to Amazon using credentials provided by the user
- Exports the scraped data to an Excel file for easy usage and analysis
- Uses **headless browsing** to run the scraper without opening a browser window

## Notes

- Make sure your Amazon credentials are correct and that you have access to the products you are trying to scrape.
- If you're scraping many products, please be mindful of Amazon's terms of service regarding web scraping.
- The scraper uses a headless browser to run the process without opening a visible browser window, which makes it suitable for running in the background.
- You will need an Excel file (`url.xlsx`) with a column named `url`, containing the product URLs you want to scrape. You can create the Excel file manually or generate it using the provided Python script.

