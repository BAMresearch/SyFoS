import tkinter as tk
import ttkbootstrap as ttk

from main_window import MainWindow

if __name__ == "__main__":
	app = ttk.Window()
	MainWindow(app)
	app.mainloop()