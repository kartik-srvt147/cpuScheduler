import tkinter as tk
from ttkbootstrap import Style
from gui.app_ui import create_ui

if __name__ == "__main__":
    root = tk.Tk()
    root.title("CPU Scheduler")
    style = Style(theme="solar")

    root.geometry("900x600")
    create_ui(root)
    root.mainloop()