import tkinter as tk
from tkinter import scrolledtext, ttk, messagebox
from stock_analysis import fetch_and_analyze

def create_gui(window):
    frame = tk.Frame(window)
    frame.pack()

    # Dark mode switch
    dark_mode_var = tk.BooleanVar()
    dark_mode_checkbox = ttk.Checkbutton(frame, text="Dark Mode", variable=dark_mode_var)
    dark_mode_checkbox.grid(row=0, column=2, padx=10, pady=10)

    symbol_label = tk.Label(frame, text="Enter Stock Symbol:", background="#282828", foreground="#FFFFFF")
    symbol_label.grid(row=1, column=0, padx=10, pady=10)

    symbol_entry = tk.Entry(frame)
    symbol_entry.grid(row=1, column=1, padx=10, pady=10)

    result_label = tk.Label(frame, text="Results:", background="#282828", foreground="#FFFFFF")
    result_label.grid(row=2, column=0, padx=10, pady=10)

    result_text = scrolledtext.ScrolledText(frame, height=15, width=60)
    result_text.grid(row=2, column=1, padx=10, pady=10, columnspan=2)

    # Create the result_table only once
    result_table = ttk.Treeview(frame)
    result_table['columns'] = ('Metric', 'Value')
    result_table.column('#0', width=0, stretch=tk.NO)
    result_table.column('Metric', anchor=tk.CENTER, width=80)
    result_table.column('Value', anchor=tk.CENTER, width=80)
    
    result_table.heading('#0', text='', anchor=tk.CENTER)
    result_table.heading('Metric', text='Metric', anchor=tk.CENTER)
    result_table.heading('Value', text='Value', anchor=tk.CENTER)

    def on_fetch_click():
        symbol = symbol_entry.get()
        if not symbol.isalpha() or not symbol.isalnum():
            messagebox.showerror("Error", "Invalid stock symbol")
            return
        results = fetch_and_analyze(symbol)
        
        # Clear existing items in the result_table
        result_table.delete(*result_table.get_children())
        
        if results is not None:
            result_table.insert(parent='', index='end', iid=0, text='', values=('Stock Price', results.get('stock_price', 'N/A')))
            result_table.insert(parent='', index='end', iid=1, text='', values=('Volume', results.get('volume', 'N/A')))
            result_table.insert(parent='', index='end', iid=2, text='', values=('Sentiment', results.get('sentiment', 'N/A')))
            result_table.insert(parent='', index='end', iid=3, text='', values=('Grade', results.get('grade', 'N/A')))
             
        else:
            # Handle the case when results is None
            print("Results is None")

    result_table.grid(row=3, column=0, columnspan=3)

    fetch_button = tk.Button(frame, text="Fetch and Analyze", command=on_fetch_click, background="#282828", foreground="#FFFFFF")
    fetch_button.grid(row=4, column=0, columnspan=3, pady=10)

    def toggle_dark_mode():
        if dark_mode_var.get():
            # Dark mode theme
            window.configure(bg="#282828")  # Set the background color of the main window
            frame.configure(bg="#282828")
            symbol_label.configure(background="#282828", foreground="#FFFFFF")
        else:
            # Light mode theme (change 'clam' to your preferred light mode theme)
            window.configure(bg="#FFFFFF")  # Set the background color of the main window
            frame.configure(bg="#ffffff")
            symbol_label.configure(background="#FFFFFF", foreground="#000000")
    
    # Set the dark mode switch callback
    dark_mode_var.trace_add('write', lambda *args: toggle_dark_mode())

    toggle_dark_mode()
