import os

from flask import Flask, session, render_template
from views.alerts import alert_blueprint
from common.database import Database
from views.stores import store_blueprint
from views.users import user_blueprint


@app.before_first_request
def init_db():
    Database.initialize()

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY')
app.config.update(ADMIN=os.environ.get('ADMIN'))

@app.route('/')
def home():
    return render_template('home.html')


app.register_blueprint(alert_blueprint, url_prefix="/alerts")
app.register_blueprint(store_blueprint, url_prefix="/stores")
app.register_blueprint(user_blueprint, url_prefix="/users")

if __name__ == '__main__':
    app.run(debug=True)






