import customtkinter as ctk
from controller.controller import RentasController

def main():
    root = ctk.CTk()  # CAMBIADO: usar CTk en lugar de tk.Tk()
    app = RentasController(root)
    root.mainloop()

if __name__ == "__main__":
    main()