from tkinter import *
from tkinter import ttk, font, messagebox as box
from code_dictionary import *
from xml_data import *


class MyFrame(Frame):
    def __init__(self,parent):
        self.chosenFont = font.Font(family='Verdana', size=10, weight='normal')

        Frame.__init__(self,parent,background="white")
        self.parent = parent
        self.parent.title("MediWhere")
        self.style = ttk.Style()
        self.style.theme_use("default")
        self.centreWindow()
        self.pack(fill=BOTH,expand=1)

        self.data_list = []

        self.addr1 = ''
        self.addr2 = ''
        self.addr3 = ''
        self.type = ''

        self.c_page = 1
        self.t_page = 1

        # MediWhere 상단로고
        self.logo1 = PhotoImage(file="logo1.gif")
        self.logo2 = PhotoImage(file="logo2.gif")
        self.logo_Label1 = Label(parent, image=self.logo1)
        self.logo_Label1.place(x=20, y=10)
        self.logo_Label2 = Label(parent, image=self.logo2)
        self.logo_Label2.place(x=420, y=10)

        # 시/도 라벨 표시와 입력
        sido_Label = Label(self, text="시/도", font=self.chosenFont, background='white')
        sido_Label.place(x=10,y=80)
        self.sidoVar = StringVar()
        self.sidoVar = ttk.Combobox(self, textvariable=self.sidoVar,width=9)
        self.sidoVar['values'] = list(sido_dict.keys())
        #self.sidoVar.current(0)  # 시작값지정
        self.sidoVar.bind("<<ComboboxSelected>>", self.sido_event)
        self.sidoVar.place(x=10, y=100)

        # 시/구/군 라벨 표시와 입력
        sigugun_Label = Label(self, text="시/구/군", font=self.chosenFont, background='white')
        sigugun_Label.place(x=90, y=80)
        self.sigugunVar = StringVar()
        self.sigugunVar = ttk.Combobox(self, textvariable=self.sigugunVar, width=11)
        self.sigugunVar.bind("<<ComboboxSelected>>", self.sigugun_event)
        self.sigugunVar.place(x=90, y=100)

        # 동/읍/면 라벨 표시와 입력
        dong_Label = Label(self, text="동/읍/면", font=self.chosenFont, background='white')
        dong_Label.place(x=185, y=80)
        self.dong_Text = Entry(self,width=8,borderwidth=2)
        self.dong_Text.place(x=185, y=100)

        # 병원 분류
        type_Label = Label(self,text="분류",font=self.chosenFont, background='white')
        type_Label.place(x=250,y=80)
        self.typeVar = StringVar()
        self.typeVar = ttk.Combobox(self,textvariable=self.typeVar, width=9)
        self.typeVar['values'] = list(hos_type.keys())
        self.typeVar.bind("<<ComboboxSelected>>", self.type_event)
        self.typeVar.place(x=250,y=100)

        # 검색 버튼
        search_Button = Button(self, text="검색", width=3, command=self.click_search)
        search_Button.place(x=335,y=95)

        # 검색 결과 출력 20개씩
        self.search_List = Listbox(self, width=50, height=20,borderwidth=3)
        self.search_List.place(x=10,y=140)
        self.search_List.bind("<<ListboxSelect>>", self.select)

        # 페이지표시 및 버튼
        prev_Button = Button(self, text="<<", width=3, command=self.click_prev)
        prev_Button.place(x=100, y=470)
        self.c_page_Label = None

        slash_Label = Label(self,text='/',font=self.chosenFont,background='white')
        slash_Label.place(x=180,y=470)

        self.t_page_Label = None
        next_Button = Button(self, text=">>", width=3, command=self.click_next)
        next_Button.place(x=250, y=470)

        # 북마크, 이메일 보내기 버튼
        inbookmark_Button = Button(self,text="★ 북마크담기",width=10)
        inbookmark_Button.place(x=420,y=90)

        outbookmark_Button = Button(self, text="북마크 보기", width=10)
        outbookmark_Button.place(x=510, y=90)

        email_Button = Button(self,text='Email',width=10)
        email_Button.place(x=600,y=90)


        # 정보출력 박스
        self.info_Box = StringVar()
        Label(self,textvariable=self.info_Box,width=50, height=20).place(x=420,y=140)

        #self.info_Box = Listbox(self, width=50, height=20, borderwidth=3)
        #self.info_Box.place(x=420, y=140)




    # 프로그램창 크기 및 항상 중앙에 띄우기
    def centreWindow(self):
        w = 800
        h = 550
        sw = self.parent.winfo_screenwidth()
        sh = self.parent.winfo_screenheight()
        x = (sw - w)/2
        y = (sh - h)/2
        self.parent.geometry('%dx%d+%d+%d'%(w,h,x,y))


