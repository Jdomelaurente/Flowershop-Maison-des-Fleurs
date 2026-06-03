from flask import Flask, render_template, redirect, url_for, request, session, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_migrate import Migrate
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.utils import secure_filename
import os

# Flask App Setup
app = Flask(__name__, template_folder='templates')
basedir = os.path.abspath(os.path.dirname(__file__))

# Configurations
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.join(basedir, "instance", "flower.db")}'
app.config['SECRET_KEY'] = 'your_secret_key'
UPLOAD_FOLDER = os.path.join('static', 'uploads')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Extensions
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# Models
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(50), default='user', nullable=False)

class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.Text, nullable=False)
    price = db.Column(db.Float, nullable=False)
    available_quantity = db.Column(db.Integer, nullable=False)
    image = db.Column(db.String(255), nullable=False)

    def __repr__(self):
        return f'<Item {self.description[:20]}>'
    
class Cart(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    item_id = db.Column(db.Integer, db.ForeignKey('item.id'), nullable=False)
    item_name = db.Column(db.String(100), nullable=False)
    item_price = db.Column(db.Float, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)

    def total_price(self):
        return self.quantity * self.item_price
    
class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    item_id = db.Column(db.Integer, db.ForeignKey('item.id'))
    quantity = db.Column(db.Integer)
    total_price = db.Column(db.Float)  # <-- Make sure this exists
    status = db.Column(db.String(20), default='pending')


import sqlite3

def get_all_orders():
    conn = sqlite3.connect('instance/flower.db')  # adjust this to your actual DB path
    conn.row_factory = sqlite3.Row  # this makes rows behave like dictionaries
    cur = conn.cursor()
    cur.execute("SELECT * FROM orders")  # ensure your table is named 'orders'
    orders = cur.fetchall()
    conn.close()
    return orders


def get_all_orders():
    return Order.query.all()


# Create admin user if not exists
with app.app_context():
    db.create_all()
    if not User.query.filter_by(username='admin').first():
        hashed_pw = generate_password_hash('admin123')
        db.session.add(User(username='admin', password=hashed_pw, role='admin'))
        db.session.commit()

# Login Manager
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Routes
@app.route('/')
def home():
    return render_template('Users/index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            session['user_id'] = user.id
            session['role'] = user.role
            flash('Login successful!', 'success')
            return redirect(url_for('admin_dashboard') if user.role == 'admin' else url_for('user_dashboard'))
        flash('Invalid credentials!', 'danger')
    return render_template('Users/index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        role = 'admin' if User.query.count() == 0 else 'user'

        if User.query.filter_by(username=username).first():
            flash('Username already exists.', 'danger')
        else:
            hashed_password = generate_password_hash(password)
            db.session.add(User(username=username, password=hashed_password, role=role))
            db.session.commit()
            flash(f'Registration successful! You are now registered as {role}.', 'success')
    return render_template('Users/register.html')

@app.route('/admin/dashboard')
@login_required
def admin_dashboard():
    if current_user.role != 'admin':
        flash('Access denied: Admins only.', 'danger')
        return redirect(url_for('home'))
    items = Item.query.all()
    return render_template('Admin/admin_dashboard.html', items=items)

@app.route('/admin_orders')
@login_required
def admin_orders():
    orders = get_all_orders()  # You must define this function
    return render_template('Admin/admin_orders.html', orders=orders)


@app.route('/view_feedbacks')
def view_feedbacks():
    ...

@app.route('/user-dashboard')
@login_required
def user_dashboard():
    return render_template('Users/user_dashboard.html', username=current_user.username)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    session.clear()
    flash('You have been logged out.', 'success')
    return redirect(url_for('login'))

@app.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        return "Password reset link has been sent to your email."
    return render_template('forgot_password.html')

@app.route('/blog')
def blog():
    return render_template('Users/blog.html')

@app.route('/about')
def about():
    return render_template('Users/about.html')

@app.route('/contact')
def contact():
    return render_template('Users/contact.html')

@app.route('/user_blog')
@login_required
def user_blog():
    return render_template('Users/user_blog.html')

@app.route('/user_about')
@login_required
def user_about():
    return render_template('Users/user_about.html')

@app.route('/user_contact')
@login_required
def user_contact():
    return render_template('Users/user_contact.html')


@app.route('/user_product_dashboard', methods=['GET', 'POST'])
@login_required
def user_product_dashboard():
    if request.method == 'POST':
        item_id = request.form['item_id']
        quantity = int(request.form['quantity'])

        # Retrieve item from DB
        item = Item.query.get(item_id)
        if quantity <= item.available_quantity:
            # Add to session cart
            cart = session.get('cart', [])
            cart.append({
                'item_id': item.id,
                'description': item.description,
                'price': item.price,
                'quantity': quantity
            })
            session['cart'] = cart
            flash('Item added to cart!')
        else:
            flash('Quantity exceeds available stock.')

        return redirect(url_for('Users/user_product_dashboard'))

    items = Item.query.all()
    cart = session.get('cart', [])
    return render_template('Users/user_product_dashboard.html', items=items, cart=cart)

@app.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    item_id = request.form['item_id']
    # your logic to add to session cart
    return redirect(url_for('user_products'))

@app.route('/view_cart')
@login_required
def view_cart():
    cart = session.get('cart', [])
    total_amount = sum(item['price'] * item['quantity'] for item in cart)
    return render_template('Users/view_cart.html', cart_items=cart, total_amount=total_amount)

@app.route('/checkout')
@login_required  # if you use login required decorator
def checkout():
    # For now, just show a simple template or a message
    return render_template('checkout.html')

@app.route('/payment')
def payment():
    return render_template('payment.html')

@app.route('/clear_cart')
def clear_cart():
    # Assuming your cart is stored in session:
    session.pop('cart', None)  # Remove cart data from session
    flash("Cart cleared successfully!", "success")
    return redirect(url_for('view_cart'))


@app.route('/buy_now', methods=['POST'])
@login_required
def buy_now():
    item_id = request.form['item_id']
    quantity = int(request.form['quantity'])
    description = request.form['description']
    price = float(request.form['price'])
    total_price = price * quantity

    item = Item.query.get(item_id)
    if item and quantity <= item.available_quantity:
        item.available_quantity -= quantity
        db.session.commit()

        # Store the order for admin
        new_order = Order(
            user_id=current_user.id,
            item_id=item.id,
            quantity=quantity,
            total_price=total_price,
            status='Successful'
        )
        db.session.add(new_order)
        db.session.commit()

        flash('Successful Buy!', 'success')
    else:
        flash('Purchase failed. Quantity exceeds available stock.', 'danger')

    return redirect(url_for('user_product_dashboard'))


@app.route('/add', methods=['GET', 'POST'])
@login_required
def add_new_item():
    if current_user.role != 'admin':
        flash('Access denied.', 'danger')
        return redirect(url_for('home'))

    if request.method == 'POST':
        description = request.form.get('description')
        price = request.form.get('price')
        quantity = request.form.get('available_quantity') or 0
        image_file = request.files.get('image')

        if not description or not price:
            flash("Description and price are required!", "danger")
            return redirect(url_for('add_new_item'))

        try:
            price = float(price)
            quantity = int(quantity)
        except ValueError:
            flash("Invalid price or quantity.", "danger")
            return redirect(url_for('add_new_item'))

        filename = 'default.jpg'
        if image_file and image_file.filename:
            filename = secure_filename(image_file.filename)
            image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            image_file.save(image_path)

        db.session.add(Item(description=description, price=price, available_quantity=quantity, image=filename))
        db.session.commit()
        flash("Item added successfully.", "success")
        return redirect(url_for('admin_dashboard'))

    return render_template('admin/add_new_item.html')

@app.route('/manage_users')
@login_required
def manage_users():
    users = User.query.order_by(User.id.asc()).all()
    return render_template('Admin/manage_users.html', users=users)

@app.route('/delete_item/<int:item_id>', methods=['POST'])
@login_required
def delete_item(item_id):
    item = Item.query.get_or_404(item_id)
    db.session.delete(item)
    db.session.commit()
    flash('Item deleted successfully.', 'success')
    return redirect(url_for('admin_dashboard'))
    
@app.route('/edit_item/<int:item_id>', methods=['GET', 'POST'])
@login_required
def edit_item(item_id):
    item = Item.query.get(item_id)
    if not item:
        flash('Item not found.', 'danger')
        return redirect(url_for('Admin/admin_dashboard'))
    return f"Edit form for item ID {item_id}"  # Replace with real form later

@app.route('/product_detail/<int:id>')
def product_detail(id):
    item = next((i for i in item if i['id'] == id), None)
    if not item:
        return "Item not found", 404
    return render_template('product_detail.html', item=item)

@app.route('/admin/delete_user', methods=['POST'])
@login_required
def delete_user():
    user_id = request.form.get('id')
    user = User.query.get(user_id)
    if user:
        db.session.delete(user)
        db.session.commit()
        flash('User deleted successfully.', 'success')
    else:
        flash('User not found.', 'danger')
    return redirect(url_for('manage_users'))

@app.route('/routes')
def list_routes():
    import urllib
    output = []
    for rule in app.url_map.iter_rules():
        methods = ','.join(rule.methods)
        line = urllib.parse.unquote(f"{rule.endpoint}: {rule} [{methods}]")
        output.append(line)
    return "<br>".join(sorted(output))

# Run app
if __name__ == '__main__':
    app.run(debug=True)
