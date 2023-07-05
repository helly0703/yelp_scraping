from datetime import datetime

from sqlalchemy import select

from yelp_project import db
from yelp_project.yelp_scrap.utils import DBActions


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


activity_types = ['Review', 'Post','Unknown']


class Activities(db.Model):
    __tablename__ = 'activities'

    activity_id = db.Column(db.Integer, primary_key=True)
    activity_author = db.Column(db.Text)
    business_link = db.Column(db.Text)
    business = db.Column(db.Text)
    activity_type = db.Column(db.Enum(*activity_types, name='activity_types'))
    business_rating = db.Column(db.Float())

    def __repr__(self):
        return self.activity_id

    def filter_by_values(self, author, business, activity_type):
        activity_db = DBActions()
        activities = activity_db.get_data(Activities, {'activity_author': author, 'business': business,
                                                       'activity_type': activity_type})
        activity_db.commit_session()
        return activities.all()


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


business_types = ['restaurants', 'home services', 'auto services', 'other']


class Business(db.Model):
    __tablename__ = 'business'

    business_id = db.Column(db.Integer, primary_key=True)
    business_name = db.Column(db.String(50), unique=True)
    business_yelp_url = db.Column(db.Text)
    business_type = db.Column(db.Enum(*business_types, name='business_types'))
    business_ratings = db.Column(db.Float())
    contact = db.Column(db.String(15))
    location = db.Column(db.String(50))
    business_image_url = db.Column(db.Text)
    website = db.Column(db.Text)

    # Define the many-to-many relationship with categories
    categories = db.relationship('Category', secondary='business_categories')
    highlights = db.relationship('Highlights', secondary='business_highlights')
    features = db.relationship('Feature', secondary='business_features')
    items = db.relationship('MenuItems', secondary='business_items')

    def __repr__(self):
        return self.business_id

    def session_commit(self):
        db.session.commit()

    def get_business_instance(self, business_name):
        business_db = DBActions()
        business = business_db.check_if_data_exists(Business, 'business_name',
                                                    business_name)
        return business.business_id if business else None

    def add_business_to_db(self, business_data, business_type):
        business_instance = Business(business_name=business_data['restaurant_name'],
                                     business_yelp_url=business_data['restaurant_link_element'],
                                     business_type=business_type, business_ratings=business_data['ratings'],
                                     business_image_url=business_data['restaurant_img_link'])
        business_db = DBActions()
        business = business_db.check_if_data_exists(Business, 'business_name',
                                                    business_data['restaurant_name'])

        if not business:
            business_db.add_to_db(business_instance)
            business = business_db.check_if_data_exists(Business, 'business_name',
                                                        business_data['restaurant_name'])
        return business.business_id

    def add_business_categories(self, categories_list, business_id):
        for category in categories_list:
            cat_db = DBActions()
            category_instance = cat_db.check_if_data_exists(Category, 'category_name',
                                                            category)
            if not category_instance:
                cat_instance = Category(category_name=category)
                cat_db.add_to_db(cat_instance)
                category_instance = cat_db.check_if_data_exists(Category, 'category_name',
                                                                category)
            business_categories_insert = business_categories.insert().values(
                business_id=business_id,
                category_id=category_instance.category_id
            )
            select_business_category = select(business_categories).where(
                (business_categories.columns.business_id == business_id) &
                (business_categories.columns.category_id == category_instance.category_id))
            new_db = DBActions()
            result = new_db.insert_into_mapping_table(select_business_category)
            if not result.fetchone():
                new_db.insert_into_mapping_table(business_categories_insert)

                # Commit the changes to the database
                new_db.commit_session()

    def add_business_features(self, features_list, business_id):
        try:
            for feature in features_list:
                feature_db = DBActions()
                feature_instance = feature_db.check_if_data_exists(Feature, 'feature_name',
                                                                   feature)
                if not feature_instance:
                    feature_instance = Feature(feature_name=feature)
                    feature_db.add_to_db(feature_instance)
                    feature_instance = feature_db.check_if_data_exists(Feature, 'feature_name',
                                                                       feature)
                business_features_insert = business_features.insert().values(
                    business_id=business_id,
                    feature_id=feature_instance.feature_id
                )
                select_business_feature = select(business_features).where(
                    (business_features.columns.business_id == business_id) &
                    (business_features.columns.feature_id == feature_instance.feature_id))
                new_db = DBActions()
                result = new_db.insert_into_mapping_table(select_business_feature)
                if not result.fetchone():
                    new_db.insert_into_mapping_table(business_features_insert)

                    # Commit the changes to the database
                    new_db.commit_session()
        except Exception:
            pass

    def add_business_highlights(self, highlights_list, business_id):
        for highlight in highlights_list:
            highlight_db = DBActions()
            highlight_instance = highlight_db.check_if_data_exists(Highlights, 'highlights_name',
                                                                   highlight)
            if not highlight_instance:
                highlight_instance = Highlights(highlights_name=highlight)
                highlight_db.add_to_db(highlight_instance)
                highlight_instance = highlight_db.check_if_data_exists(Highlights, 'highlights_name',
                                                                       highlight)
            business_highlights_insert = business_highlights.insert().values(
                business_id=business_id,
                highlights_id=highlight_instance.highlights_id
            )
            select_business_highlights = select(business_highlights).where(
                (business_highlights.columns.business_id == business_id) &
                (business_highlights.columns.highlights_id == highlight_instance.highlights_id))
            new_db = DBActions()
            result = new_db.insert_into_mapping_table(select_business_highlights)
            if not result.fetchone():
                new_db.insert_into_mapping_table(business_highlights_insert)

                # Commit the changes to the database
                new_db.commit_session()

    def add_business_menu_items(self, menu_list, business_id):
        for items in menu_list:
            items_db = DBActions()
            items_instance = items_db.check_if_data_exists(MenuItems, 'item_name',
                                                           items['items_name'])
            if not items_instance:
                items_instance = MenuItems(item_name=items['items_name'], item_image_url=items['image_url'])
                items_db.add_to_db(items_instance)
                items_instance = items_db.check_if_data_exists(MenuItems, 'item_name',
                                                               items['items_name'])
            business_items_insert = business_items.insert().values(
                business_id=business_id,
                item_id=items_instance.item_id
            )
            select_business_items = select(business_items).where(
                (business_items.columns.business_id == business_id) &
                (business_items.columns.item_id == items_instance.item_id))
            new_db = DBActions()
            result = new_db.insert_into_mapping_table(select_business_items)
            if not result.fetchone():
                new_db.insert_into_mapping_table(business_items_insert)

                # Commit the changes to the database
                new_db.commit_session()

    def filter_by_business_types(self, business_type):
        business_db = DBActions()
        business = business_db.get_data(Business, {'business_type': business_type})
        return business


