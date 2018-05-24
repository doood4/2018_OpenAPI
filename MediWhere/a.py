from tkinter import *
from io import BytesIO
import urllib
import urllib.request
from PIL import Image, ImageTk
from google_map import make_googlemap_url

root = Tk()
root.geometry("500x500+500+200")

# openapi로 이미지 url을 가져옴.
url = make_googlemap_url((126.967812251,37),15)
with urllib.request.urlopen(url) as u:
    raw_data = u.read()

im = Image.open(BytesIO(raw_data))
image = ImageTk.PhotoImage(im)

label = Label(root, image=image, height=400, width=400)
label.pack()
label.place(x=0, y=0)
root.mainloop()