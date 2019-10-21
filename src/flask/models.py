from flask_sqlalchemy import SQLAlchemy
#from flask_migrate import Migrate
import datetime

db = SQLAlchemy()
#migrate = Migrate(app, db)

class BaseModel(db.Model):
    """Base data model for all objects"""
    __abstract__ = True

    def __init__(self, *args):
        super().__init__(*args)

    def __repr__(self):
        """Define a base way to print models"""
        return '%s(%s)' % (self.__class__.__name__, {
            column: value
            for column, value in self._to_dict().items()
        })

    def json(self):
        """
                Define a base way to jsonify models, dealing with datetime objects
        """
        return {
            column: value if not isinstance(value, datetime.date) else value.strftime('%Y-%m-%d')
            for column, value in self._to_dict().items()
        }


#class Stock(BaseModel, db.Model):
class Stock(db.Model):
    """Model for the stock table"""
    __tablename__ = 'stock'

    id = db.Column(db.Integer, primary_key = True)
    symbol = db.Column(db.Text)
    price  = db.Column(db.Integer)

class Opportunity(db.Model):
    """Model for the stock table"""
    __tablename__ = 'trade_opportunity'

    id = db.Column(db.Integer, primary_key = True)
    stock_symbol = db.Column(db.Text)
    type = db.Column(db.Text)
    price  = db.Column(db.Integer)

'''
    def __repr__(self):
       return '<Stock {}>'.format(self.price) 
'''
