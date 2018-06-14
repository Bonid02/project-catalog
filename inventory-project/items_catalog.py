#!/usr/bin/ python

import random
import string
import httplib2
import json
import requests
import os
import Cookie
import re
from flask import Flask, render_template, request
from flask import redirect, url_for, flash, jsonify, make_response
from flask import session as login_session
from oauth2client.client import FlowExchangeError, flow_from_clientsecrets
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Category, Item, User
from pprint import pprint
from datetime import datetime, timedelta

# Create Flask instance
app = Flask(__name__)

# Open and read client_secrets.json file for google oauth
CLIENT_ID = json.loads(open('client_secrets.json', 'r').
                       read())['web']['client_id']
APPLICATION_NAME = "Inventory Catalog Application"

# Use inventory.db as Base
engine = create_engine('sqlite:///inventory.db')
Base.metadata.bind = engine

# Create session to inventory.db
DBSession = sessionmaker(bind=engine)
session = DBSession()

# This is latest items array
latest_array = []
# Variable to refresh category
refresh_cat_temp = ""


# Create anti-forgery state token
@app.route('/login')
def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    login_session['state'] = state
    # return "The current session state is %s" % login_session['state']
    return render_template('login.html', STATE=state)


# Route to check access token in google oauth
# This is called via ajax in login.html
@app.route('/gconnect', methods=['POST'])
def gconnect():
    # Validate state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Obtain authorization code
    code = request.data

    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print "Token's client ID does not match app's."
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(
                                json.dumps(
                                    'Current user is already connected.'),
                                200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['provider'] = 'googleplus'
    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']

    # See if a user exists, if it doesn't make a new one
    userid = getUserID(login_session['email'])
    if not userid:
        createUser(login_session)
    login_session['user_id'] = userid

    for attr, value in session:
        print(attr, value)

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    return output


# Route to logout from google
@app.route('/logout')
def logoutDisconnect():
    # grab token from the user session
    access_token = login_session.get('access_token')
    if access_token is None:
        response = make_response(
                                json.dumps('Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Send api with token to revoke
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % access_token
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    if result['status'] == '200':
        # Reset the user's sesson.
        del login_session['access_token']
        del login_session['gplus_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']

        response = make_response(json.dumps('Successfully disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return redirect(url_for('mainCatalog'))
    else:
        # For whatever reason, the given token was invalid.
        response = make_response(
            json.dumps('Failed to revoke token for given user.', 400))
        response.headers['Content-Type'] = 'application/json'
        return response


# User Helper Functions
# This function will create a User in the user table
def createUser(login_session):
    newUser = User(NAME=login_session['username'], EMAIL=login_session[
        'email'], PICTURE=login_session['picture'])
    session.add(newUser)
    session.commit()
    user = session.query(User).first()
    return user.ID


# This function will return User object using ID as query parameter
def getUserInfo(user_id):
    user = session.query(User).filter_by(ID=user_id).one()
    return user


# This function will return User ID using EMAIL as query parameter
def getUserID(email):
    try:
        user = session.query(User).filter_by(EMAIL=email).one()
        return user.id
    except:
        return None


# This route will return JSON list of all categories and items.
@app.route('/catalog.json')
def jsonAll():
    all_categories = session.query(Category).all()
    categories_array = []
    for i in all_categories:
        new_cat = i.serialize
        all_items = session.query(Item).filter_by(CATEGORY_ID=i.ID).all()
        items_array = []
        for n in all_items:
            items_array.append(n.serialize)
        new_cat['items'] = items_array
        categories_array.append(new_cat)
    return jsonify(Inventory=[categories_array])


# Route to get JSON data of items in a category using Item CATEGORY_ID
# Called via jquery ajax call in catalog.html
@app.route('/category/<int:category_id>')
def jsonItems(category_id):
    all_items = session.query(Item).filter_by(CATEGORY_ID=category_id).all()
    return jsonify(Items=[i.serialize for i in all_items])


# Route to get JSON data of item details including Category
# details using Item ID. This is called via jquery ajax
@app.route('/item/<int:item_id>')
def jsonItemDetail(item_id):
    items_details = session.query(Item).filter_by(ID=item_id).one()
    item_custom = items_details.serialize
    item_cat_id = items_details.CATEGORY_ID
    cat_name = session.query(Category).filter_by(ID=item_cat_id).one()
    item_custom['cat_detail'] = cat_name.serialize
    return jsonify(Item=item_custom)


# This is the homepage route
@app.route('/')
def mainCatalog():
    # This is mainly used for displaying the newly refreshed 
    # category list, it occurs during adding and editing an item
    global refresh_cat_temp
    cat_id = refresh_cat_temp
    refresh_cat_temp = ''
    if cat_id:
        catalog_id = session.query(Category).filter_by(ID=cat_id).one()
        cat_name = catalog_id.NAME
    else:
        cat_name = ''

    # Get all categories
    all_category = session.query(Category).all()
    session.close()

    # Get the value of the of cookie 'item_name'
    # check if already included in latest_aray
    # otherwise do not append
    try:
        item_name = request.cookies.get("item_name")
        if item_name in latest_array:
            print('do add to latest array')
        else:
            latest_array.append(item_name)

    except (Cookie.CookieError, KeyError):
        latest_array.append("No Latest Items Found")

    # Render readonly version of catalog.html if not logged in to google
    # otherwise render full version
    if 'username' not in login_session:
        return render_template('ro_catalog.html', categories=all_category,
                               latest_items=latest_array,
                               category_name=cat_name)
    else:
        return render_template('catalog.html', categories=all_category,
                               latest_items=latest_array,
                               category_name=cat_name)


# Route to display all items inside a category
# called via ajax in jquery
@app.route('/catalog/<category_name>/items')
def categoryItems(category_name):
    category = session.query(Category).filter_by(NAME=category_name).one()
    all_items = session.query(Item).filter_by(CATEGORY_ID=category.ID).all()
    return render_template('items_category.html', items=all_items)


# Route that returns description of an item
@app.route('/catalog/<category_name>/<item_name>')
def itemDetails(category_name, item_name):
    category = session.query(Category).filter_by(NAME=category_name).one()
    item = session.query(Item).filter_by(CATEGORY_ID=category.ID,
                                         NAME=item_name).one()
    session.close()
    return item.DESCRIPTION


# Add new item without category name
@app.route('/catalog/addnew', methods=['GET', 'POST'])
def addNewItem():
    if request.method == 'POST':
        new_item = Item(NAME=request.form['name-in'],
                        DESCRIPTION=request.form['desc-in'],
                        QUANTITY=request.form['quantity-in'],
                        IMAGE_URL=request.form['imgurl-in'],
                        CATEGORY_ID=request.form['category-in'])
        session.add(new_item)
        session.commit()
        flash('New Item %s Successfully Created' % (new_item.NAME))
        session.close()
        # Assign a value to refresh_cat_temp for refreshing category list
        global refresh_cat_temp
        refresh_cat_temp = new_item.CATEGORY_ID
        rand_num = random.randint(0, 10000)
        resp = make_response(redirect(url_for('mainCatalog')))
        # Set cookie parameters
        resp.set_cookie('item_name', value=new_item.NAME, max_age=600)
        return resp


# Edit item route
@app.route('/catalog/edit', methods=['GET', 'POST'])
def editItem():
    item_id = request.form['key-edit']
    edit_item = session.query(Item).filter_by(ID=item_id).one()
    if request.method == 'POST':
        if request.form['name-edit']:
            edit_item.NAME = request.form['name-edit']
        if request.form['desc-edit']:
            edit_item.DESCRIPTION = request.form['desc-edit']
        if request.form['quantity-edit']:
            edit_item.QUANTITY = request.form['quantity-edit']
        if request.form['imgurl-edit']:
            edit_item.IMAGE_URL = request.form['imgurl-edit']
        if request.form['category-edit']:
            edit_item.CATEGORY_ID = request.form['category-edit']
        session.add(edit_item)
        session.commit()
        flash('Item %s Updated' % (edit_item.NAME))
        session.close()
        # Assign a value to refresh_cat_temp for refreshing category list
        global refresh_cat_temp
        refresh_cat_temp = edit_item.CATEGORY_ID
        return redirect(url_for('mainCatalog'))


# Delete item route
@app.route('/catalog/delete', methods=['GET', 'POST'])
def deleteItem():
    item_id = request.form['key-del']
    item_to_del = session.query(Item).filter_by(ID=item_id).one()
    if request.method == 'POST':
        session.delete(item_to_del)
        session.commit()
        flash('Item %s Deleted' % (item_to_del.NAME))
        session.close()
        return redirect(url_for('mainCatalog'))


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=8000)
