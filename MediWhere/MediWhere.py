from tkinter import *
from tkinter import ttk, font, messagebox
from io import BytesIO
import webbrowser
from PIL import Image, ImageTk
from google_map import make_googlemap_url
from xml_data import *
import gmail


class Mediwhere(Frame):
    def __init__(self,parent):
        self.chosenFont = font.Font(family='Verdana', size=10, weight='normal')

        Frame.__init__(self,parent,background="white")
        self.parent = parent
        self.parent.title("MediWhere")
        self.style = ttk.Style()
        self.style.theme_use("default")
        self.centreWindow()
        self.pack(fill=BOTH, expand=1)

        # 0 -> 검색모드 / 1 -> 북마크모드
        self.mode = 0

        #클릭한 데이터
        self.value = ''

        self.data_list = []
        self.bookmark_list = []

        self.addr1 = ''
        self.addr2 = ''
        self.addr3 = ''
        self.type = ''
        self.url = ''

        self.map_url = ''
        self.map_image = None
        self.map_zoom = 15
        self.map_type = 'roadmap'
        self.xpos = ''
        self.ypos = ''

        self.c_page = 1
        self.t_page = 1

        self.email_address = ''

        #self.email_top.withdraw()

    # MediWhere 상단로고
        self.logo1 = PhotoImage(file="MediWhere_logo.gif")
        self.logo2 = PhotoImage(file="kpu_logo.gif")
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

    # 병원 분류 라벨 표시와 입력
        type_Label = Label(self,text="분류",font=self.chosenFont, background='white')
        type_Label.place(x=250, y=80)
        self.typeVar = StringVar()
        self.typeVar = ttk.Combobox(self,textvariable=self.typeVar, width=9)
        self.typeVar['values'] = list(hos_type.keys())
        self.typeVar.bind("<<ComboboxSelected>>", self.type_event)
        self.typeVar.place(x=250, y=100)

    # 검색 버튼
        search_Button = Button(self, text="검색", width=3, command=self.click_search)
        search_Button.place(x=335,y=95)

    # 검색 결과 출력 ( 20개씩 ) -> 북마크에도 사용해야한다
        self.search_List = Listbox(self, width=50, height=20,borderwidth=3)
        self.search_List.place(x=10,y=150)
        self.search_List.bind("<<ListboxSelect>>", self.select)

    # 페이지표시 및 버튼
        # << 버튼
        prev_Button = Button(self, text="<<", width=3, command=self.click_prev)
        prev_Button.place(x=100, y=500)

        # 현재 페이지 표시
        self.c_page_Label = Label(self, text=str(self.c_page), font=self.chosenFont, background='white')
        self.c_page_Label.pack()
        self.c_page_Label.place(x=150, y=500)

        # / 표시
        slash_Label = Label(self,text='/',font=self.chosenFont,background='white')
        slash_Label.place(x=180,y=500)

        # 총 페이지 표시
        self.t_page_Label = Label(self, text=str(self.t_page), font=self.chosenFont, background='white')
        self.t_page_Label.pack()
        self.t_page_Label.place(x=200, y=500)

        # >> 버틍
        next_Button = Button(self, text=">>", width=3, command=self.click_next)
        next_Button.place(x=240, y=500)


    # 북마크, 이메일, 홈페이지 버튼

        # 검색/북마크 전환 스위치
        self.switch = Scale(self, from_=0, to=1, orient=HORIZONTAL, resolution=1, length=80, sliderlength = 40,
                       command = self.switch_event)
        self.switch.place(x=410, y=80)

        Label(self,text=' 검 색 | 북마크').place(x=410, y=80)


        inbookmark_Button = Button(self, text="In 북마크", width=8, command=self.click_inbookmark)
        inbookmark_Button.place(x=500, y=90)

        outbookmark_Button = Button(self, text="Out 북마크", width=8, command=self.click_outbookmark)
        outbookmark_Button.place(x=570, y=90)

        # 이메일 버튼
        email_Button = Button(self, text='Email', width=8, command=self.click_email)
        email_Button.place(x=640, y=90)

        # 홈페이지 접속
        homepage_Button = Button(self,text='HomePage',width=8, command=self.click_homepage)
        homepage_Button.place(x=710, y=90)

    # 정보출력 박스
        self.info_Box = StringVar()
        info_label = Label(self, textvariable=self.info_Box, width=45, height=8, font=self.chosenFont)
        info_label.place(x=410, y=130)

    # 지도출력 박스
        self.map_label = Label(self, image=self.map_image, height=250, width=350, background='white')
        self.map_label.place(x=415, y=280)

    # @ 버튼
        mapChange_Button = Button(self,text='◎',width=1, command=self.map_change)
        mapChange_Button.place(x=775,y=280)

    # + 버튼
        zoomIn_Button = Button(self, text="+", width=1, command=self.zoom_in)
        zoomIn_Button.place(x=775, y=310)

    # - 버튼
        zoomOut_Button = Button(self, text="-", width=1, command=self.zoom_out)
        zoomOut_Button.place(x=775, y=335)



    # 프로그램창 크기 및 항상 중앙에 띄우기
    def centreWindow(self):
        w = 800
        h = 550
        sw = self.parent.winfo_screenwidth()
        sh = self.parent.winfo_screenheight()
        x = (sw - w)/2
        y = (sh - h)/2
        self.parent.geometry('%dx%d+%d+%d'%(w,h,x,y))

    # 주소 콤보박스 세팅
    def sido_event(self, event):
        self.addr1 = self.sidoVar.get()
        self.addr2 = ''
        self.addr3 = ''
        self.make_sigugun()
    def sigugun_event(self, event):
        self.addr2 = self.sigugunVar.get()
    def dong_event(self,event):
        pass
    def type_event(self,event):
        self.type = self.typeVar.get()

    # 시구군 콤보박스 리스트 생성
    def make_sigugun(self):
        self.sigugunVar.set('')
        self.sigugunVar['values'] = list(sigugun_dict[sido_dict[self.sidoVar.get()]].keys())


    # 정보들 초기화함수
    def clear_info(self):
        #########  검색했던것들 초기화 부분  ###########
        self.search_List.delete(0, END)
        self.info_Box.set('')
        self.map_image = None
        self.map_label.configure(image=self.map_image)
        self.map_label.image = self.map_image
        #############################################


    # 검색버튼 클릭시
    def click_search(self):
        self.switch.set(0)
        self.mode = 0
        self.c_page = 1
        self.clear_info()
        self.addr3 = self.dong_Text.get()
        self.data_list, total = make_list(self.addr1,self.addr2,self.addr3,self.type)
        self.t_page = eval(total) // 20 + 1
        for i in self.data_list:
            self.search_List.insert(END,i.name)
        self.c_page_Label.config(text=str(self.c_page))
        self.t_page_Label.config(text=str(self.t_page))

    # << 버튼 클릭
    def click_prev(self):
        self.clear_info()
        if self.c_page > 1 and self.mode == 0:
            self.search_List.delete(0, END)  # 다시 검색시 출력박스 초기화
            self.c_page -= 1
            self.c_page_Label.config(text=str(self.c_page))
            self.data_list, total = make_list(self.addr1, self.addr2, self.addr3, self.type, self.c_page)
            self.t_page = eval(total) // 20 + 1
            for i in self.data_list:
                self.search_List.insert(END, i.name)

    # >> 버튼 클릭
    def click_next(self):
        self.clear_info()
        if self.c_page < self.t_page and self.mode == 0:
            self.search_List.delete(0, END)  # 다시 검색시 출력박스 초기화
            self.c_page += 1
            self.c_page_Label.config(text=str(self.c_page))
            self.data_list, total = make_list(self.addr1, self.addr2, self.addr3, self.type,self.c_page)
            self.t_page = eval(total) // 20 + 1
            for i in self.data_list:
                self.search_List.insert(END, i.name)

    # 병원리스트 선택시 -> 정보와 지도 출력
    def select(self,val):
        self.update()
        sender = val.widget
        idx = sender.curselection()
        self.value = sender.get(idx)

        if self.mode == 0: # 검색모드
            for i in self.data_list:
                if self.value == i.name:
                    self.url = i.url
                    self.xpos = i.xpos
                    self.ypos = i.ypos
                    self.info_Box.set(i.__str__())
                    break

        elif self.mode == 1: # 북마크 모드
            for i in self.bookmark_list:
                if self.value == i.name:
                    self.url = i.url
                    self.xpos = i.xpos
                    self.ypos = i.ypos
                    self.info_Box.set(i.__str__())
                    break

        # 지도출력
        self.map_zoom = 15
        self.map_type = 'roadmap'
        self.map_url = make_googlemap_url((self.xpos, self.ypos),self.map_zoom,self.map_type)
        with urlopen(self.map_url) as u:
            raw_data = u.read()
        im = Image.open(BytesIO(raw_data))
        self.map_image = ImageTk.PhotoImage(im)
        self.map_label.configure(image=self.map_image)
        self.map_label.image = self.map_image

    # @버튼 클릭
    def map_change(self):
        if self.map_url != '':
            if self.map_type == 'roadmap':
                self.map_type = 'hybrid'
            elif self.map_type == 'hybrid':
                self.map_type = 'roadmap'
            self.map_url = make_googlemap_url((self.xpos, self.ypos), self.map_zoom, self.map_type)
            with urlopen(self.map_url) as u:
                raw_data = u.read()
            im = Image.open(BytesIO(raw_data))
            self.map_image = ImageTk.PhotoImage(im)
            self.map_label.configure(image=self.map_image)
            self.map_label.image = self.map_image

    # + 버튼 클릭
    def zoom_in(self):
        if self.map_zoom < 20 and self.map_url != '':
            self.map_zoom += 1
            self.map_url = make_googlemap_url((self.xpos, self.ypos), self.map_zoom,self.map_type)
            with urlopen(self.map_url) as u:
                raw_data = u.read()
            im = Image.open(BytesIO(raw_data))
            self.map_image = ImageTk.PhotoImage(im)
            self.map_label.configure(image=self.map_image)
            self.map_label.image = self.map_image

    # - 버튼 클릭
    def zoom_out(self):
        if self.map_zoom > 10 and self.map_url != '':
            self.map_zoom -= 1
            self.map_url = make_googlemap_url((self.xpos, self.ypos), self.map_zoom,self.map_type)
            with urlopen(self.map_url) as u:
                raw_data = u.read()
            im = Image.open(BytesIO(raw_data))
            self.map_image = ImageTk.PhotoImage(im)
            self.map_label.configure(image=self.map_image)
            self.map_label.image = self.map_image

    # 스위치 전환 이벤트
    def switch_event(self, event):
        if self.switch.get() == 0:  # 스위치가 검색으로 바뀔때
            self.mode = 0
            self.clear_info()
            for i in self.data_list:
                self.search_List.insert(END, i.name)
            self.c_page_Label.config(text=str(self.c_page))
            self.t_page_Label.config(text=str(self.t_page))
        elif self.switch.get() == 1:  # 스위치가 북마크로 바뀔때
            self.mode = 1
            # 북마크도 페이지 설정을 해야 할까?
            self.c_page_Label.config(text=str(1))
            self.t_page_Label.config(text=str(1))
            self.clear_info()
            # 북마크리스트 정보로 세팅
            for i in self.bookmark_list:
                self.search_List.insert(END, i.name)

    # 북마크 담기 버튼
    def click_inbookmark(self):
        if self.mode == 0 and self.value != '':
            ans = messagebox.askquestion('★북마크 담기', '"' + self.value + '"' + ' 을/를'
                                         + '\n' + '북마크에 추가 하시겠습니까?')
            if ans == 'yes':
                for i in self.data_list:
                    if self.value == i.name:
                        if i not in self.bookmark_list:
                            self.bookmark_list.append(i)
                            msg = messagebox.showinfo("★북마크","잘 담겼습니다!")
                        else:
                            msg = messagebox.showerror("★북마크", "이미 담겨 있습니다!")
                        break

    # 북마크 삭제 버튼
    def click_outbookmark(self):
        if self.mode == 1 and self.value != '':
            ans = messagebox.askquestion('★북마크 삭제', '"' + self.value + '"' + ' 을/를'
                                         + '\n' + '북마크에서 삭제 하시겠습니까?')
            if ans == 'yes':
                for i in self.bookmark_list:
                    if self.value == i.name:
                        self.bookmark_list.remove(i)
                        msg = messagebox.showinfo("★북마크","삭제 완료!")
                        break
                #print(self.bookmark_list)
                self.clear_info()
                # 북마크리스트 정보로 세팅
                for i in self.bookmark_list:
                    self.search_List.insert(END, i.name)

    # 이메일 보내기 버튼
    def click_email(self):
        # 북마크 모드에서만 보낼수 있음
        if self.mode == 1 and len(self.bookmark_list) != 0:
            ## 메일입력창 설정
            self.email_top = Toplevel(self)
            self.email_top.iconbitmap('MediWhere_icon.ico')
            self.email_Label = Label(self.email_top, text="받으실 메일 주소를 입력하세요")
            self.email_Label.place(x=10, y=10)
            self.email_entrybox = Entry(self.email_top, width=25)
            self.email_entrybox.place(x=10, y=35)
            self.email_top.geometry('%dx%d+%d+%d' % (200, 90,
                                                     (self.parent.winfo_screenwidth() - 200) / 2,
                                                     (self.parent.winfo_screenheight() - 50) / 2))

            self.email_OK = Button(self.email_top, text='확인', command=self.set_email_address)
            self.email_OK.place(x=80, y=60)

            self.email_top.deiconify()

    # 이메일 주소 입력되면 메일 보내자
    def set_email_address(self):
        self.email_address = self.email_entrybox.get()
        print(self.email_address)
        self.email_entrybox.delete(0,'end')
        self.email_top.withdraw()
        if gmail.sendMail(self.email_address, gmail.MakeHtmlDoc(self.bookmark_list)) == True:
            msg = messagebox.showinfo("EMAIL", "전송 완료!")
        else:
            msg = messagebox.showerror("EMAIL", "전송 실패!")

    # 홈페이지 접속
    def click_homepage(self):
        if self.url != '-' and self.url != '' and self.value :
            webbrowser.open_new(self.url)


######################################################
def main():
    root = Tk()
    root.resizable(width=FALSE,height=FALSE)
    root.iconbitmap('MediWhere_icon.ico')
    app = Mediwhere(root)
    root.mainloop()

######################################################

if __name__ == '__main__':
    main()