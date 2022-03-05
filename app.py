from flask import Flask, request, jsonify, render_template
from flask_debugtoolbar import DebugToolbarExtension
from models import connect_db, db, Cupcake

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///cupcakes'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_ECHO'] = True
app.config['DEBUG_TB_INTERCEPTS_REDIRECTS'] = False
app.config['SECRET_KEY'] = 'cupcakesAreTasty2022'
debug = DebugToolbarExtension(app)

connect_db(app)

@app.route('/')
def show_home_page():
  """List all cupcakes and allow user to add cupcakes"""
  return render_template('home.html')

@app.route('/api/cupcakes')
def show_all_cupcakes():
  """Return all cupcakes in JSON"""
  all_cupcakes = [cupcake.serialize() for cupcake in Cupcake.query.all()]
  return jsonify(cupcakes=all_cupcakes)

@app.route('/api/cupcakes/<int:id>')
def show_cupcake(id):
  """Return single cupcake in JSON"""
  cupcake = Cupcake.query.get_or_404(id)
  return jsonify(cupcake=cupcake.serialize())

@app.route('/api/cupcakes', methods=["POST"])
def post_cupcake():
  """Post new cupcake to db"""
  flavor = request.json['flavor']
  rating = request.json['rating']
  size = request.json['size']
  image = request.json.get('image')
  new_cupcake = Cupcake(flavor=flavor,size=size,rating=rating,image=image)
  db.session.add(new_cupcake)
  db.session.commit()
  response_json = jsonify(cupcake=new_cupcake.serialize())
  return (response_json, 201)

@app.route('/api/cupcakes/<int:id>', methods=["PATCH"])
def update_cupcake(id):
  """Update cupcake"""
  cupcake = Cupcake.query.get_or_404(id)
  cupcake.flavor = request.json.get('flavor', cupcake.flavor)
  cupcake.size = request.json.get('size', cupcake.size)
  cupcake.rating = request.json.get('rating', cupcake.rating)
  cupcake.image = request.json.get('image', cupcake.image)
  db.session.commit()
  return jsonify(cupcake=cupcake.serialize())

@app.route('/api/cupcakes/<int:id>', methods=["DELETE"])
def delete_cupcake(id):
  """Delete cupcake"""
  cupcake = Cupcake.query.get_or_404(id)
  db.session.delete(cupcake)
  db.session.commit()
  return jsonify(message="deleted")

