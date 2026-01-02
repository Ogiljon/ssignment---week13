import requests
import random

print("================================================")
print(" FIND YOUR NEXT READ WITH RANDOM BOOOK WHEEL📖")
print("================================================\n")
genre = str(input("Choose the book genre(e.g. fantasy, romance, mystery, sci-fi): "))
genre = genre.strip()
if genre == "":
    print("You didn't type anything! 'Fantasy' will be used to search by default")
    genre = "fantasy"
genre = genre.lower()

url = 'https://openlibrary.org/search.json'
params = {
    'q': genre,
    'limit': 50,
    'fields': "title,author_name,first_publish_year,edition_count,key"
    }

response = requests.get(url, params=params)
if response.status_code == 200:
    print('Connection successfull')
    data = response.json()
    all_books = data.get("docs")
elif response.status_code == 404:
    print('Page not found')
elif response.status_code == 500:
    print("Server error, try again later")
else:
    print(f"Other status: {response.status_code}")
   
modern_books = []
for book in all_books:
    year = book.get("first_publish_year")
    editions = book.get("edition_count", 0)
    if year is not None:
        try:
            if int(year) >= 1950 and editions >= 20:
                modern_books.append(book)
        except (TypeError, IndexError, KeyError, ValueError):
            continue 
    
for i in range(len(modern_books)):
    for j in range(len(modern_books) - 1):
        try:
            book1_editions = modern_books[j].get("edition_count", 0)
            book2_editions = modern_books[j + 1].get("edition_count", 0)
            
            if book1_editions < book2_editions:
                temporary = modern_books[j]
                modern_books[j] = modern_books[j + 1]
                modern_books[j + 1] = temporary
        except (IndexError, TypeError, ValueError, NameError):
            continue  
    
if len(modern_books) == 0:
    print(f"Sorry, could not find any '{genre}' books published after 1950")
    print("Try another genre for more options...")
else:
    print(f"Great!!! {len(modern_books)} books were found for '{genre}' book genre!\n")

    lucky_book = random.choice(modern_books)
    title = lucky_book.get("title", "No title")
    authors_list = lucky_book.get("author_name", ["Unknown Author"])
    author_text = ", ".join(authors_list)
    year = lucky_book.get("first_publish_year", "Unknown year")
    editions = lucky_book.get("edition_count", 0)
    link = "https://openlibrary.org" + lucky_book.get("key", "")

    print('-' *32)
    print('YOUR RANDOM BOOK RECOMMENDATION')
    print('-' *32)
    print(f'Title: {title}')
    print(f'Author(s): {author_text}')
    print(f'First published: {year}')
    print(f'Editions: {editions}')
    print(f'Read more here: {link}')
    print('-' *60)  
    print('\nEnjoy your book! Happy reading!\n')



