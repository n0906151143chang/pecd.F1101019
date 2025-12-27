import tkinter as tk
import random
import time

# ======================
# 難度設定
# ======================
DIFFICULTY = {
    "初級": (9, 9, 10),
    "中級": (16, 16, 40),
    "高級": (16, 30, 99)
}

CELL_SIZE = 32


class Minesweeper:
    def __init__(self, root, rows, cols, mines):
        self.root = root
        self.rows = rows
        self.cols = cols
        self.mine_count = mines

        # 狀態變數
        self.first_click = True
        self.mines = set()
        self.revealed = set()
        self.flags = set()
        self.start_time = None
        self.timer_running = False

        # 清空畫面
        for widget in root.winfo_children():
            widget.destroy()

        # ===== 上方資訊區 =====
        top_frame = tk.Frame(root)
        top_frame.pack(pady=10)

        self.timer_label = tk.Label(
            top_frame, text="時間：0 秒", font=("Arial", 14)
        )
        self.timer_label.pack(side=tk.LEFT, padx=20)

        restart_btn = tk.Button(
            top_frame, text="重新開始", font=("Arial", 12),
            command=self.restart
        )
        restart_btn.pack(side=tk.RIGHT)

        # ===== 遊戲區 =====
        self.board_frame = tk.Frame(root, bg="#AAAAAA")
        self.board_frame.pack()

        self.buttons = {}
        self.create_board()

    # ======================
    # 建立地圖按鈕
    # ======================
    def create_board(self):
        for r in range(self.rows):
            for c in range(self.cols):
                btn = tk.Button(
                    self.board_frame,
                    width=2,
                    height=1,
                    font=("Arial", 12),
                    bg="#E0E0E0",
                    relief=tk.RAISED,
                    command=lambda r=r, c=c: self.left_click(r, c)
                )
                btn.bind("<Button-3>", lambda e, r=r, c=c: self.right_click(r, c))
                btn.grid(row=r, column=c)
                self.buttons[(r, c)] = btn

    # ======================
    # 產生地雷（避開第一次）
    # ======================
    def place_mines(self, safe):
        while len(self.mines) < self.mine_count:
            cell = (
                random.randint(0, self.rows - 1),
                random.randint(0, self.cols - 1)
            )
            if cell != safe:
                self.mines.add(cell)

    # ======================
    # 左鍵點擊
    # ======================
    def left_click(self, r, c):
        if self.first_click:
            self.place_mines((r, c))
            self.first_click = False
            self.start_timer()

        if (r, c) in self.flags:
            return

        if (r, c) in self.mines:
            self.game_over(False)
            return

        self.reveal(r, c)

        if len(self.revealed) == self.rows * self.cols - self.mine_count:
            self.game_over(True)

    # ======================
    # 右鍵插旗
    # ======================
    def right_click(self, r, c):
        btn = self.buttons[(r, c)]

        if (r, c) in self.revealed:
            return

        if (r, c) in self.flags:
            btn.config(text="")
            self.flags.remove((r, c))
        else:
            btn.config(text="🚩")
            self.flags.add((r, c))

    # ======================
    # 開格子
    # ======================
    def reveal(self, r, c):
        if (r, c) in self.revealed:
            return

        self.revealed.add((r, c))
        btn = self.buttons[(r, c)]
        btn.config(relief=tk.SUNKEN, bg="#D0D0D0", state=tk.DISABLED)

        count = self.count_mines(r, c)
        if count > 0:
            btn.config(text=str(count))
        else:
            for nr in range(r - 1, r + 2):
                for nc in range(c - 1, c + 2):
                    if 0 <= nr < self.rows and 0 <= nc < self.cols:
                        self.reveal(nr, nc)

    # ======================
    # 計算周圍地雷
    # ======================
    def count_mines(self, r, c):
        count = 0
        for nr in range(r - 1, r + 2):
            for nc in range(c - 1, c + 2):
                if (nr, nc) in self.mines:
                    count += 1
        return count

    # ======================
    # 計時器
    # ======================
    def start_timer(self):
        self.start_time = time.time()
        self.timer_running = True
        self.update_timer()

    def update_timer(self):
        if self.timer_running:
            elapsed = int(time.time() - self.start_time)
            self.timer_label.config(text=f"時間：{elapsed} 秒")
            self.root.after(1000, self.update_timer)

    # ======================
    # 遊戲結束
    # ======================
    def game_over(self, win):
        self.timer_running = False

        for mine in self.mines:
            self.buttons[mine].config(text="💣", bg="red")

        msg = "🎉 勝利！" if win else "💥 遊戲結束"
        self.timer_label.config(text=msg)

    # ======================
    # 重新開始（回到選單）
    # ======================
    def restart(self):
        show_menu(self.root)


# ======================
# 主選單畫面
# ======================
def show_menu(root):
    for widget in root.winfo_children():
        widget.destroy()

    tk.Label(
        root, text="踩地雷",
        font=("Arial", 24, "bold")
    ).pack(pady=20)

    tk.Label(
        root, text="選擇難度",
        font=("Arial", 14)
    ).pack(pady=10)

    for name, setting in DIFFICULTY.items():
        btn = tk.Button(
            root, text=name,
            font=("Arial", 14),
            width=10,
            command=lambda s=setting: Minesweeper(root, *s)
        )
        btn.pack(pady=5)


# ======================
# 程式進入點
# ======================
if __name__ == "__main__":
    root = tk.Tk()
    root.title("踩地雷")
    root.resizable(False, False)
    show_menu(root)
    root.mainloop()
