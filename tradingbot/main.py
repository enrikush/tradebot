import tkinter as tk
from gui import create_gui
from stock_analysis import fetch_and_analyze

if __name__ == "__main__":
    window = tk.Tk()
    window.title("Stock Data Fetcher and Analyzer")
    create_gui(window)
    window.mainloop()
