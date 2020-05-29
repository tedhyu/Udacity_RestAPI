from findARestaurant import findARestaurant
from models import Base, Restaurant
from flask import Flask, jsonify, request
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine
from login import *
import sys
import codecs
sys.stdout = codecs.getwriter('utf8')(sys.stdout)
sys.stderr = codecs.getwriter('utf8')(sys.stderr)

engine = create_engine('sqlite:///restaurants.db')

Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()
app = Flask(__name__)

@app.route('/restaurants', methods = ['GET', 'POST'])
def all_restaurants_handler():
  if request.method == 'GET':
    #Call the method to Get all of the restaurants
    return getAllRestaurants()
  elif request.method == 'POST':
    #Call the method to make a new restaurant 
    print "Making a New Restaurant"
    location = request.args.get('location', '')
    mealType = request.args.get('mealType', '')
    return makeANewRestaurant(location, mealType)

@app.route('/restaurants/<int:id>', methods = ['GET','PUT', 'DELETE'])
def restaurant_handler(id):
  if request.method == 'GET':
    return getRestaurant(id)

#Call the method to edit a specific restaurant  
  elif request.method == 'PUT':
    address = request.args.get('address', '')
    name = request.args.get('name', '')
    image = request.args.get('image', '')
    return updateRestaurant(id,name, image, address)

 #Call the method to remove a restaurant 
  elif request.method == 'DELETE':
    return deleteRestaurant(id)

def getAllRestaurants():
  restaurants = session.query(Restaurant).all()
  return jsonify(Restaurant=[i.serialize for i in restaurants])

def getRestaurant(id):
  restaurant = session.query(Restaurant).filter_by(id = id).one()
  return jsonify(restaurant=restaurant.serialize)

def makeANewRestaurant(location,mealType):
  print(location)
  print(mealType)
  foursquare = findARestaurant(mealType,location)
  restaurant = Restaurant(restaurant_name = foursquare['name'], restaurant_address = foursquare['address'], restaurant_image = foursquare['image'])
  session.add(restaurant)
  session.commit()
  return jsonify(Restaurant=restaurant.serialize)

def updateRestaurant(id,name, image, address):
  restaurant = session.query(Restaurant).filter_by(id = id).one()
  if name:
    restaurant.name = name
  if image:
    restaurant.image = image
  if address:
    restaurant.address = address
  session.add(restaurant)
  session.commit()
  return "Updated a Restaurant with id %s" % id

def deleteRestaurant(id):
  restaurant = session.query(Restaurant).filter_by(id = id).one()
  session.delete(restaurant)
  session.commit()
  return "Removed Restaurant with id %s" % id


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)

