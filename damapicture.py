import tkinter as tk
from tkinter import messagebox
import random

# Şahmat daşını təmsil edən sinif
class Piece:
    def __init__(self, color, king=False):
        self.color = color
        self.king = king

    def make_king(self):
        self.king = True

    def __repr__(self):
        return f"{self.color.upper() if self.king else self.color}"

# Oyunun lövhəsini təmsil edən sinif
class Board:
    def __init__(self):
        self.board = self.create_board()

    def create_board(self):
        board = [[None for _ in range(8)] for _ in range(8)]
        for row in range(8):
            for col in range(8):
                if (row % 2 != col % 2):
                    if row < 3:
                        board[row][col] = Piece("b")  # Qara daşlar
                    elif row > 4:
                        board[row][col] = Piece("r")  # Qırmızı daşlar
        return board

    def print_board(self):
        for row in self.board:
            print(" ".join([str(piece) if piece else "." for piece in row]))

    def move_piece(self, start, end):
        piece = self.board[start[0]][start[1]]
        self.board[end[0]][end[1]] = piece
        self.board[start[0]][start[1]] = None

        if end[0] == 0 and piece.color == 'r':
            piece.make_king()
        elif end[0] == 7 and piece.color == 'b':
            piece.make_king()

    def get_valid_moves(self, pos):
        row, col = pos
        piece = self.board[row][col]
        if not piece:
            return []

        directions = []
        if piece.king:
            directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
        else:
            directions = [(-1, -1), (-1, 1)] if piece.color == "r" else [(1, -1), (1, 1)]

        valid_moves = []
        for dr, dc in directions:
            r, c = row + dr, col + dc
            while 0 <= r < 8 and 0 <= c < 8:
                if self.board[r][c] is None:
                    valid_moves.append((r, c))
                elif self.board[r][c].color != piece.color:
                    rr, cc = r + dr, c + dc
                    if 0 <= rr < 8 and 0 <= cc < 8 and self.board[rr][cc] is None:
                        valid_moves.append((rr, cc))
                    break
                else:
                    break
                r += dr
                c += dc

        return valid_moves

    def remove_piece(self, pos):
        r, c = pos
        self.board[r][c] = None

# Oyun idarəetmə sinifi
class DamaGame:
    def __init__(self, root):
        self.board = Board()
        self.turn = "r"  # Qırmızı oyunçu başlayır
        self.root = root
        self.canvas = tk.Canvas(root, width=400, height=400)
        self.canvas.pack()
        self.canvas.bind("<Button-1>", self.on_click)
        self.selected_piece = None
        self.valid_moves = []
        self.draw_board()

    def draw_board(self):
        for row in range(8):
            for col in range(8):
                x1 = col * 50
                y1 = row * 50
                x2 = x1 + 50
                y2 = y1 + 50
                color = "white" if (row + col) % 2 == 0 else "gray"
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color)

                piece = self.board.board[row][col]
                if piece:
                    self.canvas.create_text((x1 + x2) // 2, (y1 + y2) // 2, text=str(piece), font=("Arial", 20))

    def on_click(self, event):
        col = event.x // 50
        row = event.y // 50
        if self.selected_piece:
            end = (row, col)
            if end in self.valid_moves:
                start = self.selected_piece
                if abs(start[0] - end[0]) == 2:
                    middle = ((start[0] + end[0]) // 2, (start[1] + end[1]) // 2)
                    self.board.remove_piece(middle)
                self.board.move_piece(start, end)
                self.turn = "b" if self.turn == "r" else "r"
                self.selected_piece = None
                self.valid_moves = []
                self.draw_board()
                winner = self.is_winner()
                if winner:
                    messagebox.showinfo("Qalib!", winner)

            else:
                self.selected_piece = None
                self.valid_moves = []
        else:
            start = (row, col)
            piece = self.board.board[row][col]
            if piece and piece.color == self.turn:
                self.selected_piece = start
                self.valid_moves = self.board.get_valid_moves(start)
        
        # AI hərəkətini idarə et
        if self.turn == "b":
            self.ai_move()

    def ai_move(self):
        # AI üçün bütün mümkün hərəkətləri tapır
        ai_moves = []
        for row in range(8):
            for col in range(8):
                piece = self.board.board[row][col]
                if piece and piece.color == "b":
                    valid_moves = self.board.get_valid_moves((row, col))
                    for move in valid_moves:
                        ai_moves.append(((row, col), move))

        if ai_moves:
            # Tamamilə təsadüfi bir hərəkət seçir
            start, end = random.choice(ai_moves)
            if abs(start[0] - end[0]) == 2:
                middle = ((start[0] + end[0]) // 2, (start[1] + end[1]) // 2)
                self.board.remove_piece(middle)  # Düşmən daşını sil
            self.board.move_piece(start, end)  # Daşı yerini dəyiş
            self.turn = "r"  # Növbəni dəyiş
            self.draw_board()
            winner = self.is_winner()
            if winner:
                messagebox.showinfo("Qalib!", winner)

    def is_winner(self):
        reds = blacks = 0
        for row in self.board.board:
            for piece in row:
                if piece:
                    if piece.color == "r":
                        reds += 1
                    elif piece.color == "b":
                        blacks += 1
        if reds == 0:
            return "Qara oyunçu qalib gəldi!"
        elif blacks == 0:
            return "Qırmızı oyunçu qalib gəldi!"
        return None

# Tkinter pəncərəsini yaratmaq
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Dama Oyunu")
    game = DamaGame(root)
    root.mainloop()
