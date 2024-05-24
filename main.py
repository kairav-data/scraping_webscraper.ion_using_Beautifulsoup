import requests
from bs4 import BeautifulSoup
import pandas as pd

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'}

try:
    baseurl = 'https://webscraper.io/test-sites/e-commerce/static/computers/tablets?page='
    product_names = []
    product_prices = []
    product_reviews = []

    # Determine the total number of pages
    response = requests.get(baseurl + '1', headers=headers)
    soup = BeautifulSoup(response.content, "html.parser")
    pagination = soup.find('ul', class_='pagination')
    pages = pagination.find_all('a', class_='page-link')
    total_pages = int(pages[-2].text)  # The second to last 'a' tag contains the last page number

    for page in range(1, total_pages + 1):
        url = baseurl + str(page)
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.content, "html.parser")

        product_elements = soup.find_all('div', class_='col-md-4 col-xl-4 col-lg-4')

        for product_desc in product_elements:
            # Scraping product Name
            product_name = product_desc.find('a', class_='title').text
            product_price = product_desc.find('h4', class_='price float-end card-title pull-right').text
            product_review = product_desc.find('p', class_='review-count float-end').text

            product_names.append(product_name)
            product_prices.append(product_price)
            product_reviews.append(product_review)

    df = pd.DataFrame({'Name': product_names, 'Price': product_prices, 'Review Count': product_reviews})
    df.to_csv('products.csv', index=False)
    print("product.csv updated")
    print(df)

except Exception as e:
    print(e)