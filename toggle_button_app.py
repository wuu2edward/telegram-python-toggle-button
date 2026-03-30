import tkinter as tk

class ToggleButtonApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Toggle Button")

        self.var = tk.IntVar(value=0)  # 0=OFF, 1=ON

        self.button = tk.Checkbutton(
            root,
            text="OFF",
            variable=self.var,
            width=10,
            height=3,
            fg="white",
            bg="red",
            selectcolor="green",
            command=self.toggle
        )
        self.button.pack(pady=20)
        self.toggle()  # Initialize colors/states

    def toggle(self):
        if self.var.get():
            self.button.config(text="ON", bg="green")
        else:
            self.button.config(text="OFF", bg="red")

if __name__ == "__main__":
    root = tk.Tk()
    app = ToggleButtonApp(root)
    root.mainloop()
