
import os
import hashlib
#from Tkinter import *
from tkinter import *
from tkinter.simpledialog import askstring
#from tkSimpleDialog import askstring
import time
from PIL import Image as pImage
import PIL
if True:
    usb = "E:\\"
else:
    usb = "/media/el/picture hard drive/"

scan = "/media/el/VOLUME1/DCIM/100MEDIA"
scan = "F:\\DCIM\\100MEDIA"
save = usb + "pictures"
ids = usb + "ids"
hold = usb + "hold"


def md5(fname):
    hash_md5 = hashlib.md5()
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()


def what(x):
    for f in os.listdir(usb + x):
        yield f, md5(usb + x + "/" + f)


def add(hash, n1, n2):
    with open(os.path.join(ids, "log"), "a") as f:
        f.write(hash)
        f.write(" ")
        f.write(n1)
        f.write(" ")
        f.write(n2)
        f.write("\n")
        print(hash, n1, n2)

def make_hold(x):
    xm = 210*50
    ym = 297*50
    print(210%50, 297%50)
    print(210//50, 297//50)
    print()
    print(xm%250, ym%250)
    print(xm//250, ym//250)

    bace = pImage.new("RGB", (xm, ym),color=(255, 255, 255))
    space = pImage.new("RGB", (2500, 2500), color=(200, 200, 200))
    #space2 = pImage.new("RGB", (2500, 2500), color=(255, 0, 0))
    a = (47*50)//6
    b = (10*50)//5
    print(a, b)
    for i in range(5):
        for j in range(2):
            bace.paste(space, (j*(2500 + (b))+ (b), (2500*i)+(a*(i+1))))
            bace.paste(space, (xm - (j * (2500 + (b)) + (b)) - 2500, (2500 * i) + (a * (i + 1))))
            #bace.paste(space2, (xm - (b) - 2500, (2500 * i) + (a * (i + 1))))
    bace.resize((xm/2, ym/2), pImage.ANTIALIAS)
    bace.save(os.path.join(ids, "hold.png"))


class window(Tk):
    def __init__(self):
        Tk.__init__(self)
        self.butt = Button(master=self, text="get", command=self.loop)
        self.butt.pack()
        self.loc = Text(master=self)
        self.loc.pack()
        self.loc.insert("0.0", str(time.time()))
        self.after(0, self.loop)
        self.page = Frame(master=self)
        self.l = []
        self.b = []
        for x in range(4):
            self.l.append([0, 0, 0, 0, 0])
            self.b.append([])
            self.v = []
            for y in range(5):
                btn_text = StringVar()
                b = Button(master=self.page, textvariable=btn_text, command=lambda x=x, y=y: self.press(x, y))
                b.grid(row=y, column=x)

                self.b[x].append(b)
        self.page.pack()
        self.output = Label()
        self.var = StringVar(value="")
        #self.myText_Box.get("1.0", END)

    def pprint(self, text):
        self.var.set(text)

    def press(self, x, y):
        for x1 in range(4):
            for y1 in range(5):
                self.b[x1][y1]
        print(x, y)

    def loop(self):
        t = time.time() + 1000
        state = 1
        while True:
            if t - time.time() > 0:
                if state == 1:
                    if os.path.exists(scan):
                        state = 2
                        print("------------------------------")
                        self.get()
                elif state == 2:
                    if not os.path.exists(scan):
                        state = 1

                t = time.time() + 1000

            self.update()


    def get(self):
        tt = str(time.time())
        if os.path.exists(scan):
            #print("path good")
            for f in os.listdir(scan):
                out1 = ""
                out1 = "" #askstring("rename", str(f))
                if not out1:
                    out = str(f)
                else:
                    out = out1 + f.split(".")[-1]
                l = os.path.join(save, tt)
                if not os.path.exists(l):
                    os.mkdir(l)
                self.dupe_move(os.path.join(scan, f), os.path.join(hold, md5(os.path.join(scan, f)) + "." + f.split(".")[-1]))
                self.move(os.path.join(scan, f), os.path.join(l, out))
                add(md5(os.path.join(l, out)), f, out1)
                    #print(md5(os.path.join(l, out + f.split(".")[-1])), f, out)
        else:
            print("path bad")

    def move(self, a, b):
        with open(a, "rb") as f1:
            with open(b, "wb+") as f2:
                f2.write(f1.read())
        os.remove(a)

    def dupe_move(self, a, b):
        with open(a, "rb") as f1:
            with open(b, "wb+") as f2:
                f2.write(f1.read())
def hash_folder(path):
    for f in os.listdir(path):
        print(md5(os.path.join(path, f)), f)
        
if __name__ == "__main__":
    print(os.listdir(save))
    os.rename('E:\\pictures\\scan4\n', 'E:\\pictures\\scan4')
    hash_folder(os.path.join(save, "scan4"))
    #print(list(what("hold")))
    #root = window()
    #root.after(0, root.loop)
    #root.mainloop()
    #make_hold(4)
