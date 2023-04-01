from flask import jsonify, request
from flask.views import MethodView

from auth import check_auth, check_password, hash_password
from crud import get_item, post_item, patch_item, delete_item
from errors import ApiError
from models import User, Token, Ads, get_session_maker
from schema import UserSchema, PatchUser, AdsSchema, PatchAds, validate

import uuid

Session = get_session_maker()


def register():
    user_data = validate(UserSchema, request.json)
    with Session() as session:
        user_data["password"] = hash_password(user_data["password"])
        user = post_item(session, User, **user_data)
        return jsonify({"id":user.id})
    

def login():
    login_data = validate(UserSchema, request.json)
    with Session() as session:
        user = session.query(User).filter(User.email == login_data["email"]).first()
        if User is None or not check_password(user.password, login_data["password"]):
            raise ApiError(401, "Invalid user or password")
        
        token = Token(user=user)
        session.add(token)
        session.commit()
        return jsonify({"token":token.id})
    

class UserView(MethodView):
    def get(self, user_id):
        with Session() as session:
            user = get_item(session, User, user_id)
            return jsonify({
                "id":user.id, "email":user.email, "created_at":user.created_at.isoformat()
            })
        
    def patch(self, user_id: int):
        with Session() as session:
            patch_data = validate(PatchUser, request.json)
            if "password" in patch_data:
                patch_data["password"] = hash_password(patch_data["password"])

            token = check_auth(session)
            user = get_item(session, User, user_id)
            if token.user_id != user.id:
                raise ApiError(403, "User has no access")

            user = patch_item(session, user, **patch_data)

            return jsonify(
                {
                    "id": user.id,
                    "email": user.email,
                    "created_at": user.created_at.isoformat(),
                }
            )
        
    def delete(self, user_id: int):
        with Session() as session:
            user = get_item(session, User, user_id)
            token = check_auth(session)
            if token.user_id != user.id:
                raise ApiError(403, "User has no access")
            
            delete_item(session, user)

            return {"deleted": True}
        


def create_ads():
    user_data = validate(AdsSchema, request.json)
    with Session() as session:
        if check_auth(session):
            token = uuid.UUID(request.headers.get("token"))
        # user = session.query(Token.user_id).filter(Token.id == token).first()
        # user_data = user_data["user_id"] = user.id
        user_for_token = get_item(session, Token, token)
        user = get_item(session, User, user_for_token.user_id)
        user_data["user_id"] = user.id
        
        ads = post_item(session, Ads, **user_data)
        return jsonify({"id":ads.id})
    

class AdsView(MethodView):
    def get(self, ads_id):
        with Session() as session:
            ads = get_item(session, Ads, ads_id)

            return jsonify({
                "id":ads.id, 
                "title":ads.title, 
                "description":ads.description,
                "user":ads.user_id,
                "created_at":ads.created_at.isoformat()
            })
        
    def patch(self, ads_id: int):
        with Session() as session:
            patch_data = validate(PatchAds, request.json)

            check_auth(session)

            ads = get_item(session, Ads, ads_id)
            if Ads is None:
                raise ApiError(403, "Ads has no access")

            ads = patch_item(session, ads, **patch_data)

            return jsonify({
                "id":ads.id, 
                "title":ads.title, 
                "description":ads.description, 
                "created_at":ads.created_at.isoformat()
            })
        
    def delete(self, ads_id: int):
        with Session() as session:
            ads = get_item(session, Ads, ads_id)
            check_auth(session)

            if Ads is None:
                raise ApiError(403, "Ads has no access")
            
            delete_item(session, ads)

            return {"deleted": True}