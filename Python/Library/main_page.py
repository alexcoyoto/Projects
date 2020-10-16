import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from PIL import ImageTk, Image
import re  # регулярные выражения
import winsound  # сигнал об ошибке
import mongoDB
import basics
import machine_learning

sources = "./source/images/"


# mr_snegur@hotmail.com


class Main(tk.Frame):
    # конструктор
    def __init__(self, some_root):
        super().__init__(some_root)

        self.success_label = tk.Label(root, text='', fg='#002966')
        self.main_label = tk.Label(root, text='© Все права защищены.', fg='#404040')
        self.tree = ttk.Treeview(self, columns=('id', 'book', 'author', 'price'),
                                 height=15, show='headings', selectmode='browse')

        # 64x64, colored only!!
        self.add_book_img = ImageTk.PhotoImage(Image.open(sources + "book.png"))
        self.add_user_img = ImageTk.PhotoImage(Image.open(sources + "question.png"))
        self.add_info_img = ImageTk.PhotoImage(Image.open(sources + "faq.png"))
        self.add_statistics_img = ImageTk.PhotoImage(Image.open(sources + "statistics.png"))
        self.add_transfer_img = ImageTk.PhotoImage(Image.open(sources + "coins.png"))

        self.toolbar = tk.Frame(bg="#d7d8e0", bd=2)
        self.account_button = tk.Button(self.toolbar, text='Войти', command=self.open_account,
                                        bg='#d7d8e0', bd=0, compound=tk.TOP, image=self.add_user_img)
        self.catalog_button = tk.Button(self.toolbar, text='Добавить книгу', command=self.open_catalog, bg='#d7d8e0',
                                        bd=0, compound=tk.TOP, image=self.add_book_img)
        self.info_button = tk.Button(self.toolbar, text='FAQ', command=self.open_info,
                                     bg='#d7d8e0', bd=0, compound=tk.TOP, image=self.add_info_img)
        self.statistics_button = tk.Button(self.toolbar, text='Статистика', command=self.open_statistics, bg='#d7d8e0',
                                           bd=0, compound=tk.TOP, image=self.add_statistics_img)
        self.transfer_button = tk.Button(self.toolbar, text='Перевод', command=self.open_transfer, bg='#d7d8e0',
                                         bd=0, compound=tk.TOP, image=self.add_transfer_img)

        self.init_main()
        self.db = db  # для обращения к методам из DataBase
        self.current_user = current_user  # для получения информации из класса User
        self.current_statistics = current_statistics  # для получения информации из класса Statistics

    # хранит и инициализирует все объекты графического интерфейса
    def init_main(self):
        self.create_toolbar()
        self.create_tree()
        self.main_label.place(x=490, y=422)
        self.success_label.place(x=5, y=422)
        self.main_label.bind('<Double-3>', self.easter_egg)

        self.load_statistics()

    def create_toolbar(self):
        self.toolbar.pack(side=tk.TOP, fill=tk.X)

        self.catalog_button.pack(side=tk.LEFT)
        self.account_button.pack(side=tk.RIGHT)
        self.info_button.pack(side=tk.LEFT)

    def create_tree(self):
        # создание таблицы на главной
        self.tree.column('id', width=30, anchor=tk.CENTER)
        self.tree.column('book', width=300, anchor=tk.CENTER)
        self.tree.column('author', width=200, anchor=tk.CENTER)
        self.tree.column('price', width=100, anchor=tk.CENTER)

        self.tree.heading('id', text='ID')
        self.tree.heading('book', text='Книга')
        self.tree.heading('author', text='Автор')
        self.tree.heading('price', text='Цена')

        scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.tree.yview)
        self.tree.pack(side='left')  # отображение таблицы
        scrollbar.pack(side='right', fill='y')
        self.tree.configure(yscroll=scrollbar.set)

    def update_(self):
        # обновление иконки toolbar
        self.toolbar_update()
        # обновление списка покупок
        self.list_update()
        # обновление иконки в toolbar
        self.statistics_update()

    def toolbar_update(self):
        self.add_user_img = ImageTk.PhotoImage(Image.open(sources + current_user.image))
        self.account_button.config(image=self.add_user_img, text=current_user.name)

    def list_update(self):
        ids = ''
        for row in db.pop('users'):
            if row['_id'] == current_user.user_id:
                ids = row['books'].split(';')
        self.tree.delete(*self.tree.get_children())
        if ids == '':
            return
        for i in range(len(ids) - 1):
            for row in db.pop('books'):
                if row['_id'] == int(ids[i]):
                    self.tree.insert('', 'end', values=(str(row["_id"]), row['name'], row['author'], str(row['price'])),
                                     tags=('ttk', 'simple'))

    def statistics_update(self):
        if current_user.user_id == 1:
            self.transfer_button.pack(side=tk.RIGHT)
            self.statistics_button.pack(side=tk.RIGHT)
        else:
            self.transfer_button.pack_forget()
            self.statistics_button.pack_forget()

    @staticmethod
    def load_statistics():
        for row in db.pop('statistics'):
            if row['_id'] == current_statistics.info_id:
                current_statistics.set(row['_id'], row['downloads'], row['users'], row['money'])

    # mr_snegur@hotmail.com
    @staticmethod
    def easter_egg(self):
        messagebox.showinfo('', 'made by Alexander Snehur in 2019')

    @staticmethod
    def open_catalog():
        Catalog()

    @staticmethod
    def open_account():
        Account()

    @staticmethod
    def open_info():
        Info()

    @staticmethod
    def open_statistics():
        basics.Strategy.analyze(current_statistics.total_earned)    # реализация паттерна
        messagebox.showinfo('Cтатистика', 'Общее число пользователей: ' + str(current_statistics.total_users) +
                            '\n\nОбщее количесвто скачиваний: ' + str(current_statistics.total_downloads) +
                            '\n\nЧисло заработанных денег: ' + str(current_statistics.total_earned))

    @staticmethod
    def open_transfer():
        Transfer()


