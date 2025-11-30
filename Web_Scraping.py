import requests
from bs4 import BeautifulSoup
import csv

def scrape_books():
    # The URL of the website designed for scraping practice
    url = 'http://books.toscrape.com/catalogue/category/books_1/index.html'
    
    # It's good practice to include a User-Agent to mimic a real browser
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    try:
        print(f"Fetching data from {url}...")
        response = requests.get(url, headers=headers)
        
        # Check if the request was successful
        if response.status_code != 200:
            print(f"Failed to retrieve the page. Status code: {response.status_code}")
            return

        # Parse the HTML content
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Find all HTML containers that hold book information
        # On this site, every book is inside an <article class="product_pod">
        books = soup.find_all('article', class_='product_pod')
        
        extracted_data = []

        # A dictionary to convert word ratings to numbers
        rating_mapper = {'One': 1, 'Two': 2, 'Three': 3, 'Four': 4, 'Five': 5}

        for book in books:
            # 1. Extract Title
            # The title is inside an <h3> tag, inside an <a> tag. 
            # We use the 'title' attribute because the visible text might be truncated.
            title = book.h3.find('a')['title']

            # 2. Extract Price
            # The price is inside a <p> tag with class "price_color"
            price_text = book.find('p', class_='price_color').text
            # Remove the '£' symbol to keep it numeric
            price = price_text.replace('$', '')

            # 3. Extract Rating
            # The rating is stored as a class name (e.g., "star-rating Three")
            rating_tag = book.find('p', class_='star-rating')
            rating_classes = rating_tag['class'] # Returns a list like ['star-rating', 'Three']
            
            # Filter out 'star-rating' to get the specific number word
            rating_word = [cls for cls in rating_classes if cls != 'star-rating'][0]
            rating = rating_mapper.get(rating_word, 0)

            extracted_data.append({
                'Name': title,
                'Price (£)': price,
                'Rating (Out of 5)': rating
            })

        # Save to CSV
        filename = 'scraped_books.csv'
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['Name', 'Price ($)', 'Rating (Out of 5)']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writeheader()
            writer.writerows(extracted_data)

        print(f"Successfully scraped {len(extracted_data)} books.")
        print(f"Data saved to '{filename}'")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    scrape_books()