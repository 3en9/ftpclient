from tkinter import *
from tkinter import filedialog as fd
import tkinter.ttk as ttk
from ftplib import FTP
import os
import threading
import random
import string


def connect(ip, login, psw, port=21):
    ftp = FTP(ip)
    ftp.login(login, psw)
    ftp.cwd('public_html')
    return ftp


a = ''
directory = os.getcwd()


def clicking():
    threading.Thread(target=click).start()


def click(f=0):
    # 0 - обычное подключение
    pb['value'] = 10
    box.delete(0, 'end')
    if f == 0:
        logout(0)
    elif f == 1:
        logout(3)
    elif f == -1:
        pass
    global a
    ip = ent1.get().strip()
    user = ent2.get().strip()
    psw = ent3.get().strip()
    host = ent4.get().strip()
    try:
        pb['value'] = 20
        a = connect(ip, user, psw, host)
        sp = a.nlst()[2:]
        pb['value'] = 40
        for i in range(len(sp)):
            size = a.size(sp[i])
            box.insert(END, sp[i] + "  {} kb".format(size))
        pb['value'] = 60
        b1 = Button(text="Загрузить файл на сервер", command=allfileing)
        b1.place(x=650, y=75)
        b2 = Button(text="Удалить", command=deleting)
        b2.place(x=650, y=200)
        b3 = Button(text="Скачать файл", command=downloading_file)
        b3.place(x=650, y=230)
        b4 = Button(text='Прочитать файл', command=reading_file)
        b4.place(x=650, y=260)
        pb['value'] = 80
        if f == 0:
            log.insert(END, 'Поключение к {} успешно выполнено\n'.format(ip))
    except:
        logout(1)
    pb['value'] = 100


def deleting():
    threading.Thread(target=delete).start()


def delete():
    pb['value'] = 10
    sel = list(box.curselection())
    if len(sel) != 0:
        sel.reverse()
        pb['value'] = 30
        for i in sel:
            try:
                a.delete(box.get(i).split(' ')[0])
                pb['value'] = 60
                box.delete(i)
                logout(5)
            except:
                click(-1)
                a.delete(box.get(i).split(' ')[0])
                pb['value'] = 60
                box.delete(i)
                logout(5)
    else:
        logout(2)
    pb['value'] = 100


def downloading_file():
    threading.Thread(target=download_file).start()


def download_file():
    sel = list(box.curselection())
    sel.reverse()
    if len(sel) != 0:
        pb['value'] = 10
        for i in sel:
            file_name = box.get(i).split()[0]
            pb['value'] = 20
            try:
                a.retrbinary("RETR " + file_name, open(file_name, 'wb').write)
                pb['value'] = 80
                logout(7)
            except:
                click(-1)
                pb['value'] = 80
                a.retrbinary("RETR " + file_name, open(file_name, 'wb').write)
                pb['value'] = 90
                logout(7)
            pb['value'] = 100
    else:
        pb['value'] = 0
        logout(13)


def reading_file():
    threading.Thread(target=read_file).start()


def read_file():
    sel = list(box.curselection())
    sel.reverse()
    if len(sel) == 0:
        logout(10)
    elif len(sel) > 1:
        logout(11)
    else:
        pb['value'] = 10
        file_name = box.get(sel[0]).split()[0]
        file_randomname = (''.join([random.choice(string.ascii_lowercase) for _ in range(16)])) + '.' + \
                          file_name.split('.')[1]
        pb['value'] = 20
        try:
            a.retrbinary("RETR " + file_name, open(file_randomname, 'wb').write)
            pb['value'] = 40
            logout(12)
            top = Toplevel()
            read_txt = Text(top)
            read_txt.insert(END, open(file_randomname, 'r').read())
            read_txt.place(x=0, y=0)
            top.title(file_name)
            top.geometry('400x300')
            top.transient()
            pb['value'] = 60
            path = os.path.join(os.path.abspath(os.path.dirname(__file__)), file_randomname)
            os.remove(path)
            pb['value'] = 80
        except:
            click(-1)
            a.retrbinary("RETR " + file_name, open(file_randomname, 'wb').write)
            pb['value'] = 40
            logout(12)
            top = Toplevel()
            read_txt = Text(top)
            read_txt.insert(END, open(file_randomname, 'r').read())
            read_txt.place(x=0, y=0)
            top.title(file_name)
            top.geometry('400x300')
            top.transient()
            pb['value'] = 60
            path = os.path.join(os.path.abspath(os.path.dirname(__file__)), file_randomname)
            os.remove(path)
            pb['value'] = 80
        pb['value'] = 100


