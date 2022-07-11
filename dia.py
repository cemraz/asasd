from tkinter import filedialog
import os
from exif import Image as I


from tkinter import Tk,W,E,BOTH,X,Y,Listbox,END,LEFT,RIGHT,Text,Scrollbar,TOP,CENTER,GROOVE
from tkinter.ttk import Frame,Button,Entry,Style,Label
from tkinter import *
from PIL import ImageTk,Image



class Win(Frame):
    def __init__(self):
        Frame.__init__(self)
        self.initUI()

    def open_it(self,event):
        self.path = filedialog.askdirectory()
        self.lbl_two['text'] = f'{self.path}'

    def space(self):
        self.l1 = Label(self, text='    ')
        self.l1.pack()


    ####################
    def show_image(self,path):
        img = Image.open(path)
        width = 500
        ratio = (width / float(img.size[0]))
        height = int((float(img.size[1]) * float(ratio)))
        imag = img.resize((width, height), Image.ANTIALIAS)
        image = ImageTk.PhotoImage(imag)
        panel = Label(self, image=image)
        panel.pack(side="top", fill="both", expand="no")


    def initUI(self):
        self.master.title('seventimes rutor etc.')#Имя окна
        Style().configure('TButton', padding=(0, 5, 0, 5), font='serif 10')
        self.path = None#Начальный путь

        #############################
        self.img = ImageTk.PhotoImage(Image.open('rek.jpg'))
        self.b = Label(image=self.img)
        self.b.pack()





        #Верхняя наклейка
        self.lbl_mark = Label(self, text='Введите описание и шаблон')
        self.lbl_mark.pack()

        # пространство
        self.l1 = Label(self, text='    ')
        self.l1.pack()

        #Скролбар текста
        self.scrollbar = Scrollbar(self)
        self.scrollbar.pack(side=RIGHT, fill=BOTH)

        #Создание текста
        self.tx_desc = Text(self,height=20,yscrollcommand=self.scrollbar.set)
        self.tx_desc.pack(side=TOP)

        #Присвоение скролбара тексту
        self.scrollbar.config(command=self.tx_desc.yview)

        # пространство
        self.l2 = Label(self, text='    ')
        self.l2.pack()

        #Кнопка выбора пути
        self.but_way = Button(self, text="Выберите папку")
        self.but_way.pack()
        self.but_way.bind('<Button-1>', self.open_it)

        # наклейка
        self.lbl_two = Label(self,text='путь')
        self.lbl_two.pack()

        #создание окна
        self.pack(fill=BOTH,expand=1)

        # пространство
        self.l3 = Label(self, text='    ')
        self.l3.pack()

        #кнопка перехода к след. этапу
        self.but_ok = Button(self,text='OK')
        self.but_ok.pack()
        self.but_ok.bind('<Button-1>',self.check_way)

        #наклейка вывода результата
        self.lbl_res = Label(self, text='Результат')
        self.lbl_res.pack()


    #Возврат к первому окну из второго
    def back(self,event):
        self.but_del.pack_forget()
        self.lbl_second_top.pack_forget()
        self.entry_mark_name.pack_forget()
        self.entry_mark_sum.pack_forget()
        self.but_add.pack_forget()
        self.but_del.pack_forget()
        self.but_ok.pack_forget()
        self.lbl_second_res.pack_forget()
        self.l.pack_forget()
        self.but_back.pack_forget()
        self.scrollbar.pack_forget()
        self.initUI()

    #Проверка корректности введеных данных и переход ко второму экрану
    def check_way(self,event):
        if self.path != None and self.path != '': #проверка корректности пути
            self.files = os.listdir(self.path)
            self.files = list(filter(lambda x:x.endswith('jpg') or x.endswith('png'),self.files))#Создание списка картинок
            self.lbl_res['text'] = f'Кол-во файлов в папке - {len(self.files)}'
            if len(self.files)%2==0:
                self.lbl_res['text'] = f'Кол-во jpg файлов в папке - {len(self.files)}'
                self.unvisible_lables()
                self.second_screen()
            else:
                self.lbl_res['text'] = 'В папке нечетное кол-во фото!'
        else:
            self.lbl_res['text'] = 'Выберите путь и введите кол-во цифрами'

    #Второй экран
    def second_screen(self):
        self.text = self.tx_desc.get(1.0,END)#Получение значения текст

        #создание кнопки назад
        self.but_back = Button(self, text='Назад', width=30)
        self.but_back.pack()
        self.but_back.bind('<Button-1>', self.back)

        #создание скролбара
        self.scrollbar = Scrollbar(self)
        self.scrollbar.pack(side=RIGHT, fill=BOTH)
        #создание листбокса
        self.l = Listbox(yscrollcommand=self.scrollbar.set, width=40)
        #наклейка инструкция
        self.lbl_second_top = Label(self, text='Введите значения и кол-во')
        self.lbl_second_top.pack()

        #ввод имени марк
        self.entry_mark_name = Entry(self,width=25,justify=CENTER)
        self.entry_mark_name.pack()

        #ввод кол-ва марк
        self.entry_mark_sum = Entry(self, width=5,justify=CENTER)
        self.entry_mark_sum.pack()

        #Кнопка добавить марк
        self.but_add = Button(self, text='Добавить марк',width=250)
        self.but_add.pack()
        self.but_add.bind('<Button-1>', self.add_mark)

        # Кнопка удалить марк
        self.but_del = Button(self,text='Удалить последнюю марк',width=250)
        self.but_del.pack()
        self.but_del.bind('<Button-1>',self.del_mark)

        #Кнопка завершения
        self.but_ok = Button(self, text='ok', width=10,pady=8,highlightcolor='#255',relief=GROOVE)
        self.but_ok.pack()
        self.but_ok.bind('<Button-1>', self.sec_ok)
        #Вывод резульатта
        self.lbl_second_res = Label(self, text=' ')
        self.lbl_second_res.pack()
        #Вывод листбокса и скроллбара
        self.l.pack(fill=BOTH)
        self.scrollbar.config(command=self.l.yview)

    #Добавить марк
    def add_mark(self,event):
        if self.entry_mark_name.get() !='' and self.entry_mark_sum.get() !='':
            if self.entry_mark_sum.get().isdecimal()==True:
                self.l.insert(END,self.entry_mark_name.get())
                self.l.insert(END,self.entry_mark_sum.get())

                self.lbl_second_res['text'] = f'{self.entry_mark_name.get()} добавлен в кол-ве {self.entry_mark_sum.get()}'
            else:
                self.lbl_second_res['text'] = 'Введите кол-во цифрами'
        else:
            self.lbl_second_res['text'] = 'Заполните оба поля'

    # Удалить марк
    def del_mark(self,event):
        self.l.delete(END)
        self.l.delete(END)

    def open_listbox(self):
        s_main =1
        s = 1
        print(self.d)
        self.RES = ''
        for count in range(self.l.size()+1):
            if count%2!=0:
                times = int(self.l.get(count))
                for i in range(s_main,s_main+times):
                    res = f'{i}\n{self.l.get(count-1)}\nКоордината - {self.d[i]}\nФото: \n{self.text}\n\n'+('*' * 30) + '\n\n'
