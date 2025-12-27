import random
import time

try:
    import tkinter as tk
except Exception:
    print("無法匯入 tkinter。請確認已安裝 tkinter 並且有可用的圖形介面（macOS: 建議使用系統 Python 或安裝 python-tk）。")
    raise SystemExit(1)

# =========================
# 遊戲設定（可自行調整）
# =========================
ROWS = 9          # 行數
COLS = 9          # 列數
MINES = 10        # 地雷數量
CELL_SIZE = 40    # 每格大小（像素）

# =========================
# 主程式類別
# =========================
class Minesweeper:
    def __init__(self, root):
        self.root = root
        self.root.title("踩地雷")

        # 是否已經第一次點擊（用來保證第一次不踩雷）
        self.first_click = True

        # 計時用
        self.start_time = None
        self.timer_running = False

        # 儲存地雷位置
        self.mines = set()

        # 記錄每個格子的狀態
        self.buttons = {}
        self.revealed = set()
        self.flags = set()

        # 上方資訊欄
        self.info_label = tk.Label(root, text="時間：0 秒", font=("Arial", 14))
        self.info_label.pack()

        # 遊戲區域
        self.frame = tk.Frame(root)
        self.frame.pack()

        # 建立格子
        self.create_buttons()

    # =========================
    # 建立按鈕格子
    # =========================
    def create_buttons(self):
        for r in range(ROWS):
            for c in range(COLS):
                btn = tk.Button(
                    self.frame,
                    width=2,
                    height=1,
                    font=("Arial", 14),
                    command=lambda r=r, c=c: self.left_click(r, c)
                )
                # 綁定右鍵事件（插旗）
                btn.bind("<Button-3>", lambda e, r=r, c=c: self.right_click(r, c))
                btn.grid(row=r, column=c)
                self.buttons[(r, c)] = btn

    # =========================
    # 第一次點擊後才生成地雷
    # =========================
    def place_mines(self, safe_cell):
        while len(self.mines) < MINES:
            cell = (random.randint(0, ROWS - 1), random.randint(0, COLS - 1))
            # 確保地雷不會在第一次點擊的位置
            if cell != safe_cell:
                self.mines.add(cell)

    # =========================
    # 左鍵點擊（開格子）
    # =========================
    def left_click(self, r, c):
        # 第一次點擊
        if self.first_click:
            self.place_mines((r, c))
            self.first_click = False
            self.start_timer()

        # 已經插旗就不能開
        if (r, c) in self.flags:
            return

        # 踩到地雷
        if (r, c) in self.mines:
            self.game_over(False)
            return

        self.reveal(r, c)

        # 勝利判斷
        if len(self.revealed) == ROWS * COLS - MINES:
            self.game_over(True)

    # =========================
    # 右鍵點擊（插旗）
    # =========================
    def right_click(self, r, c):
        btn = self.buttons[(r, c)]

        if (r, c) in self.revealed:
            return

        # 插旗 / 取消旗子
        if (r, c) in self.flags:
            btn.config(text="")
            self.flags.remove((r, c))
        else:
            btn.config(text="🚩")
            self.flags.add((r, c))

    # =========================
    # 開啟格子
    # =========================
    def reveal(self, r, c):
        if (r, c) in self.revealed:
            return

        self.revealed.add((r, c))
        btn = self.buttons[(r, c)]
        btn.config(relief=tk.SUNKEN, state=tk.DISABLED)

        # 計算周圍地雷數
        count = self.count_mines(r, c)

        if count > 0:
            btn.config(text=str(count))
        else:
            # 若周圍沒地雷，自動展開
            for nr in range(r - 1, r + 2):
                for nc in range(c - 1, c + 2):
                    if 0 <= nr < ROWS and 0 <= nc < COLS:
                        self.reveal(nr, nc)

    # =========================
    # 計算周圍地雷數
    # =========================
    def count_mines(self, r, c):
        count = 0
        for nr in range(r - 1, r + 2):
            for nc in range(c - 1, c + 2):
                if (nr, nc) in self.mines:
                    count += 1
        return count

    # =========================
    # 計時器
    # =========================
    def start_timer(self):
        self.start_time = time.time()
        self.timer_running = True
        self.update_timer()

    def update_timer(self):
        if self.timer_running:
            elapsed = int(time.time() - self.start_time)
            self.info_label.config(text=f"時間：{elapsed} 秒")
            self.root.after(1000, self.update_timer)

    # =========================
    # 遊戲結束
    # =========================
    def game_over(self, win):
        self.timer_running = False

        # 顯示所有地雷
        for mine in self.mines:
            btn = self.buttons[mine]
            btn.config(text="💣", bg="red")

        result = "你贏了！🎉" if win else "踩到地雷！💥"
        self.info_label.config(text=result)

        # 顯示重新開始按鈕
        restart_btn = tk.Button(self.root, text="重新開始", command=self.restart)
        restart_btn.pack()

    # =========================
    # 重新開始遊戲
    # =========================
    def restart(self):
        self.root.destroy()
        main()

# =========================
# 主程式入口
# =========================
def main():
    root = tk.Tk()
    Minesweeper(root)
    root.mainloop()


if __name__ == "__main__":
    main()

