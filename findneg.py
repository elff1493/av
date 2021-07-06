import sqlalchemy as sql


db = sql.create_engine('sqlite:///slide.db')

link = db.Table('association', db.Model.metadata,
    db.Column('Slide_id', db.Integer, db.ForeignKey('Slides.id')),
    db.Column('Location_id', db.Integer, db.ForeignKey('Locations.id'))
)

class Slide(db.Model):
    __tablename__ = "Slides"
    id = db.Column(db.Integer, primary_key=True)
    pic1 = db.Column(db.String)
    pic2 = db.Column(db.String)
    pic3 = db.Column(db.String)
    pic4 = db.Column(db.String)
    pic5 = db.Column(db.String)
    pic6 = db.Column(db.String)
    len = db.Column(db.Integer)

    location = db.relationship("locations",
        secondary=link,
        back_populates="locations")



class Location(db.Model):
    __tablename__ = "Locations"

    name = db.Column(db.String)
    prev = db.relationship("locations")
    info = db.Column(db.String)

    here = db.relationship("Slides",
        secondary=link,
        back_populates="Slides")


from tkinter import *
from tkinter.ttk import Treeview

class Window(Tk):
    def __init__(self):
        loc1 = Listbox(master=self)
        loc1.pack()





















