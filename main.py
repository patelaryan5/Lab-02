import tkinter as tk
import backend
from frontend import CatalogGUI

def main():
    root = tk.Tk()
    app = CatalogGUI(root, backend)
    root.mainloop()

if __name__ == "__main__":
    main()
