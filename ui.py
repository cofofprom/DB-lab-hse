from tkinter import *
from ttkwidgets.autocomplete import AutocompleteCombobox
import tkinter as tk
from tkinter import ttk
import re
from tkinter.messagebox import showinfo
from tkinter import messagebox as ms
from sqlalchemy import text
import frames


class UserInterface(tk.Frame):

    def selected(self, event):
        selection = self.cinema_cb.get()
        print(selection)
        self.label["text"] = f"Your cinema is: {selection}. Now choose a movie"
        self.selected_cinema_id = next(filter(lambda x: x[1] == selection, self.db_cinemas))[0]
        print(self.selected_cinema_id)

    def selected2(self, event):
        selection = self.film_box.get()
        print(selection)
        self.label["text"] = f"Your film is: {selection}. Now choose a film session"
        self.selected_film_id = next(filter(lambda x: x[1] == selection, self.db_films))[0]
        print(self.selected_film_id)
        with self.master.engine_new.connect() as conn:
            self.db_sessions = conn.execute(text(f'SELECT * FROM find_specific_sessions({self.selected_cinema_id},'
                                                 f'{self.selected_film_id})')).all()

        print(self.db_sessions)
        self.session_cb['values'] = [f'{str(x[1])}, {str(x[2])}, {str(x[0])}' for x in self.db_sessions]

    def selected3(self, event):
        selection = self.session_cb.get()
        selection1 = self.row_cb.get()
        selection2 = self.seat_cb.get()
        print(selection)
        self.label["text"] = f"Your session is: {selection}, row {selection1}, seat {selection2}"
        self.selected_session_id = selection.split(', ')[-1]

    def genre_recommendation(self, event):
        selection = self.genre_box.get()
        print(selection)
        with self.master.engine_new.connect() as conn:
            query = conn.execute(text(f'SELECT * FROM get_recommendations(\'{selection}\')')).all()
        ms.showinfo(f"Recommended films in genre {selection}", "Recommended films:" + ', '.join([x[0] for x in query]))

    def purchase(self, event):
        cinema = self.cinema_cb.get()
        film = self.film_box.get()
        time = self.session_cb.get()
        row = self.row_cb.get()
        seat = self.seat_cb.get()
        price = int(self.row_cb.get()) * 100
        if ms.askyesno("Your ticket",
                       f"cinema: {cinema} \n"
                       f"film: {film} \n"
                       f"hall, time: {time} \n"
                       f"row: {row} \n"
                       f"seat: {seat} \n"
                       f"price: {price} \n"):
            print(cinema)
            with self.master.engine_new.connect() as conn:
                res = conn.execute(text(f'SELECT insert_ticket({seat},'
                                        f'{row},'
                                        f'{self.selected_session_id},'
                                        f'{price})'))
                conn.commit()
            print(res)
            self.pack_forget()
            frames.EntryFrame(self.master)

    def __init__(self, parent):
        super().__init__(parent)
        self.pack()
        self.label = ttk.Label(self, text="Choose a movie theater:")
        self.label.pack()

        self.l1 = Label(self, text="Cinemas:", )
        self.l1.pack()
        self.cinema_cb = ttk.Combobox(self)
        with self.master.engine_new.connect() as conn:
            self.db_cinemas = conn.execute(text('SELECT * FROM show_cinema()')).all()
        self.cinema_cb['values'] = [x[1] for x in self.db_cinemas]
        self.cinema_cb['state'] = 'readonly'
        self.cinema_cb.pack(padx=5, pady=5)
        self.cinema_cb.bind('<<ComboboxSelected>>', self.selected)

        self.l2 = Label(self, text="Films:", )
        self.l2.pack()
        with self.master.engine_new.connect() as conn:
            self.db_films = conn.execute(text('SELECT * FROM show_film()')).all()
        self.films = [x[1] for x in self.db_films]
        self.film_box = AutocompleteCombobox(self, width=20, completevalues=self.films)
        self.film_box.pack(anchor=N)
        self.film_box.bind('<<ComboboxSelected>>', self.selected2)

        self.l2 = Label(self, text="Search by genre:", )
        self.l2.pack()
        with self.master.engine_new.connect() as conn:
            g = conn.execute(text('SELECT * FROM get_genres()')).all()
        self.genres = [x[0] for x in g]
        self.genre_box = AutocompleteCombobox(self, width=20, completevalues=self.genres)
        self.genre_box.pack()
        self.genre_box.bind('<<ComboboxSelected>>', self.genre_recommendation)

        self.l3 = Label(self, text="Session:", )
        self.l3.pack()
        self.session_cb = ttk.Combobox(self)
        self.session_cb['values'] = []
        self.session_cb['state'] = 'readonly'
        self.session_cb.pack(padx=5, pady=5)
        self.session_cb.bind('<<ComboboxSelected>>', self.selected3)

        self.l3 = Label(self, text="Row:", )
        self.l3.pack()
        self.row_cb = ttk.Combobox(self)
        self.row_cb['values'] = [1, 2, 3, 4, 5]
        self.row_cb['state'] = 'readonly'
        self.row_cb.pack(padx=5, pady=5)
        self.row_cb.bind('<<ComboboxSelected>>', self.selected3)

        self.l3 = Label(self, text="Seat:", )
        self.l3.pack()
        self.seat_cb = ttk.Combobox(self)
        self.seat_cb['values'] = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        self.seat_cb['state'] = 'readonly'
        self.seat_cb.pack(padx=5, pady=5)
        self.seat_cb.bind('<<ComboboxSelected>>', self.selected3)
        self.btn = Button(self, text="Buy")
        self.btn.pack()
        self.btn.bind('<Button-1>', self.purchase)
