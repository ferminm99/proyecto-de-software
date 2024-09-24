from flask import redirect, render_template, request, url_for, abort, session, flash

from app.dao.encriptPassDao import verify
from app.dao.userDaoSQLAlchemy import UserDao
from app.models.user import User
from os import environ
from app.dao.encriptPassDao import encrypt

import requests
from oauthlib.oauth2 import WebApplicationClient
from flask import redirect,request, Flask
import os,json

GOOGLE_CLIENT_ID = environ.get("GOOGLE_CLIENT_ID", "429358953753-1hpnm45ioc7le8kfihuu2nud259jj49g.apps.googleusercontent.com")
GOOGLE_CLIENT_SECRET = environ.get("GOOGLE_CLIENT_SECRET", "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")
GOOGLE_DISCOVERY_URL = (
    "https://accounts.google.com/.well-known/openid-configuration"
)

# OAuth
client = WebApplicationClient(GOOGLE_CLIENT_ID)

def get_google_provider_cfg():
    return requests.get(GOOGLE_DISCOVERY_URL).json()

def login_google():
    # Find out what URL to hit for Google login
    google_provider_cfg = get_google_provider_cfg()
    authorization_endpoint = google_provider_cfg["authorization_endpoint"]

    # Use library to construct the request for Google login and provide
    # scopes that let you retrieve user's profile from Google
    request_uri = client.prepare_request_uri(
        authorization_endpoint,
        redirect_uri=request.base_url + "/callback",
        scope=["openid", "email", "profile"],
    )
    return redirect(request_uri)


def callback():
    # Get authorization code Google sent back to you
    code = request.args.get("code")

    # Find out what URL to hit to get tokens that allow you to ask for things on behalf of a user
    google_provider_cfg = get_google_provider_cfg()
    token_endpoint = google_provider_cfg["token_endpoint"]

    # Prepare and send a request to get tokens! Yay tokens!
    token_url, headers, body = client.prepare_token_request(
        token_endpoint,
        authorization_response=request.url,
        redirect_url=request.base_url,
        code=code
    )
    token_response = requests.post(
        token_url,
        headers=headers,
        data=body,
        auth=(GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET),
    )

    # Parse the tokens!
    client.parse_request_body_response(json.dumps(token_response.json()))

    # Now that you have tokens (yay) let's find and hit the URL
    # from Google that gives you the user's profile information,
    # including their Google profile image and email
    userinfo_endpoint = google_provider_cfg["userinfo_endpoint"]
    uri, headers, body = client.add_token(userinfo_endpoint)
    userinfo_response = requests.get(uri, headers=headers, data=body)

    

    # You want to make sure their email is verified.
    # The user authenticated with Google, authorized your
    # app, and now you've verified their email through Google!
    if userinfo_response.json().get("email_verified"):
        unique_id = userinfo_response.json()["sub"]
        users_email = userinfo_response.json()["email"]
        users_name = userinfo_response.json()["name"]
        try:        
            users_first_name = userinfo_response.json()["given_name"]
        except KeyError:
            users_first_name = "GoogleSinNombre"
        try:
            users_last_name = userinfo_response.json()["family_name"]
        except KeyError:
            users_last_name = "GoogleSinApellido"
    else:
        return "User email not available or not verified by Google.", 400

    # Create a user in your db with the information provided
    # by Google
    user = User.query.filter_by(email=users_email).first()
    # Doesn't exist? Add it to the database.
    if  user == None:
        newUser = User(email = users_email,password=encrypt(unique_id),first_name=users_first_name,last_name=users_last_name,username= users_name,active= 1, approved=0)
        UserDao.insert(newUser)
    else:
        if(user.approved == 1):
            session["user"] = user
            return redirect(url_for("home"))

    # Send user back to homepage
    return redirect(url_for("auth_login",desautorizado=1))

def login():
    desautorizado = request.args.get("desautorizado")
    if desautorizado == None:
        desautorizado = 0
    return render_template("auth/login.html",desautorizado=desautorizado)


def authenticate():
    params = request.form
 
    user = UserDao.getBy('email',params["email"])

    if (not user) or (not verify(params["password"], user.password) or (user.active == 0) or (user.approved == 0)):
        flash("errorAuth")
        return redirect(url_for("auth_login"))

    session["user"] = user
 
    flash("La sesión se inició correctamente.")

    return redirect(url_for("home"))

    
def logout():
    #del session["user"]
    session.clear()
    # flash("La sesión se cerró correctamente.")

    return redirect(url_for("auth_login"))
