
from Tkinter import *
from tkMessageBox import *
import ttk,tkFileDialog
import glob
from PIL import Image, ImageTk
import os
from os.path import splitext
import sys
dir =os.getcwd()
print dir
sys.path.append(dir+'/src')
import tempfile
from core import diff as d
from core import loader

def init():
    global menucanvas
    global diffcanvas
    global choicecanvas
    global difflabel
    global slidebar
    global displaycanvas
    global factor
    global btn_diff
    global img2
    global img1
    img1 = img2 = None

    menucanvas = Canvas(frame)
    diffcanvas = Canvas(frame)
    choicecanvas = Canvas(frame)
    displaycanvas = Canvas(frame)
    slidebar = Label(root)
    sidebar()

    btn_load1 = Button(menucanvas, text="Load Image1", width=10, command=LoadImage1)
    btn_load1.pack(side=LEFT,padx=10,pady=5)

    btn_load2 = Button(menucanvas, text="Load Image2", width=10, command=LoadImage2)
    btn_load2.pack(side=LEFT,padx=10, pady=5)

    btn_diff = Button(diffcanvas,text="Diff", width=10, command=diff)
    btn_diff.pack(side=BOTTOM,padx=10, pady=5)

    menucanvas.pack(side=TOP,anchor=N)
    diffcanvas.pack(side=TOP,anchor=N)
    # create_btns()


def create_btns():
    global btn_2_up
    global btn_swipe
    global btn_onion
    global btn_differ

    btn_2_up = Button( text="2 up", width=10, command=twoup)
    btn_2_up.pack(side=LEFT,padx=10,pady=5)
    btn_2_up.place(anchor=S, x=150, y=400)

    btn_swipe = Button( text="Swipe", width=10, command=swipe)
    btn_swipe.pack(side=LEFT,padx=10, pady=5)
    btn_swipe.place(anchor=S, x=250, y=400)

    btn_onion = Button(text="Onion skin", width=10, command=onion)
    btn_onion.pack(side=LEFT,padx=10, pady=5)
    btn_onion.place(anchor=S, x=350, y=400)


    btn_differ = Button(text="Difference", width=10, command=differ)
    btn_differ.pack(side=LEFT,padx=10, pady=5)
    btn_differ.place(anchor=S, x=450, y=400)



def twoup():
    slidebar.place_forget()
    difflabel.place_forget()
    label1.place(x=100, y=100)
    label2.place(x=310, y=100)
    # btn_2_up.config(state='disabled')

def differ():
    slidebar.place_forget()
    difflabel.place_forget()
    label1.place_forget()
    label2.place_forget()
    showdiff(diffimage())
    # btn_differ.config(state='disabled')


def swipe():
    global choice
    label1.place_forget()
    label2.place_forget()
    difflabel.place(x=200, y=100)
    choice =1
    slidebar.place(anchor=S, x=300, y=360)
    # btn_swipe.config(state='disabled')


def onion():
    global choice
    label1.place_forget()
    label2.place_forget()
    difflabel.place(x=200, y=100)
    choice =2
    slidebar.place(anchor=S, x=300, y=360)
    # btn_onion.config(state='disabled')

def diffimage():
    diffimg = d.diff(openedimage1,openedimage2)
    return diffimg


def showdiff(tempimg):
    global difflabel
    global img
    global viewWindow
    temp_dir = tempfile.mkdtemp()
    filename, extension = splitext(openedimage1)
    temp_file = temp_dir+'/diff'+extension
    loader.save_image(tempimg,temp_file)
    img = tk_image(temp_file,200,200)
    im3 = ImageTk.PhotoImage(img)

    print im3
    print temp_file


    difflabel= Label(image=im3)
    difflabel.place(x=200, y=100)

    displaycanvas.image = im3
    displaycanvas.create_image(0, 0, anchor=CENTER, image=im3, tags="bg_img")


def diff():
    if img1!=None and img2!=None:
        label1.place_forget()
        label2.place_forget()
        tempimg = diffimage()
        showdiff(tempimg)
        create_btns()
        btn_diff.config(state='disabled')
    else:
        showwarning("Load Error","You haven't selected both image")

def sidebar():
    scale = Scale(slidebar,orient='horizontal', from_=0, to=100, showvalue=0,command=sidebarScale, length=200)
    scale.pack(side = "top")

def tk_image(path,w,h):
    tempimg = Image.open(path)
    tempimg = tempimg.resize((w,h))
    return tempimg

def file_open():
    openedimage=""
    filetypes = ['*.jpg','*.png','*.gif','*.bmp']
    openedimage=tkFileDialog.askopenfilename(title='Select an image',filetypes=[('JPG','*.jpg'),('PNG','*.png'),('BMP','*.bmp'),('GIF','*.gif')])
    return openedimage

def LoadImage1():
    global img1
    global openedimage1
    global im1
    global imagewidth1
    global imageheight1
    global label1

    openedimage1 = file_open()
    print openedimage1
    img1 = tk_image(openedimage1,200,200)
    print img1

    im1 = ImageTk.PhotoImage(img1)
    print im1
    label1 = Label(image=im1)
    label1.place(x=100, y=100)


def LoadImage2():
    global img2
    global openedimage2
    global im2
    global imagewidth2
    global imageheight2
    global label2

    openedimage2 = file_open()
    print openedimage2
    img2 = tk_image(openedimage2,200,200)
    print img2
    im2 = ImageTk.PhotoImage(img2)

    print im2
    label2= Label(image=im2)
    label2.place(x=310, y=100)

def sidebarScale(val):
    if choice == 1:
        tempimg= slideImage(img1,img2,int(val))
        tempimg = ImageTk.PhotoImage(tempimg)
    else:
        tempimg= onionSkinImage(img1,img2,int(val))
        tempimg = ImageTk.PhotoImage(tempimg)

    difflabel.config(image=tempimg)
    difflabel.place(x=200, y=100)
    displaycanvas.image = tempimg
    displaycanvas.create_image(0, 0, anchor=CENTER, image=tempimg, tags="bg_img")



def onionSkinImage(img1,img2,value):
	try:
		return Image.blend(img1, img2, float(value)/100)
	except ValueError:
		return Image.blend(img1.convert('RGB'), img2.convert('RGB'), float(value)/100)


def slideImage(img1,img2,value):
	imNew = Image.new('RGB',(img1.size),'white')
	sizex=img1.size[0]
	sizey=img1.size[1]
	x = (sizex*value)/100
	img1crop = img1.crop((x,0,sizex,sizey))
	img2crop = img2.crop((0,0,x,sizey))
	imNew.paste(img1crop,(x,0))
	imNew.paste(img2crop,(0,0))
	return imNew

root =Tk()

root.title("Image-Diff Tool")
root.minsize(600, 410)
frame = Frame(root)
frame.pack(expand=NO,fill=BOTH)

init()

root.mainloop()