def allfileing():
    threading.Thread(target=allfiles).start()


def allfiles():
    file_name = fd.askopenfilename()
    tmp = 0
    if file_name != '':
        pb['value'] = 10
        f = open(file_name, 'rb')
        file_name1 = file_name.split('/')[-1]
        try:
            pb['value'] = 20
            a.storbinary('STOR ' + file_name1, f)
            pb['value'] = 60
            tmp = 1
        except:
            logout(4)
        if tmp == 1:
            pb['value'] = 80
            click(1)
            pb['value'] = 100


'''
def get_connect():
    f = open('1.txt','r')
    a = f.read().split('\n')
    return a
'''


def logout(n):
    if n == 0:
        log.insert(END, 'Подключение...\n')
    if n == 1:
        log.insert(END, 'Возникла ошибка. Повторите подключение снова.\n')
        log.insert(END,
                   'Возможно, введенные вами данные некоректны, произошла ошибка на сервере или у вас возникли проблемы с интернетом\n')
    if n == 2:
        log.insert(END, 'Выберите файл для удаления\n')
    if n == 3:
        log.insert(END, 'Загрузка файла успешно завершена\n')
    if n == 4:
        log.insert(END, 'Загрузка файла не была успешна завершена\n')
    if n == 5:
        log.insert(END, 'Удаление файла успешно завершено\n')
    if n == 6:
        log.insert(END, 'Удаление файло не было успешно завершено\n')
    if n == 7:
        log.insert(END, 'Скачивание файла успешно завершено\n')
    if n == 8:
        log.insert(END, 'При скачивание файла возникла неизвестная ошибка\n')
    if n == 9:
        log.insert(END, 'Выберите файл для удаления\n')
    if n == 10:
        log.insert(END, 'Выберите файл для чтения\n')
    if n == 11:
        log.insert(END, 'Выберите ОДИН файл для чтения\n')
    if n == 12:
        log.insert(END, 'Файл успешно прочитан\n')
    if n == 13:
        log.insert(END, 'Выберите файл для скачивания\n')


root = Tk()
root.geometry('1280x720')

pb = ttk.Progressbar(length=250, mode="determinate")
pb.place(x=75, y=250)

lbl1 = Label(text='Хост', font=18)
lbl1.place(x=5, y=5)
ent1 = Entry(font=18)
# ent1.insert(0,get_connect()[0])
ent1.place(x=50, y=5)

lbl2 = Label(text='Имя пользователя', font=18)
lbl2.place(x=245, y=5)
ent2 = Entry(font=18)
# ent2.insert(0,get_connect()[1])
ent2.place(x=395, y=5)

lbl3 = Label(text='Пароль', font=18)
lbl3.place(x=590, y=5)
ent3 = Entry(font=18)
# ent3.insert(0,get_connect()[2])
ent3.place(x=655, y=5)

lbl4 = Label(text='Порт', font=18)
lbl4.place(x=850, y=5)
ent4 = Entry(font=18)
# ent4.insert(0,get_connect()[3])
ent4.place(x=895, y=5)

btn = Button(text=' Подключиться ', font=18, command=clicking)
btn.place(x=1100, y=5)

box = Listbox(selectmode=EXTENDED, width=45, height=35, font=18)
box.place(x=817, y=50)

log = Text(wrap=WORD)
log.place(x=0, y=330)

root.title('FTP_Client')
root.mainloop()