class Category(db.Model):
    __tablename__ = 'category'

    category_id = db.Column(db.Integer, primary_key=True)
    category_name = db.Column(db.String(50), unique=True)

    def __repr__(self):
        return self.category_id


class Feature(db.Model):
    __tablename__ = 'features'

    feature_id = db.Column(db.Integer, primary_key=True)
    feature_name = db.Column(db.String(100), unique=True)

    def __repr__(self):
        return self.feature_id


class Highlights(db.Model):
    __tablename__ = 'highlights'

    highlights_id = db.Column(db.Integer, primary_key=True)
    highlights_name = db.Column(db.String(50), unique=True)

    def __repr__(self):
        return self.highlights_id


class MenuItems(db.Model):
    __tablename__ = 'menu_items'

    item_id = db.Column(db.Integer, primary_key=True)
    item_name = db.Column(db.String(50), unique=True)
    item_image_url = db.Column(db.Text)

    def __repr__(self):
        return self.item_id


class Services(db.Model):
    __tablename__ = 'services'

    service_id = db.Column(db.Integer, primary_key=True)
    service_name = db.Column(db.String(50), unique=True)

    def __repr__(self):
        return self.service_id


class State(db.Model):
    __tablename__ = 'state'

    state_id = db.Column(db.Integer, primary_key=True)
    state_name = db.Column(db.String(50), unique=True)


class City(db.Model):
    __tablename__ = 'city'

    city_id = db.Column(db.Integer, primary_key=True)
    city_name = db.Column(db.String(50), unique=True)


class Emails(db.Model):
    __tablename__ = 'emails'

    email_id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True)

    def __repr__(self):
        return self.email_id


business_categories = db.Table(
    'business_categories', db.Model.metadata,
    db.Column('business_id', db.Integer, db.ForeignKey('business.business_id')),
    db.Column('category_id', db.Integer, db.ForeignKey('category.category_id'))
)

# Define the association table for the many-to-many relationship between products and features
business_features = db.Table(
    'business_features', db.Model.metadata,
    db.Column('business_id', db.Integer, db.ForeignKey('business.business_id')),
    db.Column('feature_id', db.Integer, db.ForeignKey('features.feature_id'))
)

business_highlights = db.Table(
    'business_highlights', db.Model.metadata,
    db.Column('business_id', db.Integer, db.ForeignKey('business.business_id')),
    db.Column('highlights_id', db.Integer, db.ForeignKey('highlights.highlights_id'))
)

business_items = db.Table(
    'business_items', db.Model.metadata,
    db.Column('business_id', db.Integer, db.ForeignKey('business.business_id')),
    db.Column('item_id', db.Integer, db.ForeignKey('menu_items.item_id'))
)

business_services = db.Table(
    'business_services', db.Model.metadata,
    db.Column('business_id', db.Integer, db.ForeignKey('business.business_id')),
    db.Column('service_id', db.Integer, db.ForeignKey('services.service_id'))
)
