from flask import Blueprint, render_template, request, redirect, url_for, session
from models.alert import Alert
from models.item import Item
from models.store import Store
from models.user import requires_login

# require_login is the decorator to add functionality to the function
# @requires_login has to go underneath the route decorator

alert_blueprint = Blueprint('alerts', __name__)

@alert_blueprint.route('/')
@requires_login
def index():
    alerts = Alert.find_many_by('user_email', session['email'])
    return render_template('alerts/index.html', alerts=alerts)


@alert_blueprint.route('/new', methods=['POST', 'GET'])
@requires_login
def new_alert():
    if request.method == 'POST':
        item_url = request.form['item_url']
        alert_name = request.form['name']
        price_limit = float(request.form['price_limit'])

        print(item_url)
        store = Store.find_by_url(item_url)
        print(store)
        item = Item(item_url, store.tag_name, store.query)
        item.load_price()
        item.save_to_mongo()

        Alert(alert_name, item._id, price_limit, session['email']).save_to_mongo()

        return redirect(url_for('.index'))

    return render_template('alerts/new_alert.html')


@alert_blueprint.route('/edit/<string:alert_id>', methods=['POST', 'GET'])
@requires_login
def edit_alert(alert_id):
    alert = Alert.get_by_id(alert_id)

    if request.method == "POST":
        price_limit = float(request.form['price_limit'])

        alert.price_limit = price_limit
        alert.save_to_mongo()

        # .index means access index function in current blueprint
        return redirect(url_for('.index'))

    return render_template('alerts/edit_alert.html', alert=alert)

@alert_blueprint.route('/delete/<string:alert_id>')
@requires_login
def delete_alert(alert_id):
    alert = Alert.get_by_id(alert_id)
    if alert.user_email == session['email']:
        alert.remove_from_mongo()
    return redirect(url_for('.index'))
