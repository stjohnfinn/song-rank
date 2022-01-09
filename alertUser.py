from tkinter import messagebox

def alertUser(title, message, type):
    if type == 'error':
        messagebox.showerror(title, message)
    elif type == 'info':
        messagebox.showinfo(title, message)