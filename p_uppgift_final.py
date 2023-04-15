# Namn: Emil H
# Datum 31/03/23
# P-uppgift 193
# Titel: Memory

import os
import csv
from time import time
import random
import tkinter as tk
from operator import itemgetter

attempt = 0
current_guesses = 0
current_word = []
board_size = 2

# NOT USED YET WILL BE IMPLEMENTED ONCE THE GAME WORKSSSSSSSS
def info_menu():
    # A function to later start the game, doesnt work as of now.
    def start_game():
        global board_size, player_name, game_list, grid
        try:
            board_size = int(input_size_entry.get())
            player_name = str(name_input_entry.get())
            if board_size % 2 == 0:

                game_list = create_game_list("memo.txt", (board_size * board_size) // 2)
                grid = Board(board_size)
                add_words()

                info_menu.destroy()
                global start_time
                start_time = time()
                main_game()
        except ValueError:
            print("Invalid input.")

    info_menu = tk.Tk()
    info_menu.title("START MENU!")

    # beginning text
    start_text = tk.Label(info_menu, text="Write size A, it will be of the size AxA, only even numbers and an A < 10 is not recommended")
    start_text.grid(row=0, column=0)

    second_text = tk.Label(info_menu, text="player sick usrname :sunglass:")
    second_text.grid(row=2, column=0)

    # will be the input where the grid size comes from. AxA grid.
    input_size = tk.StringVar()
    input_size_entry = tk.Entry(info_menu, textvariable=input_size)
    input_size_entry.grid(row=1, column=0)

    # The name of the player.
    name_input = tk.StringVar()
    name_input_entry = tk.Entry(info_menu, textvariable=name_input)
    name_input_entry.grid(row=3, column=0)

    # Button to start the game.
    start_game_button = tk.Button(info_menu, text="GO!!!!!!!!", command=start_game)
    start_game_button.grid(row=4, column=0)
    info_menu.mainloop()


def create_game_list(file_name, sample_size):
    """Create a shuffled game list from file.

    Args:
        file_name (str): File name
        sample_size (int): Number of unique words to sample.

    Returns:
        list: A shuffled game list containing pairs of sample words.
    """
    with open(file_name, "r", encoding='utf-8') as f:
        full_list = [line.strip() for line in f.readlines()]
        small_list = random.sample(full_list, sample_size)

        game_list = []

        for item in small_list:
            game_list.append(item)
            game_list.append(item)

        random.shuffle(game_list)
        return game_list


game_list = create_game_list("memo.txt", (board_size*board_size)//2)


def save_to_file(file_name, username, score):
    """Used to save the score of the user. Gonna have to expant
    this to check for the positions and then be able to showcase the file to the player.

    Args:
        file_name (str): the file name
        score (int): the players score, highers = bad
    """
    with open(file_name, 'a') as f:
        f.write(username + score + "\n")


class Board:
    def __init__(self, board_size):
        """ Initialize an empty board """
        self.grid = {}
        self.board_size = board_size
        rows = [chr(i+65) for i in range(board_size)]
        cols = [i + 1 for i in range(board_size)]

        # self explaintory, fix somehow to be modular later, using ?
        for row in rows:
            for col in cols:
                self.grid[row + str(col)] = None

        self.matched_cards = []

    def set_value(self, row, col, value):
        """Set the value at the specified row and col on the grid.

        Args:
            row (str): The row letter (A-F) of the card on the grid
            col (int): The column number (1-6) of the card on the grid.
            value (str): The word to store at the specified location.
        """
        self.grid[row + str(col)] = value

    def get_value(self, row, col):
        """Get the value at the specified row and col on the grid.

        Args:
            row (str): The row letter (A-F) of the card on the grid.
            col (int): The column number (1-6) of the card on the grid.

        Returns:
            str: The word stored at the specified location.
        """
        return self.grid[row + str(col)]

    def get_all_values(self):
        """Get all values stored in the grid.

        Returns:
            dict_values: A collection of all values in the grid.
        """
        return self.grid.values()

    def hide_value(self, row, col):
        """Hide the value at the specified row and col on the grid.

        Args:
            row (str): The row letter (A-F) of the card on the grid.
            col (int): The column number (1-6) of the card on the grid.
        """
        self.grid[row + str(col)] = None

    def add_matched_cards(self, row, col):
        """Add the specified row and col to the list of matched cards.

        Args:
            row (str): The row letter (A-F) of the matched card on the grid.
            col (int): The column number (1-6) of the matched card on the grid.
        """
        self.matched_cards.append(row + str(col))

    def is_matched_card(self, row, col):
        """Check if the specified row and col represent a matched card.

        Args:
            row (str): The row letter (A-F) of the card on the grid.
            col (int): The column number (1-6) of the card on the grid.

        Returns:
            bool: True if the card is matched, False otherwise.
        """
        return row + str(col) in self.matched_cards


# create a new grid object
grid = Board(board_size)


def add_words():
    """Goes through row and such and adds one word from the game list.
    """
    i = 0

    # This adds words from the game_list with words from game_list
    for row in grid.grid.keys():
        grid.set_value(row[0], int(row[1]), game_list[i])
        if i < (grid.board_size * grid.board_size) -1:
            i += 1
            continue
        else:
            break


add_words()


def reveal_word(row, col):
    """Reveal the word at the specified row and col on the grid.
    
    Args:
        row (int): The row number (1-6) of the card on the grid
        col (int): The column number (1-6) of the card on the grid.
    """

    global root, buttons, value, current_guesses, current_word
    # Get the corresponding button
    button = buttons[(row - 1) * board_size + (col - 1)]

    try:
        # Get the value of the corresponding card on the board
        global value, current_guesses

        # the row + 64 exists to convert the row number to ASCII value, A is 65,
        # chr() function convert ASCII value to the character itself.
        # https://www.toppr.com/guides/python-guide/examples/python-examples/python-program-find-ascii-value-character/

        value = grid.get_value(chr(row + 64), col)
        print("Vword revealed : {}".format(value))

        # Set the text of the button to the revealed word
        button.config(text=value)

        # Disable the button so it cannot be clicked again
        button.config(state=tk.DISABLED)
        button.config(bg='white', fg='black')
        current_guesses += 1
        current_word.append([row, col])

        # Check for matches after every two guesses
        if current_guesses == 2:
            root.after(100, check_match)
            current_guesses = 0

    except Exception as e:
        print("Error: {}".format(str(e)))


def hide_word(row, col):
    """Hide the word at the specified row and col on the grid.

    Args:
        row (int): The row number (1-6) of the card on the grid.
        col (int): The column number (1-6) of the card on the grid.
    """
    global buttons, grid

    # (row - 1) * 6: starting number of the row, will have to replace 6 with A to make modular
    # (col - 1): Offset within the row, the column.

    button = buttons[(row - 1) * board_size + (col - 1)]
    print("hide_word function we chilling")
    if not grid.is_matched_card(chr(row + 64), col):
        button.config(text="")
        button.config(state=tk.NORMAL)
    else:
        grid.matched_cards.remove(chr(row + 64) + str(col))


def check_match():
    """Check if the currently revealed cards are a match.

    Returns:
        bool: True if there is a match, False otherwise.
    """
    global current_word, current_guesses

    # Once the list of the current displayed words are equal to two,
    # they get stored properly and then the words is aquired from the grid.
    if current_word and len(current_word) == 2:
        row1, col1 = current_word[0]
        row2, col2 = current_word[1]
        print("checking the match..... pog")
        value1 = grid.get_value(chr(row1 + 64), col1)
        value2 = grid.get_value(chr(row2 + 64), col2)

        # If word one matches word two the grid att the matched cards.
        if value1 == value2:
            print("match")
            grid.add_matched_cards(chr(row1 + 64), col1)
            grid.add_matched_cards(chr(row2 + 64), col2)
        else:
            # The opposite of the aformentioned, but here's theres a delay to
            # allow the user to see the words before they hide.
            print("Not Match")
            root.after(1000, hide_word, row1, col1)
            root.after(1000, hide_word, row2, col2)

    # Reset the current_guesses counter and clear current_word
    current_guesses = 0
    current_word.clear()

    if len(grid.matched_cards) == (grid.board_size//2):
        root.quit()

    save_to_file("high_scores.txt", player_name, attempt)
    display_highscores()


def create_labels():
    """Create labels for rows and columns. Idk why bg='black'
     makes like only the small part black but im to tired to care."""
    
    global my_frame, grid

    print("creating the labels")
    for i in range(grid.board_size):
        row_label = tk.Label(
            my_frame, text=chr(i + 65), font=("Helvetica", 20),
            height=1, width=2, bg='black', fg='white'
        )
        row_label.grid(
            row=i + 1, column=0, padx=(50, 0), pady=(0, 10), sticky=tk.W
        )

        col_label = tk.Label(
            my_frame, text=str(i + 1), font=("Helvetica", 20),
            height=1, width=2, bg='black', fg='white'
        )
        col_label.grid(
            row=0, column=i + 1, padx=(0, 10), pady=(50, 0), sticky=tk.N
        )


def is_already_revealed(row, col):
    """Check if the specified row and col represent a revealed or matched card.

    Args:
        row (str): The row letter (A-F) of the card on the grid.
        col (int): The column number (1-6) of the card on the grid.

    Returns:
        bool: True if the card is revealed or matched, False otherwise.
    """
    global buttons, grid
    button = buttons[(row - 1) * board_size + (col - 1)]
    if button["state"] == tk.DISABLED or grid.is_matched_card(chr(row + 64), col):
        return True
    return False


# make this also a function later zzzzzz
# Tkinter GUI

def main_game():

    global root, my_frame, buttons, entry
    root = tk.Tk()

    root.title("Memory Spel!")
    root.config(bg='black')

    my_frame = tk.Frame(root)
    my_frame.pack(pady=10)

    create_labels()


    # make this all a function later
    def create_buttons():
        global buttons
        buttons = []
        print("creating buttons")

        # need to make modular with everything else later.
        for i in range(grid.board_size):
            for j in range(grid.board_size):
                button = tk.Button(my_frame, text='', font=("Helvetica", 20), height=3, width=6, fg='white')
                button.grid(row=i + 1, column=j + 1)
                buttons.append(button)
        return buttons


    create_buttons()

    # create a label widget to describe the input box
    label = tk.Label(root, text="Enter your input coordinate (A1-F6) >")
    label.pack(side=tk.BOTTOM, pady=12)

    # create an Entry widget to input the data
    entry = tk.Entry(root, width=20, font=("Helvetica", 20))
    entry.pack(side=tk.BOTTOM)

    # why are these here, im scared to move them
    row = ""
    col = ""
    input_value = ""

    # Button to save the input.
    button = tk.Button(root, text="Submit coordinate", command=store_input)
    button.pack(side=tk.BOTTOM)

    # Start the Tkinter event loop
    root.mainloop()


def store_input():
    """
    A function to get the user input and process it or something.
    In: Nothing
    Out: Nothing
    """
    global entry, current_guesses, current_word
    input_value = entry.get()
    # attempt += 1
    try:
        if len(input_value) == 2:
            row = ord(input_value[0].upper()) - 64
            col = int(input_value[1])
            if not is_already_revealed(row, col):
                reveal_word(row, col)
                print("Word revealed.")
            else:
                print("coordinte already revealed")
            
    except Exception as e:
        print("error :(".format(str(e)))
    finally:
        clear_text_input()


def clear_text_input():
    """Clear the text input in the Entry widget."""
    entry.delete(0, tk.END)

def save_score(grid_size, name, attempts, time_taken):
    #Insperation från David Kniberg P-uppgift.

    score_list = [grid_size, name, attempts, time_taken]

    with open('scores.csv', 'a', newline='') as csvfile:
        score_writer = csv.writer(csvfile)
        score_writer.writerow(score_list)
    
def sort_variables(score):
    """_summary_

    Args:
        score (_type_): _description_

    Returns:
        _type_: _description_
    """
    grid_size = int(score[0])
    attempts = int(score[2])
    return (grid_size, attempts)


def save_to_file(file_name, username, score):
    """_summary_

    Args:
        file_name (_type_): _description_
        username (_type_): _description_
        score (_type_): _description_
    """
    with open(file_name, "a") as f:
        f.write(username + "," + str(score) + "\n")

    with open(file_name, "r") as f:
        scores = [line.strip().split(",") for line in f.readlines()]
        scores = [[name, int(score)] for name, score in scores]
        return scores
    
# Function to display the scores from the file
def display_highscores(scores):
    """_summary_
    """
    
    global root, end_frame, buttons, entry
    root = tk.Tk()

    root.title("Game Ended!")
    root.config(bg='black')

    end_frame = tk.Frame(root)
    end_frame.pack(pady=10)

    label = tk.Label(end_frame, text="High Scores", font=("Helvetica", 20))
    label.pack(pady=10)

    text_box = tk.Text(end_frame, font=("Helvetica", 14), width=40, height=20)
    text_box.pack(pady=10)

    if not os.path.exists('scores.csv'):
        print('No scores found.')
        return
    
    sorted_scores = sorted(scores, key=itemgetter(1))

    # Display the scores in the text box
    for name, score in sorted_scores:
        text_box.insert(tk.END, f"{name} - {score}\n")

    end_frame.mainloop()

    # Sort scores by grid size and then by attempts using the sort_key function
    sorted_scores = sorted(scores, key=sort_variables)

    # Print the sorted scores
    text = tk.Text(root, text=sorted_scores, height=12, width=12)



if __name__ == '__main__':
    info_menu()