##########


# Наследование от класса создания окон
class Catalog(tk.Toplevel):
    def __init__(self):
        super().__init__(root)

        self.btn_cancel = ttk.Button(self, text='Закрыть', command=self.destroy)
        self.coins_label = tk.Label(self, text='Коины:')
        self.coins_number = tk.Label(self, text=str(current_user.coins), fg='#003399')
        self.error_label = tk.Label(self)

        self.catalog_tree = ttk.Treeview(self, columns=('id', 'book', 'author', 'price'),
                                         height=15, show='headings', selectmode='browse')
        self.init_catalog()

    def init_catalog(self):
        self.title('Каталог книг')
        self.geometry('650x360')
        self.resizable(False, False)

        app.success_label.config(text='')
        self.db_info()

        self.grab_set()
        self.focus_set()

    def db_info(self):
        # вывод полей
        self.catalog_tree.column('id', width=30, anchor=tk.CENTER)
        self.catalog_tree.column('book', width=250, anchor=tk.CENTER)
        self.catalog_tree.column('author', width=250, anchor=tk.CENTER)
        self.catalog_tree.column('price', width=100, anchor=tk.CENTER)

        self.catalog_tree.heading('id', text='ID')
        self.catalog_tree.heading('book', text='Книга')
        self.catalog_tree.heading('author', text='Автор')
        self.catalog_tree.heading('price', text='Цена')

        for row in db.pop('books'):
            self.catalog_tree.insert('', 'end', values=(str(row["_id"]), row['name'], row['author'], str(row['price'])),
                                     tags=('ttk', 'simple'))

        self.catalog_tree.bind('<Double-1>', self.item_clicked)

        scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.catalog_tree.yview)
        self.catalog_tree.config(yscrollcommand=scrollbar.set)
        self.catalog_tree.grid(row=0, column=0)
        scrollbar.grid(row=0, column=1, sticky='ns')

        self.btn_cancel.place(x=570, y=330)

        self.coins_label.place(x=495, y=333)
        self.coins_number.place(x=540, y=333)
        self.error_label.place(x=5, y=333)

    def item_clicked(self, event):
        if current_user.user_id == 0:
            self.error_label.config(text='ДЛЯ БРОНИРОВАНИЯ ЗАЙДИТЕ В АККАУНТ', fg='#cc0000')
            winsound.Beep(300, 200)
            winsound.Beep(250, 200)
            return

        item = self.catalog_tree.selection()

        if current_user.coins < int(self.catalog_tree.item(item, "values")[3]):
            self.error_label.config(text='ОШИБКА. НЕДОСТАТОЧНО СРЕДСТВ', fg='#cc0000')
            winsound.Beep(300, 200)
            winsound.Beep(250, 200)
            return

        self.buy(item)
        self.coins_number.config(text=str(current_user.coins))

    def buy(self, item):
        # проверка на наличие выбранной книги
        ids = ''
        for row in db.pop('users'):
            if row['_id'] == current_user.user_id:
                ids = row['books'].split(';')
        for row in db.pop('users'):
            if row['_id'] == current_user.user_id:
                for i in ids:
                    if i == self.catalog_tree.item(item, "values")[0]:
                        self.error_label.config(text='У ВАС УЖЕ ЕСТЬ ТАКАЯ КНИГА', fg='#002966')
                        winsound.Beep(300, 200)
                        return
        print("you clicked on", self.catalog_tree.item(item, "values")[0])

        for row in db.pop('users'):
            if row['_id'] == current_user.user_id:
                temp_str = row['books']
                db.update_one('users', {'_id': row['_id']}, {"$set": dict(
                    books=temp_str + self.catalog_tree.item(item, "values")[0] + ';')})
                db.update_one('users', {'_id': row['_id']}, {"$set": dict(
                    coins=row['coins'] - int(self.catalog_tree.item(item, "values")[3]))})
                self.update_statistics(int(self.catalog_tree.item(item, "values")[3]))

        for row in db.pop('users'):
            if row['_id'] == current_user.user_id:
                current_user.coins = row['coins']
                current_user.books = row['books']
        app.update_()
        # self.destroy()

    @staticmethod
    def update_statistics(book_price):
        # добавление скачивания книги
        for row in db.pop('statistics'):
            if row['_id'] == current_statistics.info_id:
                db.update_one('statistics', {'_id': row['_id']}, {"$set": {'downloads': row['downloads'] + 1}})
        for row in db.pop('statistics'):
            if row['_id'] == current_statistics.info_id:
                current_statistics.total_downloads = row['downloads']

        # определение общей стоимости
        for row in db.pop('statistics'):
            if row['_id'] == current_statistics.info_id:
                db.update_one('statistics', {'_id': row['_id']}, {"$set": {'money': row['money'] + book_price}})
        for row in db.pop('statistics'):
            if row['_id'] == current_statistics.info_id:
                current_statistics.total_earned = row['money']


