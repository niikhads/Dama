import tkinter as tk
from tkinter import messagebox

# Şahmat daşını təmsil edən sinif
class Piece:
    def __init__(self, color, king=False):
        # Daşın rəngini və "king" (şah) statusunu təyin edir
        self.color = color
        self.king = king

    def make_king(self):
        # Daşı "king" (şah) statusuna keçirir
        self.king = True

    def __repr__(self):
        # Daşı mətndə təqdim etmək üçün rengi böyük hərflə qaytarır, əgər kingdirsə
        return f"{self.color.upper() if self.king else self.color}"

# Oyunun lövhəsini təmsil edən sinif
class Board:
    def __init__(self):
        # Lövhəni yaradıb oyuna hazır vəziyyətə gətirir
        self.board = self.create_board()

    def create_board(self):
        # 8x8 lövhə yaradılır və hər iki oyunçunun daşları yerləşdirilir
        board = [[None for _ in range(8)] for _ in range(8)]
        for row in range(8):
            for col in range(8):
                # Hər ikinci hüceyrəyə daşları yerləşdirir
                if (row % 2 != col % 2):
                    if row < 3:
                        board[row][col] = Piece("b")  # Qara daşlar
                    elif row > 4:
                        board[row][col] = Piece("r")  # Qırmızı daşlar
        return board

    def print_board(self):
        # Lövhəni ekranda göstərir, boş yerləri nöqtələrlə ifadə edir
        for row in self.board:
            print(" ".join([str(piece) if piece else "." for piece in row]))

    def move_piece(self, start, end):
        # Daşı başlanğıc nöqtədən son nöqtəyə hərəkət etdirir
        piece = self.board[start[0]][start[1]]
        self.board[end[0]][end[1]] = piece
        self.board[start[0]][start[1]] = None

        # Əks tərəfə çatan daşı "king" statusuna keçirir
        if end[0] == 0 and piece.color == 'r':
            piece.make_king()
        elif end[0] == 7 and piece.color == 'b':
            piece.make_king()

    def get_valid_moves(self, pos):
        # Seçilmiş daş üçün mümkün hərəkətləri qaytarır
        row, col = pos
        piece = self.board[row][col]
        if not piece:
            return []

        directions = []

        # King daşları üçün bütün istiqamətlərdə hərəkət etməyə imkan veririk
        if piece.king:
            directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
        else:
            # Qırmızı daşlar üçün yuxarıya, qara daşlar üçün aşağıya
            directions = [(-1, -1), (-1, 1)] if piece.color == "r" else [(1, -1), (1, 1)]

        valid_moves = []

        for dr, dc in directions:
            # Vurulmuş daşları tapmaq üçün dövr
            r, c = row + dr, col + dc
            while 0 <= r < 8 and 0 <= c < 8:
                if self.board[r][c] is None:
                    valid_moves.append((r, c))  # Boş yer
                elif self.board[r][c].color != piece.color:
                    # Düşmən daşını vurmaq
                    rr, cc = r + dr, c + dc
                    if 0 <= rr < 8 and 0 <= cc < 8 and self.board[rr][cc] is None:
                        valid_moves.append((rr, cc))  # Vurma imkanını əlavə et
                    break  # Düşmən daşını vurduqdan sonra dövrü dayandır
                else:
                    break  # Öz daşına rast gəldikdə dövrü dayandır
                r += dr
                c += dc

        return valid_moves

    def remove_piece(self, pos):
        # Düşmən daşını lövhədən silir
        r, c = pos
        self.board[r][c] = None

