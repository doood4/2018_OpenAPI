from tkinter import *
from tkinter import font
import tkinter.messagebox

g_tk = Tk()
g_tk.title("MediWhere")
g_tk.geometry("800x700+350+50")

# 프로그램 선 프레임
w = Canvas(g_tk,width =800, height = 700)
w.pack()
w.create_line(20,80,780,80)
w.create_line(400,100,400,680)

# MediWhere 상단로고
logo = PhotoImage(file = "MediWhere_Logo2.gif")
logo_Label = Label(g_tk,image=logo)
logo_Label.place(x=50,y=10)


RenderText = None
searchListBox = None

def initTopText():
    TempFont = font.Font(g_tk,size=20,weight='bold',family = 'Consolas')
    maintext = Label(g_tk,font=TempFont,text="[헬로우 헬로우]")
    maintext.pack()
    maintext.place(x=100)

def initSearchListBox():
    global searchListBox
    ListBoxScollbar = Scrollbar(g_tk)
    ListBoxScollbar.pack()
    ListBoxScollbar.place(x=150,y=100)

    TempFont = font.Font(g_tk,size=5,weight='bold',family='Consolas')
    searchListBox = Listbox(g_tk,font=TempFont,activestyle='none',
                            width=10, height=1, borderwidth=5,relief='ridge',
                            yscrollcommand=ListBoxScollbar.set)

    searchListBox.insert(1, "서울특별시")
    searchListBox.insert(2, "부산광역시")
    searchListBox.insert(3, "경기도")
    searchListBox.pack()
    searchListBox.place(x=10,y=100)
    ListBoxScollbar.config(command=searchListBox.yview)

def initInputLabel():
    TempFont = font.Font(g_tk, size=15, weight='bold', family='Consolas')
    InputLabel = Entry(g_tk,font=TempFont,width=26,borderwidth=12,relief='ridge')
    InputLabel.pack()
    InputLabel.place(x=10,y=150)


def SearchLibrary():
    # 여기가 데이터 받는곳이네
    pass

def initRenderText():
    # 여기가 정보 출력하는곳
    global RenderText

    RenderTextScrolbar = Scrollbar(g_tk)
    RenderTextScrolbar.pack()
    RenderTextScrolbar.place(x=380,y=250)

    RenderText = Text(g_tk,width=49,height=27,borderwidth=12,relief='ridge',
                      yscrollcommand=RenderTextScrolbar.set)
    RenderText.pack()
    RenderText.place(x=10,y=250)
    #RenderTextScrolbar.config(command=RenderText.yview)
    #RenderTextScrolbar.pack(side=RIGHT,fill=BOTH)

    #RenderText.configure(state='disabled')
    pass

def searchButtonAction():
    global searchListBox
    RenderText.configure(state='normal')
    RenderText.delete(0,0,END)
    iSearchIndex = searchListBox.curselection()[0]
    if iSearchIndex == 0:
        SearchLibrary()
    elif iSearchIndex ==1:
        pass
    elif iSearchIndex ==2:
        pass

    RenderText.configure(state='disabled')


def initSearchButton():
    TempFont = font.Font(g_tk, size=12, weight='bold', family='Consolas')
    SearchButton = Button(g_tk,font=TempFont,text="검색", command=searchButtonAction)
    SearchButton.pack()
    SearchButton.place(x=340,y=160)


#initTopText()
initSearchListBox()
initInputLabel()
initSearchButton()
initRenderText()

g_tk.mainloop()



