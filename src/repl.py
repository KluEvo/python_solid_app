from src.services import generate_books
from src.domain.book import Book
from src.domain.checkout_record import CheckoutRecord
from src.services.book_service import BookService
from src.services.checkout_service import CheckoutService
from src.services.book_analytics_service import BookAnalyticsService
from src.repositories.book_repository import BookRepository
from src.repositories.checkout_repository import CheckoutRepository
import requests

class BookREPL:
    def __init__(self, book_svc, lib_svc, book_analytics_svc):
        self.running = True
        self.book_svc = book_svc
        self.lib_svc = lib_svc
        self.book_analytics_svc = book_analytics_svc

    def start(self):
        print('Welcome to the book app! Type \'Help\' for a list of commands!')
        while self.running:
            cmd = input('>>>').strip()
            self.handle_command(cmd)

    def handle_command(self, cmd):
        match cmd:
            case 'exit':
                self.running = False
                print("goodbye!")
            case 'getAllBooks':
                self.get_all_books()
            case 'addBook':
                self.add_book()
            case 'findByName':
                self.find_book_by_name()
            case 'removeBook':
                self.remove_book()
            case 'updateBook':
                self.update_book()
            case 'getAveragePrice':
                self.get_average_price()
            case 'getTopBooks':
                self.get_top_books()
            case 'getValueScores':
                self.get_value_scores()
            case 'medianPriceByGenre':
                self.get_median_price_by_genre()
            case 'priceSD':
                self.get_price_std_dev()
            case 'priceCorr':
                self.get_price_correlation()
            case 'pricePercent':
                self.get_price_percentiles()
            case 'ratingHist':
                self.get_rating_histogram()
            case 'genrePop2026':
                self.get_most_popular_genre_2026()
            case 'checkIn':
                self.check_in_book()
            case 'checkOut':
                self.check_out_book()
            case 'checkoutHist':
                self.get_check_out_history()
            case 'pltCommonGenre':
                self.plot_most_common_genres()
            case 'pltHighRatedGenre':
                self.plot_highest_rated_genres()
            case 'pltPriceVSRating':
                self.plot_price_vs_rating()
            case 'pltBooksYear':
                self.plot_books_by_year()
            case 'pltCheckedOutVsAvailable':
                self.plot_checked_out_vs_available()
            case 'getJoke':
                self.get_joke()
            case 'help':
                print("Commands:")
                print("getAllBooks, addBook, removeBook, updateBook, findByName, getJoke, help, exit")
                print("getAveragePrice, getTopBooks, getValueScores, medianPriceByGenre, genrePop2026")
                print("priceSD, pricePercent, priceCorr, ratingHist")
                print("pltCommonGenre, pltHighRatedGenre, pltPriceVSRating, pltBooksYear, pltCheckedOutVsAvailable")
                print("checkIn, checkOut, checkoutHist")
            case _:
                print("No valid command detected")

    def get_joke(self):
        try:
            url = 'https://api.chucknorris.io/jokes/random'
            response = requests.get(url, timeout=5)
            response.raise_for_status()
            print(response.json()['value'])
        except requests.exceptions.Timeout:
            print('Request timed out.')
        except requests.exceptions.HTTPError as e:
            print(f'HTTP Error: {e}')
        except requests.exceptions.RequestException as e:
            print(f'Something else went wrong: {e}')

    def find_book_by_name(self):
        query = input('Please enter book name: ')
        books = self.book_svc.find_book_by_name(query)
        print(books)

    def get_all_books(self):
        books = self.book_svc.get_all_books()
        print(books)

    def add_book(self):
        try:
            print('Enter Book Details:')
            title = input('Title: ')
            author = input('Author: ')
            book = Book(title= title, author=author)
            new_book_id = self.book_svc.add_book(book)
            print(new_book_id)
        except Exception as e:
            print(f'An unexpected error has occurred: {e}')

    def get_exact_book(self, title, author):
        try:
            books = self.book_svc.find_book_by_name_and_author(title, author)
            if len(books) > 1:
                print("Multiple books with the same author and title:")
                for i in range(len(books)):
                    print(f"{i+1}. {books[i]}")
                book_selection = int(input("Which book to remove? Enter the number: "))
                book_target_id = books[book_selection -1].book_id
            elif len(books) == 0:
                if not isinstance(title, str):
                    raise TypeError('Expected str, got something else.')
            else:
                book_target_id = books[0].book_id
            return book_target_id
        except Exception as e:
            print(f'An unexpected error has occurred in get_exact_book: {e}')

    def remove_book(self):
        try:
            print('Enter Book Details:')
            title = input('Title: ')
            author = input('Author: ')
            book_id = self.get_exact_book(title, author)
            removed_book_id = self.book_svc.remove_book(book_id)
            print(removed_book_id)
        except Exception as e:
            print(f'An unexpected error has occurred in remove_book: {e}')

    def update_book(self):
        try:
            print('Enter title and author of the Book you want to change:')
            title = input('Title: ')
            author = input('Author: ')
            book_id = self.get_exact_book(title, author)
            book_dict = Book(title= title, author=author).to_dict()
            print('Enter updated details:')
            updated_fields_dict = {}
            for key in book_dict.keys():
                if key == 'book_id':
                    continue
                updated_field = input(f'{key}: ')
                if updated_field != "":
                    updated_fields_dict[key] = updated_field 

            updated_book_id = self.book_svc.update_book(book_id, updated_fields_dict)
            print(f"Updated book with id {updated_book_id}")
        except Exception as e:
            print(f'An unexpected error has occurred in update_book: {e}')

    def check_in_book(self):
        try:
            print('Enter title and author of the Book you want to check in:')
            title = input('Title: ')
            author = input('Author: ')
            book_id = self.get_exact_book(title, author)
            print(self.book_svc.find_book_by_id(book_id))

            record = self.lib_svc.check_in_book(book_id)

            print(f"{record}")
        except Exception as e:
            print(f'An unexpected error has occurred in check_in_book: {e}')
        
    def check_out_book(self):
        try:
            print('Enter title and author of the Book you want to check out:')
            title = input('Title: ')
            author = input('Author: ')
            book_id = self.get_exact_book(title, author)

            record = self.lib_svc.check_out_book(book_id)

            print(f"{record}")
        except Exception as e:
            print(f'An unexpected error has occurred in check_out_book: {e}')
        
    def get_check_out_history(self):
        try:
            print('Enter title and author of the Book you want to view check out history of:')
            title = input('Title: ')
            author = input('Author: ')
            book_id = self.get_exact_book(title, author)

            records = self.lib_svc.get_checkout_history(book_id)

            print(f"{records}")
        except Exception as e:
            print(f'An unexpected error has occurred in check_in_book: {e}')

    def get_average_price(self):
        try:
            books = self.book_svc.get_all_books()
            avg_price = self.book_analytics_svc.average_price(books)
            print(f"Average price: {avg_price}")
        except Exception as e:
            print(f'An unexpected error has occurred in get_average_price: {e}')

    def get_top_books(self):
        try:
            books = self.book_svc.get_all_books()
            top_rated = self.book_analytics_svc.top_rated(books)
            print(f"Top rated books: {top_rated}")
        except Exception as e:
            print(f'An unexpected error has occurred in get_top_books: {e}')

    def get_value_scores(self):
        try:
            books = self.book_svc.get_all_books()
            value_scores = self.book_analytics_svc.value_scores(books)
            print(f"Value scores: {value_scores}")
        except Exception as e:
            print(f'An unexpected error has occurred in get_value_scores: {e}')


    def get_median_price_by_genre(self):
        try:
            books = self.book_svc.get_all_books()
            medians = self.book_analytics_svc.median_price_by_genre(books)
            print(f"Median prices by genre: {medians}")
        except Exception as e:
            print(f'An unexpected error has occurred in get_median_price_by_genre: {e}')

    def get_price_std_dev(self):
        try:
            books = self.book_svc.get_all_books()
            std_dev = self.book_analytics_svc.price_std_dev(books)
            print(f"Price standard deviation: {std_dev}")
        except Exception as e:
            print(f'An unexpected error has occurred in get_price_std_dev: {e}')

    def get_price_percentiles(self):
        try:
            print("what percentiles? (enter as 1 row with a space between each):")
            percentiles = [int(p) for p in input("").split(" ")]
            books = self.book_svc.get_all_books()
            percentiles = self.book_analytics_svc.price_percentiles(books, percentiles)
            print(f"Price percentiles: {percentiles}")
        except Exception as e:
            print(f'An unexpected error has occurred in get_price_percentiles: {e}')

    def get_price_correlation(self):
        try:
            books = self.book_svc.get_all_books()
            corr = self.book_analytics_svc.rating_price_correlation(books)
            print(f"Price correlation: {corr}")
        except Exception as e:
            print(f'An unexpected error has occurred in get_price_percentiles: {e}')

    def get_rating_histogram(self):
        try:
            bins = int(input("How many bins? "))
            books = self.book_svc.get_all_books()
            rating_hist = self.book_analytics_svc.rating_histogram(books, bins)
            print(f"Rating histograms: {rating_hist}")
        except Exception as e:
            print(f'An unexpected error has occurred in get_rating_histogram: {e}')

    def get_most_popular_genre_2026(self):
        try:
            books = self.book_svc.get_all_books()
            genre = self.book_analytics_svc.most_popular_genre_2026(books)
            print(f"Most popular genre 2026: {genre}")
        except Exception as e:
            print(f'An unexpected error has occurred in get_most_popular_genre_2026: {e}')

    def plot_most_common_genres(self):
        try:
            books = self.book_svc.get_all_books()
            self.book_analytics_svc.plot_most_common_genres(books)
        except Exception as e:
            print(f'An unexpected error has occurred in plot_most_common_genres: {e}')

    def plot_highest_rated_genres(self):
        try:
            books = self.book_svc.get_all_books()
            self.book_analytics_svc.plot_highest_rated_genres(books)
        except Exception as e:
            print(f'An unexpected error has occurred in plot_highest_rated_genres: {e}')

    def plot_price_vs_rating(self):
        try:
            books = self.book_svc.get_all_books()
            self.book_analytics_svc.plot_price_vs_rating(books)
        except Exception as e:
            print(f'An unexpected error has occurred in plot_price_vs_rating: {e}')

    def plot_books_by_year(self):
        try:
            books = self.book_svc.get_all_books()
            self.book_analytics_svc.plot_books_by_year(books)
        except Exception as e:
            print(f'An unexpected error has occurred in plot_books_by_year: {e}')

    def plot_checked_out_vs_available(self):
        try:
            books = self.book_svc.get_all_books()
            self.book_analytics_svc.plot_checked_out_vs_available(books)
        except Exception as e:
            print(f'An unexpected error has occurred in plot_checked_out_vs_available: {e}')

if __name__ == '__main__':
    # generate_books()
    book_repo = BookRepository('books.json')
    book_service = BookService(book_repo)
    book_analytics_service = BookAnalyticsService()
    checkout_repo = CheckoutRepository()
    library_service = CheckoutService(book_repo, checkout_repo)
    repl = BookREPL(book_service, library_service, book_analytics_service)
    repl.start()
