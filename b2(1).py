import tkinter as tk
from tkinter import messagebox

def show_text():
    user_text = entry.get()
    messagebox.showinfo("你輸入的是", user_text)

# 建立主視窗
root = tk.Tk()
root.title("Tkinter Demo")
root.geometry("200x150")
# 標籤
label = tk.Label(root, text="請輸入文字：")
label.pack(pady=5)

# 輸入框
entry = tk.Entry(root, width=25)
entry.pack(pady=5)

# 按鈕
button = tk.Button(root, text="顯示文字", command=show_text)
button.pack(pady=10)

# 進入事件迴圈
root.mainloop()
print("程式結束")