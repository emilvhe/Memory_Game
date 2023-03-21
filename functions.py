import random

"""
Functions
"""

#Read and prepares the word list for the game.
def import_game_list(filename):
    full_list = []
    with open(filename, "r") as f:
        for line in f.readlines():
            clean = line.strip()
            full_list.append(clean)
    f.close
    small_list = random.sample(full_list,18)
    game_list = []	
    for item in small_list:
        game_list.append(item)
        game_list.append(item)
    random.shuffle(game_list)
    return(game_list)

#function to write and save 
def save_score_to_file(filename, username, score):
    with open (filename, "a") as file:
        file.write(username + ": " + str(score) + "\n")
        file.close()


#Function to place the words on the grid.
def set_word(grid, list):
    i = 0
    for row in grid.grid.keys():
        grid.set_value(row[0],int(row[1]), list[i])
        if i < 36:
            i += 1
            continue
        else:
            break

def reveal_word(row, col)
    