import tkinter as tk
import frames
import sqlalchemy

engine_post = sqlalchemy.create_engine('postgresql://moderator:123@localhost/postgres', future=True)
engine_new = sqlalchemy.create_engine('postgresql://moderator:123@localhost/lab_tickets', future=True)

root = tk.Tk()


app = frames.App(root, engine_post, engine_new)

root.title("Ticket application")
root.geometry('800x600')

root.mainloop()

