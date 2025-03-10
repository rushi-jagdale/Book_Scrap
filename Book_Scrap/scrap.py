import requests
from bs4 import BeautifulSoup
import csv
import time

def scrape_books():
    base_url = "http://books.toscrape.com/catalogue/page-{}.html"
    books = []
    
    for page in range(1, 6):
        response = requests.get(base_url.format(page))
        soup = BeautifulSoup(response.content, 'html.parser')
      
        
        for book in soup.select('article.product_pod'):
            title = book.h3.a['title']
            price = book.select('.price_color')[0].get_text()
            stock = 'In stock' if 'In stock' in book.select('.instock')[0].text else 'Out of stock'
            rating = book.p['class'][1]  # e.g., 'Three' for 3-star rating
            print(title)
            # Get book details page
            book_url = "http://books.toscrape.com/catalogue/" + book.h3.a['href']
            book_resp = requests.get(book_url)
            book_soup = BeautifulSoup(book_resp.content, 'html.parser')
            
            description = book_soup.select('.product_description')[0].get_text(strip=True) if book_soup.select('.product_description') else ''
            
            # Product information table
            product_info = {}
            for row in book_soup.select('.table.table-striped tr'):
                key = row.th.text.strip()
                value = row.td.text.strip()
                product_info[key] = value

            print(book_soup)    
            category = book_soup.select('.breadcrumb li')[2].text.strip()
            
            books.append({
                'Title': title,
                'Price': price,
                'Stock': stock,
                'Rating': rating,
                'Description': description,
                'Category': category,
                'Product Info': product_info
            })
            
            time.sleep(1)  # Be polite
        
    # Save to CSV
    with open('books.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=books[0].keys())
        writer.writeheader()
        writer.writerows(books)
    print("Scraping completed. Data saved to books.csv")

# scrape_books()



#Quotes to Scrape (10-20 distinct authors)
def scrape_authors():
    authors = set()
    page = 1
    
    while len(authors) < 20:
        url = f"http://quotes.toscrape.com/page/{page}/"
        response = requests.get(url)
        
        if "No quotes found!" in response.text:
            break
            
        soup = BeautifulSoup(response.content, 'html.parser')
        
        for quote in soup.select('.quote'):
            author_link = quote.select('a[href^="/author/"]')[0]['href']
            
            # Scrape author page
            author_url = f"http://quotes.toscrape.com{author_link}"
            author_resp = requests.get(author_url)
            author_soup = BeautifulSoup(author_resp.content, 'html.parser')
            
            name = author_soup.h3.text.strip()
            born_date = author_soup.select('.author-born-date')[0].text.strip()
            born_location = author_soup.select('.author-born-location')[0].text.strip()
            description = author_soup.select('.author-description')[0].text.strip()
            
            authors.add((name, born_date, born_location, description))
            
            if len(authors) >= 20:
                break
                
            time.sleep(1)
        
        page += 1
    
    # Save to CSV
    with open('authors.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['Name', 'Birth Date', 'Nationality', 'Description'])
        for author in list(authors)[:20]:
            writer.writerow(author)
    print("Scraping completed. Data saved to authors.csv")

# scrape_authors()


def scrape_random_wikipedia():
    url = "https://en.wikipedia.org/wiki/Special:Random"
    response = requests.get(url, allow_redirects=True)
    
    soup = BeautifulSoup(response.content, 'html.parser')
    title = soup.find('h1').text
    content = soup.select('div.mw-parser-output > p')[0].text.strip()
    
    print(f"Title: {title}\n")
    print(f"Content: {content[:500]}...")  # Show first 500 characters

# scrape_random_wikipedia()