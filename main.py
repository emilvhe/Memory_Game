from time import time
import random
from functions import *
import tkinter as tk

attempt = 0
current_guesses = 0
current_word = []

with open("memoUTF8.txt", "r", encoding='utf-8') as f:
    full_list = []
    for line in f.readlines():
        clean = line.strip()
        full_list.append(clean)

    small_list = random.sample(full_list, 18)

    game_list = []

    for item in small_list:
        game_list.append(item)
        game_list.append(item)

    random.shuffle(game_list)


class Board:
    def __init__(self):
        self.grid = {}
        rows = ['A', 'B', 'C', 'D', 'E', 'F']
        cols = [1, 2, 3, 4, 5, 6]
        for row in rows:
            for col in cols:
                self.grid[row + str(col)] = None
    
        self.matched_cards = []

    def set_value(self, row, col, value):
        self.grid[row + str(col)] = value

    def get_value(self, row, col):
        check_match()
        return self.grid[row + str(col)]

    def get_all_values(self):
        return self.grid.values()
    
    def hide_value(self, row, col):
        self.grid[row + str(col)] = None

    def add_matched_cards(self, row, col):
        self.matched_cards.append(row + str(col))
    
    def is_matched_card(self, row, col):
        return row + str(col) in self.matched_cards
# create a new grid object
grid = Board()

i = 0
for row in grid.grid.keys():
    grid.set_value(row[0], int(row[1]), game_list[i])
    if i < 36:
        i += 1
        continue
    else:
        break


def reveal_word(row, col):
    # Get the corresponding button
    button = buttons[(row-1)*6 + (col-1)]
    
    try:
        # Get the value of the corresponding card on the board
        global value
        value = grid.get_value(chr(row + 64), col)
        print("Value retrieved: {}".format(value))

        # Set the text of the button to the revealed word
        button.config(text=value)

        # Disable the button so it cannot be clicked again
        button.config(state=tk.DISABLED)
    
        #kollar för matches
        root.after(100, check_match)
    except Exception as e:
        print("Error: {}".format(str(e)))


def hide_word(row, col):
    button = buttons[(row-1)*6 + (col-1)]
    print("hide_word function")
    if not grid.is_matched_card(chr(row + 64), col):
        button.config(text ="")
        button.config(state=tk.NORMAL)
    else:
        grid.matched_cards.remove(chr(row + 64) + str(col))


def check_match():
    # Get all revealed values
    revealed_values = [button.cget('text') for button in buttons if button.cget('state') == 'disabled']

    # Check if two of the revealed values are the same
    if len(revealed_values) == 2 and revealed_values[0] == revealed_values[1]:
        print("match")
        if current_word:
            row1, col1 = current_word[0]
            row2, col2 = current_word[1]
        grid.add_matched_cards(chr(row1 + 64), col1)
        grid.add_matched_cards(chr(row2 + 64), col2)
        current_word.clear()
        return True
    elif len(revealed_values) == 2 and revealed_values[0] != revealed_values[1]:
        print("Not Match")    
        if current_word:
            hide_word(current_word[0][0], current_word[0][1])
            hide_word(current_word[1][0], current_word[1][1])
            current_word.clear()    
        return False



# Tkinter GUI
root = tk.Tk()
root.title("Emil A1-F6 IQ Spel!")
root.geometry("1080x800")

my_frame = tk.Frame(root)
my_frame.pack(pady=10)

buttons = []
for i in range(6):
    for j in range(6):
        button = tk.Button(my_frame, text='', font=("Helvetica", 20), height=3, width=6)
        button.grid(row=i, column=j)
        buttons.append(button)



# create a label widget to describe the input box
label = tk.Label(root, text="Enter your input cordinate (A1-F6) >")
label.pack(side=tk.BOTTOM,pady=12)

# create an Entry widget to input the data
entry = tk.Entry(root, width=20, font=("Helvetica", 20))
entry.pack(side=tk.BOTTOM)

# a function to store the input as a variable :3
row = ""
col = ""
input_value = ""

def store_input():
    global current_guesses, current_word
    input_value = entry.get()

    try:
        if len(input_value) == 2:
            row = ord(input_value[0].upper()) - 64
            col = int(input_value[1])
            reveal_word(row, col)
            print("Word revealed.")
            current_guesses += 1
            current_word.append([row, col])

            if current_guesses == 2:
                if check_match():
                    if len(grid.matched_cards) == len(grid.grid):
                        root.quit()
                       
                current_guesses = 0
                current_word.clear()
    except Exception as e:
        print("error :(".format(str(e)))
                #if len(current_word[0]) == [1]:
                    #grid.add_matched_cards(chr(current_word[0][0]+64), current_word[0][1])
                    #if len(grid.matched_cards) == 36:
                        #root.quit

    finally:
        clear_text_input()




def clear_text_input():
    entry.delete(0, tk.END)


# knapp för att använda store input som ska spara inputen.
button = tk.Button(root, text="Submit cordinate", command=store_input)
button.pack(side=tk.BOTTOM)


# Start the Tkinter event loop
root.mainloop()