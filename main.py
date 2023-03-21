#Emil Hedeby
#P-





from functions import *

#The game board
class Board:

    def __init__(self, A):
        self.grid = {}
        #alphabet = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
        #numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 0]
        rows = ['A','B','C','D','E','F']
        cols = [1, 2, 3, 4, 5, 6]

        #for alphabet in range(A):
            #rows.append(alphabet)
        
        #for numbers in range(A):
            #cols.append(numbers)


        for row in rows:
            for col in cols:
                self.grid[row+str(col)] = None

    def set_word(self, row, col, word):
        self.grid[row+str(col)] = word

    def get_word(self, row, col):
        return self.grid[row+str(col)]
    
    def get_all_words(self):
        return self.grid_words()
    
grid = Board(6)


def main():
    #Running the functions from functions.py
    game_list = import_game_list("Memo.txt")

    save_score_to_file("highscore.txt", "Emil", 13)
    start_window()

if __name__ == '__main__':
    main()