import atexit
from flask import Flask

from models import init_db, close_db
from errors import ApiError, error_handler
from app import get_app
from views import register, login, UserView, create_ads, AdsView

init_db()
atexit.register(close_db)

app: Flask = get_app()

app.add_url_rule("/register", view_func=register, methods=["POST"])
app.add_url_rule("/login", view_func=login, methods=["POST"])
app.add_url_rule("/user/<int:user_id>", view_func=UserView.as_view("user"), methods=["GET", "PATCH", "DELETE"])
app.add_url_rule("/create_ad", view_func=create_ads, methods=["POST"])
app.add_url_rule("/ad/<int:ads_id>", view_func=AdsView.as_view("ads"), methods=["GET", "PATCH", "DELETE"])

app.errorhandler(ApiError)(error_handler)