import os
from flask import Flask
from collections import Counter
from flask_sqlalchemy import SQLAlchemy
import html_text as ht
import css_style as cs

import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

app.config['DEBUG'] = True

from models import db, Stock, Opportunity
import postgres_keys as pgk

POSTGRES = {
    'user': pgk.db_user,
    'pw':   pgk.db_pw,
    'db':   pgk.db,
    'host': pgk.host,
    'port': pgk.dbport,
}
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://%(user)s:%(pw)s@%(host)s:%(port)s/%(db)s' % POSTGRES

db.init_app(app)
#db.app = app

@app.route('/')
def main_render():

   """ Collect all stock events """
   u = Opportunity.query.all()

   """ Display all events by type """
   stock_string = ''
   alerts={"BUY":[],"SELL":[],"WATCH":[]}

   for s in u:
        alerts[s.type].append([str(s.stock_symbol),  " ( $" + str(s.price)+ " ) "])
   return ht.html_headers() + cs.css() + ht.html_headers_b() +  ht.display_opportunity_div(alerts["SELL"], "SELL")  +  ht.display_opportunity_div(alerts["BUY"], "BUY") +  ht.display_opportunity_div(alerts["WATCH"], "WATCH") 


if __name__ == '__main__':
   app.run()
