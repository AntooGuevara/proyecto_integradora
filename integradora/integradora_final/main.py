import customtkinter as ctk
from controller.controller import RentasController

def main():
    root = ctk.CTk()
    app = RentasController(root)
    root.mainloop()

if __name__ == "__main__":
    main()