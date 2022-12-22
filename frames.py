import tkinter as tk
import tkinter.messagebox

import psycopg2
import sqlalchemy
from sqlalchemy import text

import frames
import ui


def create_database(engine):
    with engine.connect() as conn:
        try:
            print(conn.execute(text('CALL create_db()')))

        except:
            tk.messagebox.showerror('Engine error', 'Database already exist')
            return

    tk.messagebox.showinfo('DB created', 'Database created')


class App(tk.Frame):
    def __init__(self, master=None, engine_post=None, engine_new=None):
        super().__init__(master)
        self.pack()
        self.fr = EntryFrame(self)
        self.fr.pack()
        self.engine_post = engine_post
        self.engine_new = engine_new


class EntryFrame(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.pack()
        self.lbl = tk.Label(self, text='Please, choose what do you want to do')
        self.usr_btn = tk.Button(self, text='Buy tickets', command=self.usr_btn_click)
        self.adm_btn = tk.Button(self, text='Edit db', command=self.adm_btn_click)
        self.lbl.pack()
        self.usr_btn.pack()
        self.adm_btn.pack()

    def usr_btn_click(self):
        self.pack_forget()
        ui.UserInterface(self.master)

    def adm_btn_click(self):
        self.pack_forget()
        AdminActions(self.master)


class AdminActions(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.pack()
        tk.Label(self, text='DB edit options').pack()
        tk.Button(self, text='Edit cinemas', command=self.edit_cinemas).pack()
        tk.Button(self, text='Edit films', command=self.edit_films).pack()
        tk.Button(self, text='Edit sessions', command=self.edit_sessions).pack()
        tk.Button(self, text='Edit tickets', command=self.edit_tickets).pack()
        tk.Button(self, text='Create database', command=self.create_db).pack()
        tk.Button(self, text='Drop database', command=self.drop_db).pack()
        tk.Button(self, text='Clear database', command=self.clear_db).pack()

    def clear_db(self):
        with self.master.engine_new.connect() as conn:
            try:
                print(conn.execute(text('SELECT clear_all()')))
                conn.commit()
            except Exception as e:
                tk.messagebox.showerror('Engine error', 'Database doesnt exist')
                print(e)
                return

        tk.messagebox.showinfo('DB dropped', 'Database cleared')

    def create_db(self):
        create_database(self.master.engine_post)

    def drop_db(self):
        self.master.engine_new.dispose()
        with self.master.engine_post.connect() as conn:
            try:
                print(conn.execute(text('CALL drop_db()')))
            except Exception as e:
                tk.messagebox.showerror('Engine error', 'Database doesnt exist')
                print(e)
                return

        tk.messagebox.showinfo('DB dropped', 'Database dropped')

    def edit_cinemas(self):
        try:
            with self.master.engine_new.connect() as conn:
                res = conn.execute(text('SELECT * FROM show_cinema()')).all()
                self.pack_forget()
                CinemaView(self.master, res)
        except Exception as e:
            print(e)
            tk.messagebox.showerror('Engine error', 'Database doesnt exist. Create it first')

    def edit_films(self):
        try:
            with self.master.engine_new.connect() as conn:
                res = conn.execute(text('SELECT * FROM show_film()')).all()
                self.pack_forget()
                FilmView(self.master, res)
        except Exception as e:
            print(e)
            tk.messagebox.showerror('Engine error', 'Database doesnt exist. Create it first')

    def edit_sessions(self):
        try:
            with self.master.engine_new.connect() as conn:
                res = conn.execute(text('SELECT * FROM show_session()')).all()
                self.pack_forget()
                SessionView(self.master, res)
        except psycopg2.OperationalError as e:
            print(e)
            tk.messagebox.showerror('Engine error', 'Database doesnt exist. Create it first')
        except TypeError:
            tk.messagebox.showerror('Engine error', 'Theres no films or cinemas.')
            self.pack()

    def edit_tickets(self):
        try:
            with self.master.engine_new.connect() as conn:
                rrr = conn.execute(text('SELECT * FROM show_ticket()')).all()
                self.pack_forget()
                TicketView(self.master, rrr)
        except Exception as e:
            print(e)
            tk.messagebox.showerror('Engine error', 'Database doesnt exist. Create it first')


class CinemaView(tk.Frame):
    def __init__(self, master=None, data=[]):
        super().__init__(master)
        self.pack()
        tk.Label(self, text="Cinema table").pack()
        tk.Button(self, text='Exit', command=lambda:
                  self.pack_forget() or
                  frames.EntryFrame(self.master)).pack()
        self.records_frame = tk.Frame(self)
        self.records_frame.pack(side=tk.LEFT)
        self.action_frame = tk.Frame(self)
        self.action_frame.pack(side=tk.LEFT)
        self.insert_frame = tk.Frame(self.action_frame)
        self.insert_frame.pack(side=tk.LEFT)
        tk.Button(self.insert_frame, text='Insert', command=self.insert_record).pack()
        self.name = tk.Entry(self.insert_frame)
        self.address = tk.Entry(self.insert_frame)
        tk.Label(self.insert_frame, text='Name').pack()
        self.name.pack()
        tk.Label(self.insert_frame, text='Address').pack()
        self.address.pack()
        self.delete_frame = tk.Frame(self.action_frame)
        self.delete_frame.pack(side=tk.LEFT)
        tk.Button(self.delete_frame, text='Delete', command=self.delete_record).pack()
        tk.Label(self.delete_frame, text='Delete ID').pack()
        self.deleteid = tk.Entry(self.delete_frame)
        self.deleteid.pack()
        for rec in data:
            fr = tk.Frame(self.records_frame, borderwidth=2, relief='groove')
            fr.pack()
            l = tk.Label(fr, text=f'({rec[0]}) "{rec[1]}" || {rec[2]}')
            # l.bind('<Button-1>', lambda e: self.delete_record(rec[0]))
            l.pack(side=tk.LEFT)
            print(rec[0])
            # tk.Button(fr, text='D', command=lambda: self.delete_record(rec[0])).pack(side=tk.LEFT)

    def delete_record(self):
        idx = self.deleteid.get()
        with self.master.engine_new.connect() as conn:
            print(conn.execute(text(f"SELECT delete_cinema('{idx}')")))
            conn.commit()

        tk.messagebox.showinfo('Delete', 'OK')

        self.deleteid.delete(0, 'end')

        self.pack_forget()
        AdminActions(self.master).edit_cinemas()

    def insert_record(self):
        name = self.name.get()
        addr = self.address.get()
        with self.master.engine_new.connect() as conn:
            print(conn.execute(text(f'SELECT insert_cinema(\'{name}\', \'{addr}\')')))
            conn.commit()

        tk.messagebox.showinfo('Insert', 'OK')

        self.name.delete(0, 'end')
        self.address.delete(0, 'end')

        self.pack_forget()
        AdminActions(self.master).edit_cinemas()


class FilmView(tk.Frame):
    def __init__(self, master=None, data=[]):
        super().__init__(master)
        self.pack()
        tk.Label(self, text="Film table").pack()
        tk.Button(self, text='Exit', command=lambda:
            self.pack_forget() or
            frames.EntryFrame(self.master)).pack()
        self.records_frame = tk.Frame(self)
        self.records_frame.pack(side=tk.LEFT)
        self.action_frame = tk.Frame(self)
        self.action_frame.pack(side=tk.RIGHT)
        self.insert_frame = tk.Frame(self.action_frame)
        self.insert_frame.pack(side=tk.LEFT)
        tk.Button(self.insert_frame, text='Insert', command=self.insert_record).pack()
        self.name = tk.Entry(self.insert_frame)
        self.genre = tk.Entry(self.insert_frame)
        self.duration = tk.Entry(self.insert_frame)
        self.year = tk.Entry(self.insert_frame)
        self.country = tk.Entry(self.insert_frame)
        self.director = tk.Entry(self.insert_frame)
        tk.Label(self.insert_frame, text='Name').pack()
        self.name.pack()
        tk.Label(self.insert_frame, text='Genre').pack()
        self.genre.pack()
        tk.Label(self.insert_frame, text='Duration').pack()
        self.duration.pack()
        tk.Label(self.insert_frame, text='Year').pack()
        self.year.pack()
        tk.Label(self.insert_frame, text='Country').pack()
        self.country.pack()
        tk.Label(self.insert_frame, text='Director').pack()
        self.director.pack()
        print(data)
        self.delete_frame = tk.Frame(self.action_frame)
        self.delete_frame.pack(side=tk.LEFT)
        tk.Button(self.delete_frame, text='Delete', command=self.delete_record).pack()
        tk.Label(self.delete_frame, text='Delete ID').pack()
        self.deleteid = tk.Entry(self.delete_frame)
        self.deleteid.pack()
        tk.Button(self.delete_frame, text='Film info', command=self.film_info).pack()
        tk.Label(self.delete_frame, text='Info ID').pack()
        self.infoid = tk.Entry(self.delete_frame)
        self.infoid.pack()
        for rec in data:
            fr = tk.Frame(self.records_frame, borderwidth=2, relief='groove')
            fr.pack()
            l = tk.Label(fr, text=f'({rec[0]}) "{rec[1]}" || {rec[2]} || {rec[3]} || {rec[4]} || {rec[5]} || {rec[6]}')
            l.pack(side=tk.LEFT)
            print(rec[0])

    def delete_record(self):
        idx = self.deleteid.get()
        with self.master.engine_new.connect() as conn:
            print(conn.execute(text(f"SELECT delete_film('{idx}')")))
            conn.commit()

        tk.messagebox.showinfo('Delete', 'OK')

        self.deleteid.delete(0, 'end')

        self.pack_forget()
        AdminActions(self.master).edit_films()

    def film_info(self):
        idx = self.infoid.get()
        with self.master.engine_new.connect() as conn:
            info = conn.execute(text(f"SELECT * FROM find_film_by_id('{idx}')")).all()[0]
            conn.commit()
        print(info)
        tk.messagebox.showinfo("Film Info", f"Film name: {info[1]}\n"
                                            f"Genre: {info[2]}\n"
                                            f"Year: {info[4]}\n"
                                            f"Country: {info[5]}\n"
                                            f"Director: {info[6]}\n"
                                            f"Duration: {info[3].hour}:{info[3].minute}")

    def insert_record(self):
        name = self.name.get()
        genre = self.genre.get()
        duration = self.duration.get()
        year = self.year.get()
        country = self.country.get()
        director = self.director.get()
        with self.master.engine_new.connect() as conn:
            print(conn.execute(text(f'SELECT insert_film(\'{name}\','
                                    f' \'{genre}\','
                                    f'\'{duration}\'::time,'
                                    f'{year},'
                                    f'\'{country}\','
                                    f'\'{director}\')')))
            conn.commit()

        tk.messagebox.showinfo('Insert', 'OK')

        self.name.delete(0, 'end')
        self.genre.delete(0, 'end')
        self.duration.delete(0, 'end')
        self.year.delete(0, 'end')
        self.country.delete(0, 'end')
        self.director.delete(0, 'end')

        self.pack_forget()
        AdminActions(self.master).edit_films()


class SessionView(tk.Frame):
    def __init__(self, master=None, data=[]):
        super().__init__(master)
        self.pack()
        tk.Label(self, text="Session table").pack()
        tk.Button(self, text='Exit', command=lambda:
            self.pack_forget() or
            frames.EntryFrame(self.master)).pack()
        self.records_frame = tk.Frame(self)
        self.records_frame.pack(side=tk.LEFT)
        self.action_frame = tk.Frame(self)
        self.action_frame.pack(side=tk.RIGHT)
        self.insert_frame = tk.Frame(self.action_frame)
        self.insert_frame.pack(side=tk.LEFT)
        tk.Button(self.insert_frame, text='Insert', command=self.insert_record).pack()
        self.hall = tk.Entry(self.insert_frame)
        self.time = tk.Entry(self.insert_frame)
        self.selected_film = tk.StringVar(self.insert_frame)
        self.selected_cinema = tk.StringVar(self.insert_frame)
        with self.master.engine_new.connect() as conn:
            res_f = conn.execute(text('SELECT * FROM show_film()')).all()
        res = [x[1] for x in res_f]
        if len(res) == 0:
            self.pack_forget()
            tk.messagebox.showerror('Engine error', 'Theres no films or cinemas.')
            AdminActions(self.master)
            return
        self.film = tk.OptionMenu(self.insert_frame, self.selected_film, *res)
        with self.master.engine_new.connect() as conn:
            res_c = conn.execute(text('SELECT * FROM show_cinema()')).all()
        res = [x[1] for x in res_c]
        if len(res) == 0:
            self.pack_forget()
            tk.messagebox.showerror('Engine error', 'Theres no films or cinemas.')
            AdminActions(self.master)
            return
        self.cinema = tk.OptionMenu(self.insert_frame, self.selected_cinema, *res)
        tk.Label(self.insert_frame, text='Hall').pack()
        self.hall.pack()
        tk.Label(self.insert_frame, text='Time').pack()
        self.time.pack()
        tk.Label(self.insert_frame, text='Film').pack()
        self.film.pack()
        tk.Label(self.insert_frame, text='Cinema').pack()
        self.cinema.pack()
        self.delete_frame = tk.Frame(self.action_frame)
        self.delete_frame.pack(side=tk.LEFT)
        tk.Button(self.delete_frame, text='Delete', command=self.delete_record).pack()
        tk.Label(self.delete_frame, text='Delete ID').pack()
        self.deleteid = tk.Entry(self.delete_frame)
        self.deleteid.pack()
        tk.Button(self.delete_frame, text='Session info', command=self.session_info).pack()
        tk.Label(self.delete_frame, text='Info ID').pack()
        self.infoid = tk.Entry(self.delete_frame)
        self.infoid.pack()
        for rec in data:
            fr = tk.Frame(self.records_frame, borderwidth=2, relief='groove')
            fr.pack()
            l = tk.Label(fr, text=f'({rec[0]}) Hall:"{rec[1]}" at {rec[2]}')
            l.pack(side=tk.LEFT)
            print(rec[0])

    def delete_record(self):
        idx = self.deleteid.get()
        with self.master.engine_new.connect() as conn:
            print(conn.execute(text(f"SELECT delete_session({idx})")))
            conn.commit()

        tk.messagebox.showinfo('Delete', 'OK')

        self.deleteid.delete(0, 'end')

        self.pack_forget()
        AdminActions(self.master).edit_sessions()

    def session_info(self):
        idx = self.infoid.get()
        with self.master.engine_new.connect() as conn:
            info = conn.execute(text(f"SELECT * FROM find_session_by_id('{idx}')")).all()[0]
            conn.commit()
            fname = conn.execute(text(f"SELECT * FROM find_film_by_id('{info[3]}')")).all()[0][1]
            conn.commit()
            cname = conn.execute(text(f"SELECT * FROM find_cinema_by_id('{info[4]}')")).all()[0][1]
            conn.commit()
        print(fname, cname)

        tk.messagebox.showinfo("Session Info", f"Hall: {info[1]}\n"
                                               f"Time: {info[2]}\n"
                                               f"Film: {fname}\n"
                                               f"Cinema: {cname}")

    def insert_record(self):
        hall = self.hall.get()
        time = self.time.get()
        fid = self.selected_film.get()
        with self.master.engine_new.connect() as conn:
            res = conn.execute(text(f'SELECT * FROM find_by_name(\'{fid}\')')).all()
            conn.commit()
        fid = res[0][0]
        cid = self.selected_cinema.get()
        with self.master.engine_new.connect() as conn:
            res = conn.execute(text(f'SELECT * FROM find_cinema_by_name(\'{cid}\')')).all()
            conn.commit()
        cid = res[0][0]
        with self.master.engine_new.connect() as conn:
            print(conn.execute(text(f'SELECT insert_session({hall}, \'{time}\'::timestamp, {fid}, {cid})')))
            print(hall, time, fid, cid)
            conn.commit()

        tk.messagebox.showinfo('Insert', 'OK')

        self.pack_forget()
        AdminActions(self.master).edit_sessions()


class TicketView(tk.Frame):
    def __init__(self, master=None, data=[]):
        super().__init__(master)
        self.pack()
        tk.Label(self, text="Ticket table").pack()
        tk.Button(self, text='Exit', command=lambda:
            self.pack_forget() or
            frames.EntryFrame(self.master)).pack()
        self.records_frame = tk.Frame(self)
        self.records_frame.pack(side=tk.LEFT)
        self.action_frame = tk.Frame(self)
        self.action_frame.pack(side=tk.RIGHT)
        self.insert_frame = tk.Frame(self.action_frame)
        self.insert_frame.pack(side=tk.LEFT)
        tk.Button(self.insert_frame, text='Insert', command=self.insert_record).pack()
        self.seat = tk.Entry(self.insert_frame)
        self.row = tk.Entry(self.insert_frame)
        self.selected_session = tk.StringVar(self.insert_frame)
        with self.master.engine_new.connect() as conn:
            res_s = conn.execute(text('SELECT * FROM show_session()')).all()
        res = [(x[0], x[1], x[2]) for x in res_s]
        if len(res) == 0:
            self.pack_forget()
            tk.messagebox.showerror('Engine error', 'Theres no sessions.')
            AdminActions(self.master)
            return
        self.session = tk.OptionMenu(self.insert_frame, self.selected_session, *res)
        self.price = tk.Entry(self.insert_frame)
        tk.Label(self.insert_frame, text='Seat').pack()
        self.seat.pack()
        tk.Label(self.insert_frame, text='Row').pack()
        self.row.pack()
        tk.Label(self.insert_frame, text='Session').pack()
        self.session.pack()
        tk.Label(self.insert_frame, text='Price').pack()
        self.price.pack()
        self.delete_frame = tk.Frame(self.action_frame)
        self.delete_frame.pack(side=tk.LEFT)
        tk.Button(self.delete_frame, text='Delete', command=self.delete_record).pack()
        tk.Label(self.delete_frame, text='Delete ID').pack()
        self.deleteid = tk.Entry(self.delete_frame)
        self.deleteid.pack()
        tk.Button(self.delete_frame, text='Ticket info', command=self.ticket_info).pack()
        tk.Label(self.delete_frame, text='Info ID').pack()
        self.infoid = tk.Entry(self.delete_frame)
        self.infoid.pack()
        tk.Button(self.delete_frame, text='Update place', command=self.update_placement).pack()
        tk.Label(self.delete_frame, text='Update ID').pack()
        self.updid = tk.Entry(self.delete_frame)
        self.updid.pack()
        tk.Label(self.delete_frame, text='New seat and row').pack()
        self.upd_str = tk.Entry(self.delete_frame)
        self.upd_str.pack()
        for rec in data:
            fr = tk.Frame(self.records_frame, borderwidth=2, relief='groove')
            fr.pack()
            l = tk.Label(fr,
                         text=f'({rec[0]}) Seat:{rec[1]}, Row:{rec[2]}, Session:{rec[3]}, Price: {rec[4]} || {rec[5]}')
            l.pack(side=tk.LEFT)
            print(rec[0])

    def update_placement(self):
        idx = self.updid.get()
        updstring = self.upd_str.get().split(' ')
        with self.master.engine_new.connect() as conn:
            print(conn.execute(text(f"SELECT update_location({idx}, {updstring[0]}, {updstring[1]})")))
            conn.commit()

        self.pack_forget()
        AdminActions(self.master).edit_tickets()

    def delete_record(self):
        idx = self.deleteid.get()
        with self.master.engine_new.connect() as conn:
            print(conn.execute(text(f"SELECT delete_ticket({idx})")))
            conn.commit()

        tk.messagebox.showinfo('Delete', 'OK')

        self.deleteid.delete(0, 'end')

        self.pack_forget()
        AdminActions(self.master).edit_tickets()

    def ticket_info(self):
        idx = self.infoid.get()
        with self.master.engine_new.connect() as conn:
            info = conn.execute(text(f"SELECT * FROM find_ticket_by_id('{idx}')")).all()[0]
            conn.commit()
            sname = conn.execute(text(f"SELECT * FROM find_session_by_id('{info[3]}')")).all()[0]
            conn.commit()
            cinema = conn.execute(text(f'SELECT * FROM find_cinema_by_id(\'{sname[4]}\')')).all()[0][1]
            conn.commit()
        print(info, sname, cinema)

        tk.messagebox.showinfo("Ticket Info", f"Seat: {info[1]}\n"
                                              f"Row: {info[2]}\n"
                                              f"Session time: {sname[2]}\n"
                                              f"Cinema: {cinema}\n"
                                              f"Price: {info[4]}\n"
                                              f"Last ticket update: {info[5]}")

    def insert_record(self):
        seat = self.seat.get()
        row = self.row.get()
        sid = eval(self.selected_session.get())
        price = self.price.get()
        with self.master.engine_new.connect() as conn:
            res = conn.execute(text(f'SELECT insert_ticket({seat}, {row}, {sid[0]}, {price})'))
            print(res)
            conn.commit()

        tk.messagebox.showinfo('Insert', 'OK')

        self.pack_forget()
        AdminActions(self.master).edit_tickets()