#                    res = f'{i}\n' + self.l.get(count-1)  + f'Координата - {self.d[i]}\n' + self.text + '\nФото: ' + (
#                        '*' * 30) + '\n'
                    s += 1
                    self.RES += res
                s_main = s

        return self.RES


    def sec_ok(self,event):
        #Проверка кол-ва фото
        size = self.l.size()
        res=0
        for i in range(size):
            if i%2!=0:
                a = int(self.l.get(i))
                res+=a

        if (res*2) == len(self.files):
            self.RUN()

    def RUN(self):
        self.d = {}
        self.pere2()
        self.cords()
        self.zapis(self.open_listbox())

    def zapis(self,RES):
        f = open(f'{self.path}/RESULT....ЛУЧШИЕ УСЛОВИЯ RUTOR ETC.txt', 'w')
        f.write(RES)

    def pere2(self):
        '''
        Переменовыввает ВСЕ файлы в папке где лежит скрипт на 1-1(2)-2-2(2)...и тд
        :return: переименовывает все файлы
        '''
#        l = os.listdir(self.path)
#        l = list(filter(lambda x: x.endswith('jpg') or x.endswith('png'), l))
        n = 0
        i = 0
        if len(self.files) % 2 == 0:#if len(l) % 2 == 0:
            while i != len(self.files):#while i != len(l):
                n += 1
                os.replace(f'{self.path}/{self.files[i]}', f'{self.path}/{n}.jpg')#os.replace(l[i], f'{n}.jpg')
                i += 1
                os.replace(f'{self.path}/{self.files[i]}', f'{self.path}/{n} (uuu).jpg')#os.replace(l[i], f'{n} (2).jpg')
                i += 1

    def cord(self,image):
        '''
        Проверяет на наличие координаты у фото и извлекает из него координаты в виде (градусы/минуты/секунды)
        :param image: имя изображения
        :return: координаты в виде (градусы/минуты/секунды)
        '''
        img = I(image)
        if img.has_exif == True:
            m = (dir(img))
            if 'gps_latitude' in m and 'gps_longitude' in m:
                return self.dms_coordinates_to_dd_coordinates(img.get('gps_latitude'), img.get(
                    'gps_latitude_ref')), self.dms_coordinates_to_dd_coordinates(img.get('gps_longitude'),
                                                                            img.get('gps_longitude_ref'))
        res = 'Exif файл не обнаружен,проверьте фото'

    def dms_coordinates_to_dd_coordinates(self,coordinates, coordinates_ref):
        '''
        Функция перевода координат в привычный формат
        :param coordinates: координата содержащая градусы/минуты/секунды
        :param coordinates_ref:направление(N E W S)
        :return:коорд в привычном виде
        '''
        decimal_degrees = coordinates[0] + \
                          coordinates[1] / 60 + \
                          coordinates[2] / 3600

        if coordinates_ref == "S" or coordinates_ref == "W":
            decimal_degrees = -decimal_degrees

        return decimal_degrees

    def cords(self):
        '''
        соединяет координату и номер
        :return: Возвращает словарь где ключ есть номер а знгачение координата
        '''
