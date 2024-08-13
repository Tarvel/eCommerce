from flask import current_app as app, Blueprint, render_template, flash, redirect, url_for, request, g
import secrets
import os
from app import bcrypt, db
from app.models import User, Products, Notification, add_to_cart, add_to_wishlist
from app.forms import RegisterForm, LoginForm, EditProfileForm, ProductForm, DeleteForm
from flask_login import login_user, logout_user, current_user, login_required

auth = Blueprint('auth', __name__, template_folder='templates', static_folder='static')
product = Blueprint('product', __name__, template_folder='templates', static_folder='static')

@product.before_request
def before_product_request():
    if request.method == 'POST':
        delete_form = DeleteForm()
        if delete_form.validate_on_submit():
            noty = Notification.query.filter_by(user_id=current_user.id).first()
            db.session.delete(noty)
            db.session.commit()

@product.route('/', methods=['POST', 'GET'])
def home():
    products = Products.query.all()
    if current_user.is_authenticated:
        delete = DeleteForm()
        notifs = current_user.notification
        image_file = url_for('static', filename='profile_pic/' + current_user.user_img)
        return render_template('home.html', image_file=image_file, products=products, notifs=notifs)
    else:
        return render_template('home.html', products=products)

@product.route('/add_to_carts/<int:id>')
@login_required
def add_to_carts(id):
    productz = Products.query.get_or_404(id)
    add_to_cart(id)
    notif_message = f"{productz.product_name} has been added to your cart"
    new_notifs = Notification(notification=notif_message, user_id=current_user.id)
    db.session.add(new_notifs)
    db.session.commit()
    return redirect(url_for('product.home'))

@product.route('/add_to_wishlists/<int:id>')
@login_required
def add_to_wishlists(id):
    productz = Products.query.get_or_404(id)
    add_to_wishlist(id)
    notif_mssg = f"{productz.product_name} has been added to your wishlist"
    new_notifs = Notification(notification=notif_mssg, user_id=current_user.id)
    db.session.add(new_notifs)
    db.session.commit()
    return redirect(url_for('product.home'))

@auth.route('/register', methods=['POST', 'GET'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('product.home'))
    form = RegisterForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        first_name = form.first_name.data.title()
        last_name = form.last_name.data.title()
        username = form.username.data
        email = form.email.data
        user = User(name=f"{first_name} {last_name}", email=email, username=username, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        login_user(user)
        notif_mssg = f"Welcome, {current_user.name}"
        new_notifs = Notification(notification=notif_mssg, user_id=current_user.id)
        db.session.add(new_notifs)
        db.session.commit()
        flash(f'Account has been created {first_name} {last_name}. Complete your profile.')
        return redirect(url_for('auth.edit_profile', username=user.username))
    return render_template('register.html', form=form)

@auth.route('/login', methods=['POST', 'GET'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('product.home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('product.home'))
        else:
            flash('Login Unsuccessful. Check email or password')
    return render_template('login.html', form=form)

@auth.route('/logout', methods=['POST', 'GET'])
def logout():
    logout_user()
    return redirect(url_for('product.home'))

@auth.route('/profile/<string:username>')
def profile(username):
    user = User.query.filter_by(username=username).first()
    if not user:
        flash('User does not exist')
        return redirect(url_for('product.home'))
    image_profile = url_for('static', filename='profile_pic/' + user.user_img)
    if current_user.is_authenticated:
        image_file = url_for('static', filename='profile_pic/' + current_user.user_img)
        return render_template('profile.html', profile=user, image_profile=image_profile, image_file=image_file)
    else:
        return render_template('profile.html', profile=user, image_profile=image_profile)

def save_pic(form_img):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_img.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pic', picture_fn)
    form_img.save(picture_path)
    return picture_fn

@auth.route('/edit_profile/<string:username>', methods=['POST', 'GET'])
@login_required
def edit_profile(username):
    if username != current_user.username:
        flash('Cannot edit another user\'s profile')
        return redirect(url_for('auth.edit_profile', username=current_user.username))
    image_file = url_for('static', filename='profile_pic/' + current_user.user_img)
    edit = EditProfileForm()
    edit_profile = User.query.filter_by(username=username).first()
    if edit.validate_on_submit():
        if edit.user_img.data:
            img_file = save_pic(edit.user_img.data)
            current_user.user_img = img_file
        edit_profile.name = f"{edit.first_name.data} {edit.last_name.data}"
        edit_profile.username = edit.username.data
        edit_profile.user_address = edit.user_address.data
        edit_profile.user_description = edit.user_description.data
        edit_profile.user_state = edit.user_state.data
        edit_profile.user_country = edit.user_country.data
        edit_profile.user_gender = edit.user_gender.data
        db.session.commit()
        flash('Profile updated successfully!')
        return redirect(url_for('auth.profile', username=current_user.username))
    elif request.method == 'GET':
        names = edit_profile.name.split()
        edit.first_name.data = names[0]
        edit.last_name.data = names[1]
        edit.username.data = edit_profile.username
        edit.user_address.data = edit_profile.user_address
        edit.user_description.data = edit_profile.user_description
        edit.user_state.data = edit_profile.user_state
        edit.user_country.data = edit_profile.user_country
        edit.user_gender.data = edit_profile.user_gender
    return render_template('edit_profile.html', form=edit, edit_profile=edit_profile, image_file=image_file)

def save_product_pic(form_img):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_img.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/products', picture_fn)
    form_img.save(picture_path)
    return picture_fn

@product.route('/add_product', methods=['POST', 'GET'])
@login_required
def add_product():
    form = ProductForm()
    image_file = url_for('static', filename='profile_pic/' + current_user.user_img)
    if form.validate_on_submit():
        if form.product_img.data:
            pics = [save_product_pic(pictures) for pictures in form.product_img.data]
        product_data = {
            "product_name": form.product_name.data,
            "product_description": form.product_description.data,
            "price": form.price.data,
            "category": form.category.data,
            "user_id": current_user.id
        }
        product = Products(**product_data)
        for i in range(min(len(pics), 5)):
            setattr(product, f"product_img{i+1}", pics[i])
        db.session.add(product)
        db.session.commit()
        return redirect(url_for('product.home'))
    return render_template('add_product.html', form=form, image_file=image_file)

@product.route('/product/<string:product_namez>/<int:product_id>', methods=['POST', 'GET'])
@login_required
def products(product_namez, product_id):
    image_file = url_for('static', filename='profile_pic/' + current_user.user_img)
    products = Products.query.get_or_404(product_id)
    return render_template('products.html', products=products, image_file=image_file)
