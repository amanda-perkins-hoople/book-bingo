# Imports
import random
import csv
import textwrap
from pathlib import Path

# Data

import csv
from pathlib import Path

def load_books():
    books = []
    file_path = Path(__file__).resolve().parent / "books.csv"

    with open(file_path, "r", encoding="utf-8-sig", newline="") as file:
        reader = csv.DictReader(file)

        for row in reader:
            title = row["title"].strip()
            if title:
                books.append(title)

    return books


books = load_books()
print(f"Loaded {len(books)} books.")

#Function Definitions
def display_books(books, called_books):
    for number, book in enumerate(books, start=1):     
        if book in called_books:
             print(f"*** {book} has been called! ***")
        else:
            print(f"{number}. {book}")

def call_book(book_to_call, books, called_books):

    for book in books:

        if book.lower() == book_to_call.lower():

            if book in called_books:
                print(f"{book} has already been called.")

            else:
                called_books.append(book)
                print(f"{book} was added to the called books.")

                if len(called_books) == len(books):
                    print("All books have now been called!")

            return

    print(f"{book_to_call} was not found.")


def count_called_books(called_books):
    return len(called_books)

def called_books_message(called_books):
    total_called = len(called_books)

    if total_called == 1:
        return f"{total_called} book has been called."
    else:
        return f"{total_called} books have been called."

def call_random_book(books, called_books):
    available_books = []

    for book in books:
        if book not in called_books:
            available_books.append(book)

    if len(available_books) == 0:
        print("All books have been called!")
        return
        

    selected_book = random.choice(available_books)
    called_books.append(selected_book)
    print(f"{selected_book} was randomly called.")

    if len(called_books) == len(books):
        print("All books have now been called!")

def create_bingo_card(books):
    selected_books = random.sample(books, 24)

    # Insert the FREE space in the center
    selected_books.insert(12, "FREE")

    card = []

    for row_number in range(5):
        start = row_number * 5
        end = start + 5

        row = selected_books[start:end]
        card.append(row)

    return card


def display_bingo_card(card, called_books):
    column_width = 24
    border = "+" + "+".join(
        ["-" * column_width] * 5
    ) + "+"

    print("\nYour Bingo Card:")
    print(border)

    for row in card:
        wrapped_row = []

        for book in row:
            if book == "FREE" or book in called_books:
                displayed_book = f"[X] {book}"
            else:
                displayed_book = f"[ ] {book}"

            # Wrap long titles to fit within the cell
            wrapped_book = textwrap.wrap(
                displayed_book,
                width=column_width - 2
            )

            wrapped_row.append(wrapped_book)

        # Find how many lines the tallest cell needs
        row_height = max(len(cell) for cell in wrapped_row)

        # Print each line of the row
        for line_number in range(row_height):
            displayed_row = []

            for cell in wrapped_row:
                if line_number < len(cell):
                    line = cell[line_number]
                else:
                    line = ""

                displayed_row.append(
                    line.center(column_width)
                )

            print("|" + "|".join(displayed_row) + "|")

        print(border)



def remaining_books_message(books, called_books):
    total_remaining = len(books) - len(called_books)

    if total_remaining == 1:
        return f"{total_remaining} book remains."
    else:
        return f"{total_remaining} books remain."

def get_game_stats(books, called_books):
    return {
        "called_books": len(called_books),
        "remaining_books": len(books) - len(called_books),
        "total_books": len(books)
    }



def check_for_bingo(card, called_books):
    # Check Horizontals
    for row in card:
        row_complete = True

        for book in row:
            if book != "FREE" and book not in called_books:
                row_complete = False

        if row_complete:
            return True

    # Check Verticals
    for column_number in range(len(card[0])):
        column_complete = True

        for row in card:
            book = row[column_number]

            if book != "FREE" and book not in called_books:
                column_complete = False

        if column_complete:
            return True

    # Check Diagonals
    diagonal_one_complete = True
    diagonal_two_complete = True

    for position in range(len(card)):
        book_one = card[position][position]

        opposite_position = len(card) - 1 - position
        book_two = card[position][opposite_position]

        if book_one != "FREE" and book_one not in called_books:
            diagonal_one_complete = False

        if book_two != "FREE" and book_two not in called_books:
            diagonal_two_complete = False

    if diagonal_one_complete or diagonal_two_complete:
        return True

    return False


def create_bingo_cards(books, number_of_cards):
    bingo_cards = {}

    for number in range(1, number_of_cards + 1):
        card_number = f"CARD-{number:03}"
        bingo_cards[card_number] = create_bingo_card(books)
    return bingo_cards
 
#Main Running Program
test_mode = True
called_books = []
available_books = []

bingo_cards = create_bingo_cards(books, 3)
bingo_card = bingo_cards["CARD-002"]
display_bingo_card(bingo_card, called_books)
bingo_announced = False

while True:
    book_to_call = input(
        "\nEnter a book title, 'random', 'reset', or 'quit': "
    ).strip()

    if book_to_call.lower() == "quit":
        print("Ending the book caller.")
        break

    elif book_to_call.lower() == "reset":
        called_books.clear()
        bingo_announced = False
        print("The called books have been reset.")

    elif book_to_call.lower() == "random":
        call_random_book(books, called_books)

    else:
        call_book(book_to_call, books, called_books)
    game_stats = get_game_stats(books, called_books)
    
    print()
    display_bingo_card(bingo_card, called_books)
    if test_mode and check_for_bingo(bingo_card, called_books) and not bingo_announced:
        print("*** BINGO! Testing confirms the win logic works. ***")
        bingo_announced = True
    print(
       f"Called Books: {game_stats['called_books']} | "
       f"Remaining: {game_stats['remaining_books']} | "
       f"Total: {game_stats['total_books']}"
    )
    