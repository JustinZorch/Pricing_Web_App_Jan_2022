from common.database import Database
from models.alert import Alert
from dotenv import load_dotenv

load_dotenv()

Database.initialize()

alerts = Alert.all()


for alert in alerts:
    alert.load_item_price()
    alert.notify_if_price_reached()
    alert.json()

if not alerts:
    print("No alerts have been created. Add an item and an alert to begin!")