##########


class Account(tk.Toplevel):
    def __init__(self):
        super().__init__(root)

        self.account_name_label = tk.Label(self, text='Имя:')
        self.account_name = tk.Label(self, text=current_user.name)

        self.account_email_label = tk.Label(self, text='Email:')
        self.account_email = tk.Label(self, text=current_user.email)

        self.account_coins_label = tk.Label(self, text='Коины:')
        self.account_coins = tk.Label(self, text=str(current_user.coins))

        self.account_photo_label = tk.Label(self, text='Фото:')
        self.photo_list = ttk.Combobox(self, values=['boy.png', 'man.png', 'girl.png', 'woman.png', 'cat.png'],
                                       state='readonly')

        self.add_user_img = ImageTk.PhotoImage(Image.open(sources + current_user.image))
        self.account_photo = tk.Label(self, image=self.add_user_img)
        self.exit_button = ttk.Button(self, text='Выйти')
        self.save_button = ttk.Button(self, text='Применить')

        ##########

        self.description = tk.Label(self, text="Войдите в систему")
        self.login_button = ttk.Button(self, text='Войти')
        self.register_button = ttk.Button(self, text='Создать')
        self.email_label = tk.Label(self, text="Email:")
        self.pass_label = tk.Label(self, text="Пароль:")
        self.entry_email = ttk.Entry(self)
        self.entry_pass = ttk.Entry(self, show="●")

        app.success_label.config(text='')

        if current_user.user_id == 0:
            self.login_account()
        else:
            self.show_account()

    def show_account(self):
        self.title('Аккаунт')
        self.geometry('205x260+400+200')
        self.resizable(False, False)

        self.account_photo.place(x=102, y=60, anchor='center')

        self.account_name_label.place(x=5, y=110)
        self.account_name.place(x=55, y=110)

        self.account_email_label.place(x=5, y=140)
        self.account_email.place(x=55, y=140)

        self.account_coins_label.place(x=5, y=170)
        self.account_coins.place(x=55, y=170)

        self.account_photo_label.place(x=5, y=200)
        self.photo_list.set(current_user.image)
        self.photo_list.place(x=55, y=200)
        self.photo_list.bind("<<ComboboxSelected>>", self.change_photo)

        self.exit_button.place(x=5, y=230)
        self.exit_button.bind('<Button-1>', self.exit_account)
        self.save_button.place(x=124, y=230)
        self.save_button.bind('<Button-1>', self.save_account)

        self.grab_set()
        self.focus_set()

    def change_photo(self, event):
        self.add_user_img = ImageTk.PhotoImage(Image.open(sources + self.photo_list.get()))
        self.account_photo.config(image=self.add_user_img)

    def save_account(self, event):
        current_user.image = self.photo_list.get()
        for row in db.pop('users'):
            if row['_id'] == current_user.user_id:
                db.update_one('users', {'_id': row['_id']}, {"$set": {'image': current_user.image}})
        app.update_()
        self.destroy()

    def exit_account(self, event):
        winsound.Beep(450, 200)
        winsound.Beep(300, 200)
        current_user.set(0, 'unknown', '123', 'unknown@gmail.com', '', 0, 'question.png')
        app.update_()
        self.destroy()

    ###########

    def login_account(self):
        self.title('Аккаунт')
        self.geometry('200x170+400+250')
        self.resizable(False, False)

        self.description.place(x=45, y=5)

        self.email_label.place(x=0, y=50)
        self.entry_email.place(x=60, y=50)
        self.entry_email.insert(0, 'test@mail.com')

        self.pass_label.place(x=0, y=100)
        self.entry_pass.place(x=60, y=100)
        self.entry_pass.insert(0, '123')

        self.login_button.place(x=5, y=140)
        self.login_button.bind('<Button-1>', self.log_in)
        self.register_button.place(x=120, y=140)
        self.register_button.bind('<Button-1>', self.sing_in)

        self.grab_set()
        self.focus_set()

    def log_in(self, event):
        for row in db.pop('users'):
            if row['email'] == self.entry_email.get() and row['password'] == self.entry_pass.get():
                current_user.set(row['_id'], row['name'], row['password'], row['email'],
                                 row['books'], row['coins'], row['image'])
                break

        if current_user.user_id == 0:
            messagebox.showerror("Title", "Неверная почта или пароль")
        else:
            self.hello_user()
            app.update_()
            self.destroy()

    @staticmethod
    def hello_user():
        if current_user.books != '':
            app.success_label.config(text='Добро пожаловать, ' +
                                          machine_learning.prediction(current_user.books, current_user.image) + ' ^_^')
        else:
            app.success_label.config(text='Добро пожаловать, ' + current_user.name)
        winsound.Beep(300, 200)
        winsound.Beep(450, 200)

    def sing_in(self, event):
        Registration()
        self.destroy()


