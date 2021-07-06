from flask import Flask, send_from_directory, render_template, request, redirect, escape
from flask_thumbnails import Thumbnail
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import Form, FlaskForm
from wtforms import Form, FormField, HiddenField, TextField, TextAreaField, validators, StringField, SubmitField, BooleanField, SelectMultipleField, FieldList
#from wtforms.validators import InputRequired
import os

from sys import platform
if platform == "linux" or platform == "linux2":
    usb = "/media/el/picture hard drive/"
elif platform == "win32":
    usb = "E:\\"

app = Flask(__name__)
thumb = Thumbnail(app)
db = SQLAlchemy(app)
HASHED = usb + "hashed"

DATAFILE = usb + "data"

print(os.path.join(DATAFILE, 'data.sqlite'))

app.config['SQLALCHEMY_DATABASE_URI'] =\
    'sqlite:///' + os.path.join(DATAFILE, 'data.sqlite')

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config['THUMBNAIL_MEDIA_ROOT'] = HASHED
app.config['THUMBNAIL_MEDIA_URL'] = "/thumb/"
app.config['SECRET_KEY'] = os.urandom(32)

from sql import Image, Tag

@app.route('/')
def main():
    p = int(0)
    return page(p)


@app.route('/page/<p>')
def page(p=0):
    p = int(p)
    data = [(i.hash, i.ex) for i in Image.query.filter_by(deleted=False).paginate(p, 100, False).items]
    if len(data) != 100:
        data.extend([("no image", "png") for i in range(100-len(data))])
    return render_template("main.html", x1=range(10), y1=range(10), im=data, p=p)


@app.route("/image/<id>")
def image(id=""):
    return send_from_directory(HASHED, filename=id)

@app.route("/imaget/<id>")
def imaget(id=""):
    image = Image.query.filter_by(hash=id).first()

    return send_from_directory(HASHED, filename=id)


@app.route("/im/<hash>", methods=['GET', 'POST'])
def im(hash):
    image = Image.query.filter_by(hash=hash).first()
    if request.method == "POST":
        image.name = request.form.get("name", image.name)
        image.deleted = request.form.get("deleted", False) == "y"

        for i in Tag.query.all():
            if request.form.get("tag_" + i.name, False) == "y":
                if i not in image.tags:
                    image.tags.append(i)
            else:
                if i in image.tags:
                    image.tags.remove(i)

        db.session.commit()

    class F(FlaskForm):
        name = StringField(label="name:", default=image.name)
        date = image.date

        tags = TagsForm()

        for i in Tag.query.all():
            tags.list.append_entry()

            tags.list.entries[-1].label = i.name
            tags.list.entries[-1].name = "tag_" + i.name
            tags.list.entries[-1].process_data(i in image.tags)

        add_tag = StringField(label="add tag")
        add_tag_go = SubmitField(label="add tag")
        url = HiddenField(default="/im/" + escape(hash), id="url")  # idk if i need it

        deleted = BooleanField(label="delete", default=image.deleted)
        stored = "cd"
        go = SubmitField(label="save")

    form = F()
    n = Image.query.filter_by(id=image.id + 1).first()
    p = Image.query.filter_by(id=image.id - 1).first()
    return render_template("image.html", hash=hash, ex=image.ex, form=form, n=n, p=p)


@app.route("/thumb/<file>")
def thumb(file):
    return send_from_directory(app.config['THUMBNAIL_MEDIA_THUMBNAIL_ROOT'], filename=file)


@app.route("/addtag", methods=['POST'])
def addtag():
    t = request.form["add_tag"]
    u = request.form["url"]

    db.session.add(Tag(name=t))
    db.session.commit()
    return redirect(u)

@app.route("/scan")
def scaner():
    return render_template("scan.html")


class TagForm(Form):
    tick = BooleanField()
    hidden = HiddenField()

    def set(self, x, b):
        self.hidden.name = "tag_" + x.name
        self.hidden.default = False
        self.tick.label = x.name
        self.tick.name = "tag_" + x.name
        self.tick.process_data(b)


class TagsForm(Form):
    #list = FieldList(FormField(TagForm))
    list = FieldList(BooleanField())