#        global d
        l = os.listdir(self.path)
        l = list(filter(lambda x: x.endswith('jpg') or x.endswith('png'), l))
        for i in range(1, len(l) // 2 + 1):
            img = open(f'{self.path}/{i} (uuu).jpg', 'rb').name
            print(img)
            self.d[i] = self.cord(img)

    def qu(self):
        '''
        Указывается количество,дата маркировка,все это соединяется в один текст
        :return: Готово
        '''
        n = len(d)  # КОличество
        RES = ''
        for i in range(1, n + 1):
            res = f'{i}\n' + self.DATA + '\nМск.etc\n' + f'Координата - {self.d[i]}\n' + text + (
                        '*' * 30) + '\n'
            RES += res

        return RES

    #Скрыть лейблы для перехода на второй экран
    def unvisible_lables(self):
        self.lbl_res.pack_forget()
        self.but_ok.pack_forget()
        self.lbl_two.pack_forget()
        self.but_way.pack_forget()
        self.tx_desc.pack_forget()
        self.scrollbar.pack_forget()
        self.lbl_mark.pack_forget()
        self.l1.pack_forget()
        self.l2.pack_forget()
        self.l3.pack_forget()

def main():
    root = Tk()
    root.geometry('500x525')
    w =Win()
    root.mainloop()


if __name__ == '__main__':
    main()