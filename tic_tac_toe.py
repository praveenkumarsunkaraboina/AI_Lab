def is_board_full(board):
    return all(cell != " " for row in board for cell in row)

def print_board(board):
    for row in range(3):
        print("  |  ".join(board[row]))
        if row<3:
            print("--------------")

def check_winner(board, player):
    for row in range(3):
        if all([cell==player for cell in board[row]]):
            return True
    for col in range(3):
        if all([board[row][col]==player for row in range(3)]):
            return True
    if all([board[i][i]==player for i in range(3)]):
        return True
    if all([board[i][2-i]==player for i in range(3)]):
        return True
    
    return False
    

def tic_tac_toe():
    board=[[" " for _ in range(3)] for _ in range(3)]
    current_player="X"

    while True:
        print_board(board)
        print(f"Player {current_player}'s turn.")
        while True:
            try:
                move=input(f"Enter row and column (1-3) for {current_player}: ").strip()
                row, col=map(int, move.split()) # converts each element of move in int
                if row<1 or row>3 or col<1 or col>3:
                    print("Invalid input. Row and column must be between 1 and 3.")
                elif board[row-1][col-1]!=" ":
                    print("This cell is already taken. Please choose another.")
                else:
                    board[row-1][col-1]=current_player
                    break
            except ValueError:
                print("Invalid Input. Please enter two numbers separated by a space.")
        
        if check_winner(board,current_player):
            print_board(board)
            print(f"Player {current_player}wins!")
            break
        
        if is_board_full(board):
            print_board(board)
            print("It's Draw!")
            break

        current_player="O" if current_player=="X" else "X"

if __name__ == "__main__":
    tic_tac_toe()