##########


class Registration(tk.Toplevel):
    def __init__(self):
        super().__init__(root)

        self.description = tk.Label(self, text=' ')
        self.register_button = ttk.Button(self, text='Создать')
        self.name_label = tk.Label(self, text="Имя:")
        self.pass_label = tk.Label(self, text="Пароль:")
        self.pass_label2 = tk.Label(self, text="Повторите пароль:")
        self.email_label = tk.Label(self, text="e-mail:")
        self.entry_name = ttk.Entry(self)
        self.entry_pass = ttk.Entry(self, show="●")
        self.entry_pass2 = ttk.Entry(self, show="●")
        self.entry_email = ttk.Entry(self)

        self.init_registration()

    def init_registration(self):
        self.title('Регистрация')
        self.geometry('260x280+400+200')
        self.resizable(False, False)

        app.success_label.config(text='')
        self.registration()

        self.grab_set()
        self.focus_set()

    def registration(self):
        self.description.place(x=55, y=5)

        self.name_label.place(x=0, y=50)
        self.entry_name.place(x=120, y=50)

        self.pass_label.place(x=0, y=100)
        self.entry_pass.place(x=120, y=100)
        self.pass_label2.place(x=0, y=150)
        self.entry_pass2.place(x=120, y=150)

        self.email_label.place(x=0, y=200)
        self.entry_email.place(x=120, y=200)

        self.register_button.place(x=170, y=240)
        self.register_button.bind('<Button-1>', self.sing_in)

        self.grab_set()
        self.focus_set()

    def sing_in(self, event):
        if self.entry_name.get() == '' or self.entry_pass.get() == '' or self.entry_email.get() == '':
            self.description.config(text='Присутствуют пустые поля', fg='red', anchor='center')
            self.pass_label2.config(fg='black')
            self.email_label.config(fg='black')
            return

        is_valid = re.findall('(^|\s)[-a-z0-9_.]+@([-a-z0-9]+\.)+[a-z]{2,6}(\s|$)', self.entry_email.get())
        if not is_valid:
            self.description.config(text='Неверный формат почты', fg='red', anchor='center')
            self.pass_label2.config(fg='black')
            self.email_label.config(fg='red')
            return

        counter = 1
        is_exist = True
        if self.entry_pass.get() == self.entry_pass2.get():
            for row in db.pop('users'):
                counter += 1
                if row['email'] == self.entry_email.get():
                    self.description.config(text='Эта почта уже занята', fg='red', anchor='center')
                    self.email_label.config(fg='red')
                    self.pass_label2.config(fg='black')
                    is_exist = False
                    pass
            if is_exist:
                db.add('users', {'_id': counter, 'name': self.entry_name.get(), 'password': self.entry_pass.get(),
                                 'email': self.entry_email.get(), 'books': '', 'coins': 20, 'image': 'boy.png'})
                current_user.set(counter, self.entry_name.get(), self.entry_pass.get(), self.entry_email.get(),
                                 '', 20, 'boy.png')
                self.update_users_statistics()
                app.update_()
                self.destroy()
        else:
            self.description.config(text='Пароли не сопадают', fg='red', anchor='center')
            self.pass_label2.config(fg='red')
            self.email_label.config(fg='black')

    @staticmethod
    def update_users_statistics():
        for row in db.pop('statistics'):
            if row['_id'] == current_statistics.info_id:
                db.update_one('statistics', {'_id': row['_id']}, {"$set": {'users': row['users'] + 1}})
        for row in db.pop('statistics'):
            if row['_id'] == current_statistics.info_id:
                current_statistics.total_users = row['users']


