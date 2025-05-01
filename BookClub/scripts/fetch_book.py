import requests
import json
import os
from datetime import datetime

# Constants
OPEN_LIBRARY_SEARCH_URL = "https://openlibrary.org/search.json"
OPEN_LIBRARY_COVER_URL = "https://covers.openlibrary.org/b/id/{}-L.jpg"
BOOKS_DIR = "books"
LATEST_FILE = os.path.join(BOOKS_DIR, "latest.json")

# Ensure the books directory exists
os.makedirs(BOOKS_DIR, exist_ok=True)

def fetch_random_book():
    """
    Fetches a random book from Open Library.
    """
    try:
        # Search for books with a common subject to get varied results
        params = {
            'subject': 'fiction',
            'limit': 50
        }
        response = requests.get(OPEN_LIBRARY_SEARCH_URL, params=params)
        response.raise_for_status()
        data = response.json()
        books = data.get('docs', [])
        if not books:
            print("No books found.")
            return None
        # Select a random book
        import random
        book = random.choice(books)
        return book
    except Exception as e:
        print(f"Error fetching book: {e}")
        return None

def generate_book_entry(book):
    """
    Generates a dictionary with book details.
    """
    title = book.get('title', 'No Title')
    author = ', '.join(book.get('author_name', ['Unknown Author']))
    publish_date = book.get('first_publish_year', 'Unknown')
    cover_id = book.get('cover_i')
    cover_image = OPEN_LIBRARY_COVER_URL.format(cover_id) if cover_id else ''
    summary = book.get('first_sentence', {}).get('value', 'No summary available.')
    isbn_list = book.get('isbn', [])
    amazon_link = f"https://www.amazon.com/s?k={isbn_list[0]}" if isbn_list else "https://www.amazon.com"

    return {
        'title': title,
        'author': author,
        'publish_date': publish_date,
        'cover_image': cover_image,
        'summary': summary,
        'amazon_link': amazon_link
    }

def save_book_entry(entry):
    """
    Saves the book entry as a JSON file.
    """
    date_str = datetime.utcnow().strftime('%Y-%m-%d')
    file_path = os.path.join(BOOKS_DIR, f"{date_str}.json")
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(entry, f, ensure_ascii=False, indent=4)
    # Update latest.json
    with open(LATEST_FILE, 'w', encoding='utf-8') as f:
        json.dump(entry, f, ensure_ascii=False, indent=4)

def main():
    book = fetch_random_book()
    if book:
        entry = generate_book_entry(book)
        save_book_entry(entry)
        print(f"Book entry for '{entry['title']}' saved successfully.")
    else:
        print("Failed to fetch a book.")

if __name__ == "__main__":
    main()
