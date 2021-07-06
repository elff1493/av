
import os
import hashlib

from PIL.IptcImagePlugin import i

from web import app
from sql import *
from web import HASHED
import datetime

from sys import platform
if platform == "linux" or platform == "linux2":
    usb = "/media/el/picture hard drive/"
elif platform == "win32":
    usb = "E:\\"
# save locals


raw = usb + "pictures"
done = usb +"done"
thum = usb + "thumb"
testf = "+0"
basedir = os.path.abspath(os.path.dirname(__file__))
# thumbs = "E:\\thumbs\\"


# setings
# app.config['THUMBNAIL_STORAGE_BACKEND'] = thumbs #this brakes and idk why

# web stuff # todo move to web.py


def md5(fname):
    hash_md5 = hashlib.md5()
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()


def hash_raw():
    n = 0
    for folder in os.listdir(raw):
        folder = os.path.join(raw, folder)
        print("scanning " + folder)
        if os.path.isdir(folder):

            if not os.path.exists(os.path.join(folder, "scan.txt")):
                print("new folder scan made")
                with open(os.path.join(folder, "scan.txt"), "w+") as file:
                    print("making")

            with open(os.path.join(folder, "scan.txt"), "r") as file:
                print("r")
                #print(file.read())
                items = [i for i in file.read().splitlines()]
                print(items)

            for image in os.listdir(folder):
                if image not in items:
                    print("adding " + image)

                    items.append(image)

                    imagep = os.path.join(folder, image)
                    h = md5(imagep)
                    with open(imagep, "rb") as f1:

                        with open(os.path.join(HASHED, h+"."+image.split(".")[-1]), "wb+") as f2:
                            f2.write(f1.read())
                    d = os.path.getmtime(imagep)
                    d = datetime.datetime.utcfromtimestamp(d)
                    im = Image(hash=h, ex=image.split(".")[-1], date=d)
                    db.session.add(im)
                else:
                    pass
                    #print("skippping " + image)

            with open(os.path.join(folder, "scan.txt"), "w+") as file:
                n += len(items)
                for i in items:
                    file.write(i)
                    file.write("\n")
    db.session.commit()
    #print(Image.query.all())
    print("total images = " + str(n))


def rescan():
    for folder in os.listdir(raw):
        try:
            os.remove(os.path.join(raw, folder, "scan.txt"))
        except Exception as e:
            print(e)


def del_txt():
    txt = Image.query.filter_by(ex="txt").all()

    print("purging txt", txt)
    for i in txt:
        db.session.delete(i)
    db.session.commit()

def run():
    host_name = socket.gethostname()
    ip = socket.gethostbyname(host_name)
    print(ip)
    print(socket.getfqdn("0.0.0.0"))
    app.run(host=ip, port=80)
    print(socket.getfqdn("0.0.0.0"))
    # app.run()

def what(x):
    for f in os.listdir(usb + x):
        print(f, md5(usb + x + "/" + f))

def find_hash(x):
    print(Image.query.filter(Image.hash.ilike(str(x) + '%')))
    print(Image.query.filter(Image.hash.ilike(str(x) + '%')))
    #input()
import socket

if __name__ == '__main__':
    #db.drop_all()
    #db.create_all()
    #rescan()
    i = Image.query.filter(Image.hash.ilike("9e0e15d299c5a89044028ed38842" + '%')).first()
    print(i.id)
    print(Image.query.filter_by(id=i.id+2).first().hash)

    #p = [db.session.delete(i) for i in Tag.query.all()]

    #t = Tag(name="test tag")
    #db.session.add(t)
    #db.session.commit()
    find_hash("1845")
    hash_raw()
    del_txt()
    run()
    #what("scan2")











