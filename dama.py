# Şahmat daşını təmsil edən sinif
class Piece:
    def __init__(self, color, king=False):
        # Rəngi və "king" (şah) statusunu təyin edir
        self.color = color
        self.king = king

    def make_king(self):
        # Daşı "king" (şah) statusuna keçirir
        self.king = True

    def __repr__(self):
        # Daşı mətndə təqdim etmək üçün rəngi böyük hərflə qaytarır, əgər kingdirsə
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
        # Sütun nömrələrini çap edir
        print("  0 1 2 3 4 5 6 7")
        for idx, row in enumerate(self.board):
            # Hər sıranın əvvəlində sıra nömrəsini əlavə edir
            print(idx, " ".join([str(piece) if piece else "." for piece in row]))
        print()

    def move_piece(self, start, end):
        # Daşı başlanğıc nöqtədən son nöqtəyə hərəkət etdirir
        piece = self.board[start[0]][start[1]]
        self.board[end[0]][end[1]] = piece
        self.board[start[0]][start[1]] = None

        # Əgər vurma əməliyyatı baş veribsə, vurulan rəqib daşını lövhədən çıxarır
        if abs(start[0] - end[0]) == 2:  # Vurma əməliyyatı 2 sıranı keçirsə, rəqib daşı çıxarır
            middle_row = (start[0] + end[0]) // 2
            middle_col = (start[1] + end[1]) // 2
            self.board[middle_row][middle_col] = None

        # Əks tərəfə çatan daşı "king" statusuna keçirir
        if end[0] == 0 and piece.color == 'r':
            piece.make_king()
        elif end[0] == 7 and piece.color == 'b':
            piece.make_king()

    def get_valid_moves(self, pos):
        # Seçilmiş daş üçün mümkün hərəkətləri və vurma əməliyyatlarını qaytarır
        row, col = pos
        piece = self.board[row][col]
        if not piece:
            return []

        # Hərəkət istiqamətləri müəyyən edilir: qırmızı və qara daşlar üçün fərqlidir
        directions = [(-1, -1), (-1, 1)] if piece.color == "r" else [(1, -1), (1, 1)]
        if piece.king:
            directions += [(-d[0], -d[1]) for d in directions]

        valid_moves = []
        for dr, dc in directions:
            r, c = row + dr, col + dc
            # Əgər bir addımda boşdursa, sadə hərəkət icazəlidir
            if 0 <= r < 8 and 0 <= c < 8 and self.board[r][c] is None:
                valid_moves.append((r, c))

            # Əgər rəqib daşı varsa və ondan sonra boş yer varsa, vurma mümkündür
            elif 0 <= r + dr < 8 and 0 <= c + dc < 8:
                if self.board[r][c] and self.board[r][c].color != piece.color:
                    if self.board[r + dr][c + dc] is None:
                        valid_moves.append((r + dr, c + dc))

        return valid_moves

# Oyun idarəetmə sinifi
class DamaGame:
    def __init__(self):
        # Lövhəni və ilk oyunçunun növbəsini təyin edir
        self.board = Board()
        self.turn = "r"
        
        

    def play_turn(self, start, end):
        # Seçilmiş başlanğıc və son nöqtəyə əsasən hərəkəti icra edir
        piece = self.board.board[start[0]][start[1]]
        if piece and piece.color == self.turn:
            # Əgər hərəkət etibarlıdırsa, onu icra edir
            valid_moves = self.board.get_valid_moves(start)
            if end in valid_moves:
                self.board.move_piece(start, end)
                # Növbəni digər oyunçuya keçirir
                self.turn = "b" if self.turn == "r" else "r"
                return True
        return False

    def is_winner(self):
        # Oyunçu qazanıb-qazanmadığını yoxlayır
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


# Konsol üzərində sadə oyun
game = DamaGame()
game.board.print_board()

while True:
    # İstifadəçidən başlanğıc və son mövqeləri soruşur
    start = tuple(map(int, input(f"{game.turn.upper()} oyunçu, başlanğıc mövqeyi daxil edin (sıra sütun): ").split()))
    end = tuple(map(int, input(f"{game.turn.upper()} oyunçu, son mövqeyi daxil edin (sıra sütun): ").split()))
    
    # Hərəkət icra edilərsə, lövhə yenilənir
    if game.play_turn(start, end):
        game.board.print_board()
    else:
        print("Yanlış hərəkət, yenidən cəhd edin.")

    # Qalib varsa, oyun sona çatır
    winner = game.is_winner()
    if winner:
        print(winner)
        break
