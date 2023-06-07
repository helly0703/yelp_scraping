from datetime import datetime

from yelp_project import db


class Article(db.Model):
    __tablename__ = 'articles'

    article_id = db.Column(db.Integer, primary_key=True)
    article_title = db.Column(db.Text, unique=True)
    article_tag = db.Column(db.String(100))
    article_image = db.Column(db.Text)
    article_date = db.Column(db.DateTime)
    article_link = db.Column(db.Text)
    date_created = db.Column(db.DateTime, default=datetime.now)

    def __repr__(self):
        return self.article_id


class Activities(db.Model):
    __tablename__ = 'activities'

    activity_id = db.Column(db.Integer, primary_key=True)
    activity_author = db.Column(db.Text)
    activity_name = db.Column(db.Text)
    activity_link = db.Column(db.Text)
    date_created = db.Column(db.DateTime, default=datetime.now)

    def __repr__(self):
        return self.activity_id


class Event(db.Model):
    __tablename__ = 'events'

    event_id = db.Column(db.Integer, primary_key=True)
    event_date = db.Column(db.DateTime)
    event_link = db.Column(db.Text)
    event_location = db.Column(db.Text)
    event_name = db.Column(db.String(255))
    event_type = db.Column(db.String(255))
    image_link = db.Column(db.Text)
    date_created = db.Column(db.DateTime, default=datetime.now)

    def __repr__(self):
        return self.event_id


class Product(db.Model):
    __tablename__ = 'products'

    product_id = db.Column(db.Integer, primary_key=True)
    product_name = db.Column(db.String(50), unique=True)

    def __repr__(self):
        return self.product_id


class Category(db.Model):
    __tablename__ = 'category'

    category_id = db.Column(db.Integer, primary_key=True)
    category_name = db.Column(db.String(50), unique=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.product_id'))
    product = db.relationship('Product', backref='category')

    def __repr__(self):
        return self.category_id


class Emails(db.Model):
    __tablename__ = 'emails'

    email_id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True)

    def __repr__(self):
        return self.email_id
