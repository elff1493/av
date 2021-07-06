from web import db
import sqlalchemy as ss

tag_ass = db.Table('association', db.Model.metadata,
    db.Column('Image_id', db.Integer, db.ForeignKey('images.id')),
    db.Column('Tag_id', db.Integer, db.ForeignKey('tags.id'))
)


class Image(db.Model):
    __tablename__ = "images"
    id = db.Column(db.Integer, primary_key=True)

    hash = db.Column(db.String)
    ex = db.Column(db.String)
    name = db.Column(db.String)
    date = db.Column(db.DATETIME)
    deleted = db.Column(db.Boolean, default=False)
    tags = db.relationship(
        "Tag",
        secondary=tag_ass,
        back_populates="taged")


    negative = False

    def __repr__(self):
        return self.hash + "." + self.ex

class Tag(db.Model):
    __tablename__ = "tags"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    taged = db.relationship(
        "Image",
        secondary=tag_ass,
        back_populates="tags")