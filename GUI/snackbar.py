import tkinter as tk


class GuiSnackbar:
    def __init__(self, parent):
        self._parent = parent
        self._snackbar_text = tk.StringVar()

    def show(self, message, duration=3000):
        self._snackbar_text.set(message)
        snackbar = tk.Label(self._parent, textvariable=self._snackbar_text, background="darkseagreen1", anchor='center')
        snackbar.place(relx=0.5, rely=0.95, anchor=tk.CENTER)
        self._parent.after(duration, snackbar.destroy)
