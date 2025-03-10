
###  main.py

from Book_Scrap.scrap import scrape_books
from Book_Scrap.scrap import scrape_authors
from Book_Scrap.scrap import scrape_random_wikipedia

def main():
    print("Starting scraping process...")
    scrape_books()
    scrape_authors()
    scrape_random_wikipedia()
    print("All scraping tasks completed!")

if __name__ == "__main__":
    main()