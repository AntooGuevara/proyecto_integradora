import tkinter as tk
from controller.controller import RentasController

def main():
    root = tk.Tk()
    app = RentasController(root)
    root.mainloop()

if __name__ == "__main__":
    main()