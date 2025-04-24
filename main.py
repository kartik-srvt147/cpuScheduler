# main.py
import tkinter as tk
import ttkbootstrap as ttk
from gui.app_ui import create_ui

def main():
    # Create the main window with ttkbootstrap theme
    root = ttk.Window(themename="solar")  # Changed from "darkly" to "solar"
    root.title("CPU Scheduler Simulator")
    root.geometry("1000x800")
    
    # Create the application UI
    create_ui(root)
    
    # Start the application
    root.mainloop()

if __name__ == "__main__":
    main()
