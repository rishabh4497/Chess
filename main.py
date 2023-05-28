import tkinter as tk
from tkinter import messagebox
from PIL import ImageTk, Image
import os

# Chess Game

# Initialize the chessboard
board = [
    ['r', 'n', 'b', 'q', 'k', 'b', 'n', 'r'],
    ['p', 'p', 'p', 'p', 'p', 'p', 'p', 'p'],
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
    ['P', 'P', 'P', 'P', 'P', 'P', 'P', 'P'],
    ['R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R']
]

# Piece images
piece_images = {
    'r': 'rook.png',
    'n': 'knight.png',
    'b': 'bishop.png',
    'q': 'queen.png',
    'k': 'king.png',
    'p': 'pawn.png',
    'R': 'rookB.png',
    'N': 'knightB.png',
    'B': 'bishopB.png',
    'Q': 'queenB.png',
    'K': 'kingB.png',
    'P': 'pawnB.png',
}

# Create the GUI window
window = tk.Tk()
window.title("Chess Game")

# Function to update the GUI board
def update_board():
    for i in range(8):
        for j in range(8):
            piece = board[i][j]
            if piece == ' ':
                buttons[i][j].config(image='', bg='white')
            else:
                image_path = os.path.join('images', piece_images.get(piece, ''))
                if os.path.exists(image_path):
                    try:
                        image = Image.open(image_path)
                        resized_image = image.resize((60, 60))
                        photo = ImageTk.PhotoImage(resized_image)
                        buttons[i][j].config(image=photo, width=60, height=60, bg='light gray' if (i+j) % 2 == 0 else 'gray')
                        buttons[i][j].image = photo
                    except (FileNotFoundError, PIL.UnidentifiedImageError) as e:
                        messagebox.showerror("Image Error", f"Failed to load image: {image_path}\n{str(e)}")
                else:
                    messagebox.showerror("Image Error", f"Image not found: {image_path}")

# Function to handle button click events
def on_click(row, col):
    global start_pos
    if not start_pos:
        piece = board[row][col]
        if piece.islower():
            messagebox.showwarning("Invalid Move", "It's not your turn.")
            return
        if piece == ' ':
            return
        start_pos = [row, col]
        buttons[row][col].config(bg='yellow')
    else:
        start_row, start_col = start_pos
        make_move((start_row, start_col), (row, col))
        start_pos = []

# Function to check if a move is valid
def is_valid_move(start, end):
    start_row, start_col = start
    end_row, end_col = end
    piece = board[start_row][start_col]
    target = board[end_row][end_col]

    # Check if the start and end positions are different
    if start == end:
        return False

    # Check if the start position is not empty
    if piece == ' ':
        return False

    # Check if the end position is not occupied by the player's own piece
    if piece.islower() == target.islower():
        return False

    # Check if the move is valid based on the piece type
    if piece.lower() == 'p':
        # Pawn moves
        direction = -1 if piece.isupper() else 1
        if start_col == end_col and start_row + direction == end_row and target == ' ':
            return True
        if abs(start_col - end_col) == 1 and start_row + direction == end_row and target.islower() != piece.islower():
            return True
    elif piece.lower() == 'r':
        # Rook moves
        if start_row == end_row or start_col == end_col:
            if start_row == end_row:
                row_range = range(min(start_col, end_col) + 1, max(start_col, end_col))
                if all(board[start_row][col] == ' ' for col in row_range):
                    return True
            elif start_col == end_col:
                col_range = range(min(start_row, end_row) + 1, max(start_row, end_row))
                if all(board[row][start_col] == ' ' for row in col_range):
                    return True
    elif piece.lower() == 'n':
        # Knight moves
        if (abs(start_row - end_row) == 2 and abs(start_col - end_col) == 1) or (abs(start_row - end_row) == 1 and abs(start_col - end_col) == 2):
            return True
    elif piece.lower() == 'b':
        # Bishop moves
        if abs(start_row - end_row) == abs(start_col - end_col):
            row_range = range(min(start_row, end_row) + 1, max(start_row, end_row))
            col_range = range(min(start_col, end_col) + 1, max(start_col, end_col))
            if all(board[row][col] == ' ' for row, col in zip(row_range, col_range)):
                return True
    elif piece.lower() == 'q':
        # Queen moves
        if start_row == end_row or start_col == end_col or abs(start_row - end_row) == abs(start_col - end_col):
            if start_row == end_row:
                row_range = range(min(start_col, end_col) + 1, max(start_col, end_col))
                if all(board[start_row][col] == ' ' for col in row_range):
                    return True
            elif start_col == end_col:
                col_range = range(min(start_row, end_row) + 1, max(start_row, end_row))
                if all(board[row][start_col] == ' ' for row in col_range):
                    return True
            elif abs(start_row - end_row) == abs(start_col - end_col):
                row_range = range(min(start_row, end_row) + 1, max(start_row, end_row))
                col_range = range(min(start_col, end_col) + 1, max(start_col, end_col))
                if all(board[row][col] == ' ' for row, col in zip(row_range, col_range)):
                    return True
    elif piece.lower() == 'k':
        # King moves
        if abs(start_row - end_row) <= 1 and abs(start_col - end_col) <= 1:
            return True

    return False

# Function to make a move
def make_move(start, end):
    if is_valid_move(start, end):
        board[end[0]][end[1]] = board[start[0]][start[1]]
        board[start[0]][start[1]] = ' '
        update_board()
    else:
        messagebox.showwarning("Invalid Move", "The selected move is invalid.")

# Create the chessboard buttons
buttons = []
for i in range(8):
    row_buttons = []
    for j in range(8):
        button = tk.Button(window, width=60, height=60, command=lambda row=i, col=j: on_click(row, col))
        button.grid(row=i, column=j)
        row_buttons.append(button)
    buttons.append(row_buttons)

# Initialize the start position list
start_pos = []

# Update the initial board state
update_board()

# Run the GUI main loop
window.mainloop()
