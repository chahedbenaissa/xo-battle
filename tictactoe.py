import tkinter as tk
from tkinter import simpledialog, messagebox
import threading
import socket
import random
import queue

# --- Networking constants ---
PORT = 65432
BUFFER_SIZE = 1024

# --- Game logic ---
playerX = "X"
playerO = "O"
color_blue = "#4584b6"
color_yellow = "#ffde57"
color_gray = "#343434"
color_light_gray = "#646464"

def get_local_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "127.0.0.1"

class NetworkGame:
    def __init__(self):
        self.sock = None
        self.conn = None
        self.is_host = False
        self.running = False
        self.my_turn = False

    def host(self):
        self.is_host = True
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind(('', PORT))
        self.sock.listen(1)
        self.conn, addr = self.sock.accept()
        self.running = True

    def join(self, host_ip):
        self.is_host = False
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((host_ip, PORT))
        self.conn = self.sock
        self.running = True

    def send(self, msg):
        try:
            self.conn.sendall(msg.encode())
        except Exception:
            self.running = False

    def receive(self):
        try:
            data = self.conn.recv(BUFFER_SIZE)
            return data.decode() if data else None
        except Exception:
            self.running = False
            return None

    def close(self):
        self.running = False
        try:
            if self.conn:
                self.conn.close()
            if self.is_host and self.sock:
                self.sock.close()
        except Exception:
            pass

class TicTacToeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Tic Tac Toe")
        self.root.resizable(False, False)
        self.mode = tk.StringVar(value="PvP")
        self.player_symbol = tk.StringVar(value=playerX)
        self.online_role = tk.StringVar(value="host")
        self.network = None
        self.curr_player = playerX
        self.turns = 0
        self.game_over = False
        self.board = [[None for _ in range(3)] for _ in range(3)]
        self.ui_queue = queue.Queue()
        self.setup_ui()
        self.check_queue()

    def check_queue(self):
        """Vérifie régulièrement la queue pour les mises à jour d'interface"""
        try:
            while True:
                task = self.ui_queue.get_nowait()
                task()
        except queue.Empty:
            pass
        self.root.after(100, self.check_queue)

    def setup_ui(self):
        self.setup_frame = tk.Frame(self.root, background=color_gray)
        self.setup_frame.pack(padx=20, pady=20)

        tk.Label(self.setup_frame, text="Tic Tac Toe", font=("Consolas", 24, "bold"),
                 background=color_gray, foreground="white").pack(pady=(0, 20))

        tk.Label(self.setup_frame, text="Choose Mode:", font=("Consolas", 16),
                 background=color_gray, foreground="white").pack(anchor="w")
        tk.Radiobutton(self.setup_frame, text="Player vs Player (Local)", variable=self.mode, value="PvP",
                       font=("Consolas", 14), background=color_gray, foreground="white", selectcolor=color_light_gray).pack(anchor="w")
        tk.Radiobutton(self.setup_frame, text="Player vs AI", variable=self.mode, value="PvAI",
                       font=("Consolas", 14), background=color_gray, foreground="white", selectcolor=color_light_gray).pack(anchor="w")
        tk.Radiobutton(self.setup_frame, text="Player vs Player (Online)", variable=self.mode, value="Online",
                       font=("Consolas", 14), background=color_gray, foreground="white", selectcolor=color_light_gray).pack(anchor="w")

        tk.Label(self.setup_frame, text="Choose Your Symbol:", font=("Consolas", 16),
                 background=color_gray, foreground="white").pack(anchor="w", pady=(20, 0))
        tk.Radiobutton(self.setup_frame, text="X (goes first)", variable=self.player_symbol, value=playerX,
                       font=("Consolas", 14), background=color_gray, foreground="white", selectcolor=color_light_gray).pack(anchor="w")
        tk.Radiobutton(self.setup_frame, text="O", variable=self.player_symbol, value=playerO,
                       font=("Consolas", 14), background=color_gray, foreground="white", selectcolor=color_light_gray).pack(anchor="w")

        self.online_frame = tk.Frame(self.setup_frame, background=color_gray)
        tk.Label(self.online_frame, text="Online Role:", font=("Consolas", 16),
                 background=color_gray, foreground="white").pack(anchor="w", pady=(20, 0))
        tk.Radiobutton(self.online_frame, text="Host", variable=self.online_role, value="host",
                       font=("Consolas", 14), background=color_gray, foreground="white", selectcolor=color_light_gray).pack(anchor="w")
        tk.Radiobutton(self.online_frame, text="Join", variable=self.online_role, value="join",
                       font=("Consolas", 14), background=color_gray, foreground="white", selectcolor=color_light_gray).pack(anchor="w")
        self.mode.trace_add("write", self.toggle_online_options)

        tk.Button(self.setup_frame, text="Start Game", font=("Consolas", 16, "bold"),
                  background=color_blue, foreground="white", command=self.start_game).pack(pady=(30, 0))

        # Main game frame
        self.frame = tk.Frame(self.root)
        self.label = tk.Label(self.frame, text="", font=("Consolas", 20), background=color_gray,
                                 foreground="white")
        self.label.grid(row=0, column=0, columnspan=3, sticky="we")

        for row in range(3):
            for column in range(3):
                self.board[row][column] = tk.Button(self.frame, text="", font=("Consolas", 50, "bold"),
                                                     background=color_gray, foreground=color_blue, width=4, height=1,
                                                     command=lambda row=row, column=column: self.set_tile(row, column))
                self.board[row][column].grid(row=row+1, column=column)

        self.button = tk.Button(self.frame, text="Restart", font=("Consolas", 20), background=color_gray,
                                 foreground="white", command=self.new_game)
        self.button.grid(row=4, column=0, columnspan=3, sticky="we")

    def toggle_online_options(self, *args):
        if self.mode.get() == "Online":
            self.online_frame.pack(anchor="w", pady=(10, 0))
        else:
            self.online_frame.pack_forget()

    def start_game(self):
        self.setup_frame.pack_forget()
        self.frame.pack()
        self.new_game()
        if self.mode.get() == "Online":
            self.start_online_game()

    def new_game(self):
        self.turns = 0
        self.game_over = False
        self.curr_player = playerX
        for row in range(3):
            for column in range(3):
                self.board[row][column].config(text="", foreground=color_blue, background=color_gray, state="normal")
        self.label.config(text=f"{self.curr_player}'s turn", foreground="white")

    def disable_board(self):
        for row in range(3):
            for col in range(3):
                self.board[row][col]["state"] = "disabled"

    def enable_board(self):
        for row in range(3):
            for col in range(3):
                if self.board[row][col]["text"] == "":
                    self.board[row][col]["state"] = "normal"

    def set_tile(self, row, column):
        if self.game_over or self.board[row][column]["text"]:
            return

        symbol = self.curr_player

        if self.mode.get() == "PvAI" and symbol != self.player_symbol.get():
            return

        self.board[row][column]["text"] = symbol
        self.check_winner()

        if not self.game_over:
            if self.mode.get() == "PvP":
                self.curr_player = playerO if self.curr_player == playerX else playerX
                self.label.config(text=f"{self.curr_player}'s turn")
            elif self.mode.get() == "PvAI":
                if self.curr_player == self.player_symbol.get():
                    self.curr_player = playerO if self.curr_player == playerX else playerX
                    self.label.config(text="AI's turn")
                    self.root.after(500, self.ai_move)
            elif self.mode.get() == "Online":
                self.network.send(f"{row},{column}")
                self.network.my_turn = False
                self.label.config(text="Opponent's turn")
                self.disable_board()

    def ai_move(self):
        empty = [(r, c) for r in range(3) for c in range(3) if not self.board[r][c]["text"]]
        if not empty or self.game_over:
            return
        r, c = random.choice(empty)
        self.board[r][c]["text"] = playerO if self.player_symbol.get() == playerX else playerX
        self.check_winner()
        if not self.game_over:
            self.curr_player = self.player_symbol.get()
            self.label.config(text="Your turn")

    def check_winner(self):
        self.turns += 1
        b = self.board
        for row in range(3):
            if b[row][0]["text"] == b[row][1]["text"] == b[row][2]["text"] != "":
                self.declare_winner(b[row][0]["text"], [(row, 0), (row, 1), (row, 2)])
                return
        for col in range(3):
            if b[0][col]["text"] == b[1][col]["text"] == b[2][col]["text"] != "":
                self.declare_winner(b[0][col]["text"], [(0, col), (1, col), (2, col)])
                return
        if b[0][0]["text"] == b[1][1]["text"] == b[2][2]["text"] != "":
            self.declare_winner(b[0][0]["text"], [(0, 0), (1, 1), (2, 2)])
            return
        if b[0][2]["text"] == b[1][1]["text"] == b[2][0]["text"] != "":
            self.declare_winner(b[0][2]["text"], [(0, 2), (1, 1), (2, 0)])
            return

        if self.turns == 9:
            self.declare_winner(None)
            return

    def declare_winner(self, winner, winning_coords=None):
        if winner:
            for (r, c) in winning_coords:
                self.board[r][c].config(background=color_yellow)
            self.label.config(text=f"{winner} wins!", foreground="green")
        else:
            self.label.config(text="It's a draw!", foreground="red")
        self.game_over = True
        self.disable_board()

    def start_online_game(self):
        ip = get_local_ip()
        role = self.online_role.get()
        if role == "host":
            self.network = NetworkGame()
            self.network.host()
            self.curr_player = playerX
            self.label.config(text=f"{self.curr_player}'s turn")
        elif role == "join":
            host_ip = simpledialog.askstring("Host IP", "Enter the host's IP address:")
            self.network = NetworkGame()
            self.network.join(host_ip)
            self.curr_player = playerO
            self.label.config(text="Waiting for opponent's move")
            self.network.send(f"join_{ip}")
            self.network.my_turn = False
            self.disable_board()

root = tk.Tk()
app = TicTacToeApp(root)
root.mainloop()
