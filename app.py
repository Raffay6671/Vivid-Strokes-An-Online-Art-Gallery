from flask import Flask, render_template, request, redirect, url_for, jsonify, session
from flask_pymongo import PyMongo
from bson.objectid import ObjectId

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/userdata"
app.secret_key = 'your_secure_secret_key_here'
mongo = PyMongo(app)

@app.route('/')
def index():
    return redirect(url_for('home_page'))

@app.route('/home')
def home_page():
    return render_template('home.html')

@app.route('/abstract-art')
def abstract_art():
    return render_template('abstract-art.html')



@app.route('/add-to-cart', methods=['POST'])
def add_to_cart():
    if 'user_id' not in session:
        return jsonify({'status': 'error', 'message': 'User not logged in'}), 401
    user_id = session['user_id']
    item_name = request.json.get('item_name')
    item_price = request.json.get('item_price')
    mongo.db.users.update_one(
        {'_id': ObjectId(user_id)},
        {'$push': {'cart': {'name': item_name, 'price': item_price}}}
    )
    return jsonify({'status': 'success', 'message': 'Item added to cart'})



@app.route('/cart')
def cart():
    if 'user_id' not in session:
        return redirect(url_for('login'))  
    user_id = session['user_id']
    user = mongo.db.users.find_one({'_id': ObjectId(user_id)})
    return render_template('cart.html', cart_items=user.get('cart', []))



@app.route('/remove-from-cart', methods=['POST'])
def remove_from_cart():
    if 'user_id' not in session:
        return jsonify({'status': 'error', 'message': 'User not logged in'}), 401

    user_id = session['user_id']
    item_name = request.json['item_name']
    

    result = mongo.db.users.update_one(
        {'_id': ObjectId(user_id)},
        {'$pull': {'cart': {'name': item_name}}}
    )

    if result.modified_count > 0:
        return jsonify({'status': 'success', 'message': 'Item removed successfully'})
    else:
        return jsonify({'status': 'error', 'message': 'Item not found or could not be removed'})


@app.route('/cart-data')
def cart_data():
    if 'user_id' not in session:
        return jsonify({'status': 'error', 'message': 'User not logged in'}), 401
    user_id = session['user_id']
    user = mongo.db.users.find_one({'_id': ObjectId(user_id)})
    cart_items = user.get('cart', [])
    total_items = len(cart_items)
    total_price = sum(item['price'] for item in cart_items)
    return jsonify({'totalItems': total_items, 'totalPrice': total_price})

@app.route('/checkout')
def checkout():
    if 'user_id' not in session:
        return redirect(url_for('login'))  # Redirect to login if not logged in
    user_id = session['user_id']
    user = mongo.db.users.find_one({'_id': ObjectId(user_id)})
    cart_items = user.get('cart', [])
    total_items = len(cart_items)
    subtotal = sum(item['price'] for item in cart_items)
    tax = subtotal * 0.05  # Assuming 5% tax
    shipping = 0 if subtotal > 500 else 30  # Free shipping for orders over $500
    total_price = subtotal + tax + shipping

    return render_template('checkout.html', total_items=total_items, subtotal=subtotal, tax=tax, shipping=shipping, total_price=total_price)


@app.route('/finalize-order', methods=['POST'])
def finalize_order():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    user_id = session['user_id']
    user = mongo.db.users.find_one({'_id': ObjectId(user_id)})
    if not user:
        return 'No user found', 404
    

    cart_items = user.get('cart', [])
    total_items = len(cart_items)
    subtotal = sum(item['price'] for item in cart_items)
    tax = subtotal * 0.05  
    shipping = 0 if subtotal > 500 else 30  # Free shipping for orders over $500
    total_price = subtotal + tax + shipping

    

    return render_template('final.html', total_items=total_items, subtotal=subtotal, tax=tax, shipping=shipping, total_price=total_price)


@app.route('/paintings')
def paintings():
    return render_template('paintings.html')



@app.route('/drawings')
def drawings():
    return render_template('drawings.html')



@app.route('/digital_art')
def digital_art():
    return render_template('digital_art.html')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        email = request.form.get('email')
        existing_user = mongo.db.users.find_one({'username': username})
        if not existing_user:
            mongo.db.users.insert_one({
                'username': username,
                'password': password,
                'email': email,
                'cart': []
            })
            return redirect(url_for('login'))
        return 'That username already exists!'
    return render_template('signup.html')



@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = mongo.db.users.find_one({'username': username, 'password': password})
        if user:
            session['user_id'] = str(user['_id'])
            return redirect(url_for('home_page'))
        return 'Invalid username/password combination'
    return render_template('login.html')

if __name__ == '__main__':
    app.run(debug=True)
