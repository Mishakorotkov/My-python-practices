from tkcalendar import Calendar, DateEntry
from tkinter import *
import sqlite3
import datetime

class Calend:
    def __init__(self):
        self.top = Tk()
        self.today = datetime.date.today()
        
        self.mindate = datetime.date(year=2020, month=8, day=1)
        self.maxdate = self.today + datetime.timedelta(weeks=130)


        self.cal = Calendar(self.top, font="Arial 14", selectmode='day', locale='ru_RU',
                           mindate=self.mindate,
                           cursor="hand1", year=self.today.year, month=self.today.month, day=self.today.day)
        self.cal.pack(fill="both", expand=True)
        self.x = Button(self.top, text="запланировать", command=self.print_sel)
        self.b_vip_dela = Button(text = "выполненные дела")
        self.b_vip_dela.bind('<Button-1>', self.list_vd)
        self.x.pack()
        self.b_vip_dela.pack()
        self.sqlite_connection = sqlite3.connect("plan.db")
        self.cursor = self.sqlite_connection.cursor()
    def print_sel(self):
        try:
            self.root.destroy()
        except:
            pass
            
        self.sqlite_create_table_query = '''CREATE TABLE IF NOT EXISTS table_name (
                                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                                            date TEXT NOT NULL,
                                            text TEXT,
                                            complete INT
                                            );'''
        self.cursor.execute(self.sqlite_create_table_query)
        self.sqlite_connection.commit()
        self.sql = "SELECT text FROM table_name WHERE date=? AND complete = ?"
        self.root = Tk()
        self.t = Text(self.root, width = 100, height = 6)
        self.b1 = Button(self.root, text = "добавить")
        self.b2 = Button(self.root, text = "закрыть",
                          bg='#ba0000')
        self.b_list_del = Button(self.root, text = "выполнено")
        self.d = self.cal.selection_get()
        self.lbox = Listbox(self.root, width = 60, height = 25, selectmode=EXTENDED)
        self.cursor.execute(self.sql, [self.d, 0])
        self.a = self.cursor.fetchall()
        self.cal.see(datetime.date(year=self.today.year, month=self.today.month, day=self.today.day))
        for i in self.a:
            self.lbox.insert(0, str(self.d) + " - " + i[0])
        self.b1.bind('<Button-1>', self.save_t)
        self.b2.bind('<Button-1>', self.del_r)
        self.b_list_del.bind('<Button-1>', self.list_del)
        self.t.pack()
        self.b1.pack()
        self.b2.place(relx=0.933, rely=0.955)
        self.b_list_del.pack()
        self.lbox.pack()
    def save_t(self, event):
        self.te = self.t.get(1.0, END)[:-1]
        if len(self.te) == 0:
            return
        else:
            self.sql = "INSERT INTO table_name (date, text, complete) VALUES (?, ?, ?);"
            self.cursor.execute(self.sql, [self.d, self.te, 0])
            self.lbox.insert(0, str(self.d) + " - " + self.te)
            #self.update = "UPDATE table_name SET text = ? WHERE text = ?"
            #self.cursor.execute(self.update, [self.te, self.a[0][0]])
        self.t.delete(1.0, END)
        self.sqlite_connection.commit()
    def del_r(self, event):
        self.root.destroy()
    def list_del(self, event):
        self.select = list(self.lbox.curselection())
        self.select.reverse()
        self.sql2 = 'UPDATE table_name SET complete = ? WHERE text = ?'
        for i in self.select:
            self.nep = self.lbox.get(i)
            self.nep = self.nep[13:]
            self.lbox.delete(i)
            self.cursor.execute(self.sql2, [1, self.nep])
        self.sqlite_connection.commit()
    def list_vd(self, event):
        try:
            self.root_vd.destroy()
        except:
            pass
        self.d = self.cal.selection_get()
        self.root_vd = Tk()
        self.vd_lbox = Listbox(self.root_vd, width = 60, height = 25, selectmode=EXTENDED)
        self.vd_lbox.pack()
        self.sin = "SELECT text FROM table_name WHERE date=? AND complete = ?"
        self.cursor.execute(self.sin, [self.d, 1])
        self.cur = self.cursor.fetchall()
        for ab in self.cur:
            self.vd_lbox.insert(0, str(self.d) + " - " + ab[0])
app = Calend()
app.top.mainloop()