##########


class Info(tk.Toplevel):
    def __init__(self):
        super().__init__(root)

        self.textBox = tk.Text(self)

        self.init_info()

    def init_info(self):
        self.title('Что это?')
        self.geometry('600x400+350+100')
        self.resizable(False, False)

        app.success_label.config(text='')
        self.show_info()

        self.grab_set()
        self.focus_set()

    def show_info(self):
        description = open('./source/information.txt', 'r')

        scrollbar = ttk.Scrollbar(self)
        scrollbar.pack(side='right', fill='y')
        self.textBox.pack(side='left', fill='y')
        scrollbar.config(command=self.textBox.yview)
        self.textBox.config(yscrollcommand=scrollbar.set)

        self.textBox.insert(tk.INSERT, description.read())

        self.textBox.configure(font=("Comic Sans MS", 10))
        self.textBox.tag_add('title', 1.0, '1.end')
        self.textBox.tag_config('title', font=("Comic Sans MS", 16), justify=tk.CENTER)

        self.textBox.config(state='disabled')


##########


class Transfer(tk.Toplevel):
    def __init__(self):
        super().__init__(root)

        self.users_list_label = tk.Label(self, text='Кому:')
        self.value_label = tk.Label(self, text='Сколько:')
        self.error_label = tk.Label(self, fg='red', anchor='center')

        self.users_list = ttk.Combobox(self, state='readonly')
        self.enter_value = ttk.Entry(self)

        self.transfer_button = ttk.Button(self, text='Перевести')

        self.init_transfers()

    def init_transfers(self):
        self.title('Перевод')
        self.geometry('220x140+400+250')
        self.resizable(False, False)

        app.success_label.config(text='')
        self.create_transfer()

        self.grab_set()
        self.focus_set()

    def create_transfer(self):
        app.success_label.pack_forget()
        self.users_list_label.place(x=5, y=15)
        self.value_label.place(x=5, y=55)
        self.error_label.place(x=25, y=85)

        user_list = ''
        for row in db.pop('users'):
            if row['_id'] != 1:
                user_list += row['email'] + ' '
        self.users_list.config(values=user_list.split())
        self.users_list.current(0)

        self.users_list.place(x=45, y=15)
        self.enter_value.place(x=65, y=55)

        self.transfer_button.place(x=75, y=110)
        self.transfer_button.bind('<Button-1>', self.transfer)

    def transfer(self, user):
        try:
            int(self.enter_value.get())
        except ValueError:
            self.error_label.config(text='НЕВЕРНЫЙ ФОРМАТ ВВОДА', anchor='center')
            self.value_label.config(fg='#cc0000')
            return

        if int(self.enter_value.get()) >= 50 or int(self.enter_value.get()) <= 0:
            self.error_label.config(text='ИНТЕРВАЛ ЗНАЧЕНИЙ: 0<x<50', anchor='center')
            self.value_label.config(fg='#cc0000')
            return

        for row in db.pop('users'):
            if row['email'] == self.users_list.get():
                db.update_one('users', {'email': row['email']}, {"$set": dict(
                    coins=row['coins'] + int(self.enter_value.get()))})
        app.success_label.config(text='ОПЕРАЦИЯ ПРОШЛА УСПЕШНО')
        winsound.Beep(300, 200)
        self.destroy()


##########


if __name__ == "__main__":
    root = tk.Tk()
    db = mongoDB.DataBase()  # объект класса базы данных
    current_user = basics.User()  # объект для хранения информации о текущем пользователе
    current_statistics = basics.Statistics()  # объект для хранения и изменения статистики
    app = Main(root)
    app.pack()
    root.title("Pocket Library")
    root.geometry("650x450+300+200")
    root.resizable(False, False)
    root.mainloop()
