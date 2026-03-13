import tkinter as tk

class ToggleButtonApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Toggle Button")
        self.is_on = False

        self.button = tk.Button(root, text="OFF", width=10, height=3, bg="red", fg="white", command=self.toggle)
        self.button.pack(pady=20)

    def toggle(self):
        self.is_on = not self.is_on
        if self.is_on:
            self.button.config(text="ON", bg="green")
        else:
            self.button.config(text="OFF", bg="red")

if __name__ == "__main__":
    root = tk.Tk()
    app = ToggleButtonApp(root)
    root.mainloop()
