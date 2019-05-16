import sys
from random import randint
from time import sleep

def printTurn(p, x, y):
    print("Player ", '1 '*(p == -1), '2 '*(p == 1), "turn: ", x, " ", y, sep='')


# check if there is no space left on the board
def ifDraw(board):
    for line in board:
        if '.' in line:
            return False
    return True


def isInRange(x, y, board):
    if 0 <= x < len(board) and 0 <= y < len(board[0]):
        return True
    return False


# by the next construction we can check if there is near at least one X or O
# and we go through only board's range cells
def isLegal(x, y, board):
    if board[y][x] == '.':
        for i in range(x-1, x+2):
            if i >= 0 and i < len(board[0]):
                for k in range(y-1, y+2):
                    if k >= 0 and k < len(board):
                        if board[k][i] != ".":
                            return True
    return False


def computer_move(board, number, first_move=False):
    while 1 != 0:
        x = randint(0, len(board[0])-1)
        y = randint(0, len(board)-1)
        # there is no need to check if it is legal when it is the first turn
        if not first_move:
            if isLegal(x, y, board):
                break
        else: break
    return (x, y)


def player_move(board, number, first_move=False):
    while 1 != 0:
        x, y = map(int, input("Write X and Y coordinates... ").split())
        if isInRange(x, y, board):
            if first_move == False:
                if isLegal(x, y, board):
                    break
            else: break
        print("Enter the legal values!")
    return (x, y)


# defines if 'X(space)X' or 'O(space)O' in the vertical line
def checkVertical(board):
    for y in range(len(board)-2):
        for x in range(len(board[0])):
            sign = board[y][x]
            # if once one element is X or O and element below is space (.)
            # then we look for relevant X or O below
            if sign in ['x', 'o'] and board[y+1][x] == '.':
                for i in range(y+2, len(board)):
                    if board[i][x] == sign:
                        return sign
                    # if it is an opposite sign then stop
                    if board[i][x] != '.':
                        return False
    return False


# defines if 'X(space)X' or 'O(space)O' in the horizontal line
def checkHorizontal(board):
    for line in board:
        # defines if combination X . or O . is in line
        s = ''.join(line)
        if 'x.' in ''.join(s[:-1]):
            sign = 'x'
            ind = s.index('x.')
        elif 'o.' in ''.join(s[:-1]):
            sign = 'o'
            ind = s.index('o.')
        else:
            continue
        # tries to find the second sign, what would mean that it is
        # a winning line
        for i in range(ind+2, len(line)):
            if line[i] == sign:
                return sign
            if line[i] != '.':
                return False
    return False


# via players[] dictionary returns winner's number or returns 0
def who_won(board):
    players = {'x': 1, 'o': 2}
    ch = checkHorizontal(board)
    cv = checkVertical(board)
    if ch:
        return players[ch]
    if cv:
        return players[cv]
    return 0


# function for printing actual board's state
def printBoard(w, h, b):
    print(" "*3, end='')
    for i in range(w):
        print(i, end=' ')
    print()
    print(" "*2, "_ "*w)
    for i in range(h):
        print(i, "| ", sep='', end='')
        for x in b[i]:
            print(x, end=" ")
        print()
    print()


def game(width, height, player1, player2):
    # initializing game board
    board = [['.' for x in range(width)] for y in range(height)]
    printBoard(width, height, board)

    # initializing players and their human/computer move option
    # -1 for the 1st player, 1 for the 2nd
    moveType = {"h": player_move, "c": computer_move}
    move = {-1: moveType[player1], 1: moveType[player2]}

    # FIRST TURN
    p = -1
    x, y = move[p](board, p, True)

    # insert turn on the board
    board[y][x] = 'x' if p == -1 else 'o'
    printTurn(p, x, y)
    printBoard(width, height, board)

    # NEXT TURNS
    while who_won(board) == 0 and not ifDraw(board):
        sleep(1)
        p *= -1
        x, y = move[p](board, p)
        board[y][x] = 'x'*(p == -1) + 'o'*(p == 1)
        printTurn(p, x, y)
        printBoard(width, height, board)

    if ifDraw(board):
        print ("Draw")
    else:
        print("Player ", "2 won!"*(p == 1), \
              "1 won!"*(p == -1), sep='')


def argsValid():
    if len(sys.argv) != 5:
        return False
    if not (sys.argv[1].isdigit() and sys.argv[2].isdigit()):
        return False
    if int(sys.argv[1]) < 3 or int(sys.argv[2]) < 3:
        return False
    if not (sys.argv[3] in ["h", "c"] and sys.argv[4] in ["h", "c"]):
        return False
    return True


def main():
    if not argsValid():
        sys.exit("Invalid arguments!")

    game(int(sys.argv[1]), int(sys.argv[2]), sys.argv[3], sys.argv[4])


main()