# Oyun idarəetmə sinifi
class DamaGame:
    def __init__(self, root):
        # Lövhəni və ilk oyunçunun növbəsini təyin edir
        self.board = Board()
        self.turn = "r"
        self.root = root
        # Oyun pəncərəsini (canvas) yaradaraq ölçülərini müəyyən edir
        self.canvas = tk.Canvas(root, width=400, height=400)
        self.canvas.pack()
        # Pəncərədəki kliklər üçün hadisə bağlayır
        self.canvas.bind("<Button-1>", self.on_click)
        self.selected_piece = None  # Seçilmiş daş
        self.valid_moves = []  # Mümkün hərəkətlər
        self.draw_board()  # Lövhəni çək

    def draw_board(self):
        # Lövhənin görünüşünü çəkir
        for row in range(8):
            for col in range(8):
                # Hər hüceyrənin koordinatlarını hesablayır
                x1 = col * 50
                y1 = row * 50
                x2 = x1 + 50
                y2 = y1 + 50
                # Hüceyrənin rəngini təyin edir
                color = "white" if (row + col) % 2 == 0 else "gray"
                # Hüceyrəni çəkir
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color)

                # Hüceyrədə daş varsa, onu çəkir
                piece = self.board.board[row][col]
                if piece:
                    self.canvas.create_text((x1 + x2) // 2, (y1 + y2) // 2, text=str(piece), font=("Arial", 20))

    def on_click(self, event):
        # İstifadəçi klik etdikdə bu metod çağırılır
        col = event.x // 50  # Klik olunan sütun
        row = event.y // 50  # Klik olunan sıra
        if self.selected_piece:
            # Əgər bir daş seçilibsə
            end = (row, col)
            if end in self.valid_moves:
                # Hərəkət etibarlıdırsa, onu icra et
                start = self.selected_piece
                # Vurma əməliyyatını həyata keçir
                if abs(start[0] - end[0]) == 2:
                    middle = ((start[0] + end[0]) // 2, (start[1] + end[1]) // 2)
                    self.board.remove_piece(middle)  # Düşmən daşını sil
                self.board.move_piece(start, end)  # Daşı yerini dəyiş
                self.turn = "b" if self.turn == "r" else "r"  # Növbəni dəyiş
                self.selected_piece = None  # Seçimi sıfırla
                self.valid_moves = []  # Mümkün hərəkətləri sıfırla
                self.draw_board()  # Lövhəni yenidən çək
                winner = self.is_winner()  # Qalibi yoxla
                if winner:
                    messagebox.showinfo("Qalib!", winner)  # Qalib haqqında məlumat pəncərəsi aç

            else:
                # Əgər seçilmiş daşa etibarlı bir son nöqtə deyilsə, seçimi sıfırla
                self.selected_piece = None
                self.valid_moves = []
        else:
            # Əgər heç bir daş seçilməyibsə
            start = (row, col)
            piece = self.board.board[row][col]
            if piece and piece.color == self.turn:
                # Əgər klik olunan hüceyrədəki daş öz növbənizdədirsə, onu seç
                self.selected_piece = start
                self.valid_moves = self.board.get_valid_moves(start)  # Mümkün hərəkətləri al

    def is_winner(self):
        # Oyunçuların qalib olub-olmamasını yoxlayır
        reds = blacks = 0
        for row in self.board.board:
            for piece in row:
                if piece:
                    if piece.color == "r":
                        reds += 1  # Qırmızı daşların sayını artır
                    elif piece.color == "b":
                        blacks += 1  # Qara daşların sayını artır
        if reds == 0:
            return "Qara oyunçu qalib gəldi!"  # Qara qalib gəldiyi halda
        elif blacks == 0:
            return "Qırmızı oyunçu qalib gəldi!"  # Qırmızı qalib gəldiyi halda
        return None  # Hələlik qalib yoxdur

# Tkinter pəncərəsini yaratmaq
if __name__ == "__main__":
    root = tk.Tk()  # Tkinter pəncərəsini yaradın
    root.title("Dama Oyunu")  # Pəncərənin başlığını təyin edin
    game = DamaGame(root)  # Dama oyunu obyekti yaradın
    root.mainloop()  # Pəncərə açıq qaldığı müddətdə dövrü davam et
*