# 이벤트 핸들
    def sido_event(self, event):
        self.addr1 = self.sidoVar.get()
        self.addr2 = ''
        self.addr3 = ''
        print(self.addr1) # .get()= 타입 반환
        self.make_sigugun()

    def sigugun_event(self, event):
        self.addr2 = self.sigugunVar.get()
        print(self.addr2)  # .get()= 타입 반환

    def dong_event(self,event):
        pass

    def type_event(self,event):
        self.type = self.typeVar.get()
        print(self.type)

    # 검색버튼 클릭시
    def click_search(self):
        # 강력하다 업데이트 ㄷㄷ
        self.update()
        self.search_List.delete(0,END) # 다시 검색시 출력박스 초기화
        self.addr3 = self.dong_Text.get()
        print(self.addr3)
        self.data_list, total = make_list(self.addr1,self.addr2,self.addr3,self.type)
        self.t_page = eval(total) // 20 + 1
        for i in self.data_list:
            self.search_List.insert(END,i.name)
        #box.showinfo("Information", "Thank you!")
        self.c_page_Label = Label(self, text=str(self.c_page), font=self.chosenFont, background='white')
        self.c_page_Label.place(x=150, y=470)
        self.t_page_Label = Label(self, text=str(self.t_page), font=self.chosenFont, background='white')
        self.t_page_Label.place(x=200, y=470)

    def click_prev(self):
        if self.c_page > 1:
            self.search_List.delete(0, END)  # 다시 검색시 출력박스 초기화
            self.c_page -= 1
            self.c_page_Label = Label(self, text=str(self.c_page), font=self.chosenFont, background='white')
            self.c_page_Label.place(x=150, y=470)
            self.data_list, total = make_list(self.addr1, self.addr2, self.addr3, self.type, self.c_page)
            self.t_page = eval(total) // 20 + 1
            for i in self.data_list:
                self.search_List.insert(END, i.name)


    def click_next(self):
        if self.c_page < self.t_page:
            self.search_List.delete(0, END)  # 다시 검색시 출력박스 초기화
            self.c_page += 1
            self.c_page_Label = Label(self, text=str(self.c_page), font=self.chosenFont, background='white')
            self.c_page_Label.place(x=150, y=470)
            self.data_list, total = make_list(self.addr1, self.addr2, self.addr3, self.type,self.c_page)
            self.t_page = eval(total) // 20 + 1
            for i in self.data_list:
                self.search_List.insert(END, i.name)


    def select(self,val):
        sender = val.widget
        idx = sender.curselection()
        value = sender.get(idx)
        for i in self.data_list:
            if value == i.name:
                print(i.name)
                self.info_Box.set(i.__str__())





    def make_sigugun(self):
        self.sigugunVar.set('')
        self.sigugunVar['values'] = list(sigugun_dict[sido_dict[self.sidoVar.get()]].keys())
        # self.sigugunVar.current(0)  # 시작값지정



def main():

    root = Tk()
    root.resizable(width=FALSE,height=FALSE)
    root.iconbitmap('MediWhere_icon.ico')

    app = MyFrame(root)

    root.mainloop()


if __name__ == '__main__':
    main()