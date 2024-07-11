from flask import Flask, url_for, redirect,jsonify,render_template,request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
import os
from flask_login import UserMixin,login_user, LoginManager,login_required, logout_user,current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError
from flask_bcrypt import Bcrypt
app = Flask(__name__)#For config and locating and what root directory is

app.config['SQLALCHEMY_DATABASE_URI'] ='sqlite:///database.db'
app.config['SECRET_KEY'] ='thisiskey'

db= SQLAlchemy(app)
bcrypt =Bcrypt(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), nullable=False, unique=True)
    password = db.Column(db.String(80), nullable=False)
    cart = db.relationship('CartItem', backref='buyer', lazy=True)



class RegisterForm(FlaskForm):
    username = StringField(validators=[InputRequired(), Length(min=4,max=20)], render_kw={"placeholder": "Username"})
    password = PasswordField(validators=[InputRequired(), Length(min=4,max=20)], render_kw={"placeholder": "password"})
    submit = SubmitField("Register")

    def validate_username(self,username):
        existing_user_username = User.query.filter_by(
            username=username.data).first()
        if existing_user_username:
            raise ValidationError(
            "Alreay exists"
        )

class LoginForm(FlaskForm):
    username = StringField(validators=[InputRequired(), Length(min=4,max=20)], render_kw={"placeholder":"Username"})
    password = PasswordField(validators=[InputRequired(), Length(min=4,max=20)], render_kw={"placeholder":"password"})
    submit = SubmitField("Login ")
#========================================================================================================================================
class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cat_name = db.Column(db.String, nullable=False)
    products = db.relationship('Product', backref='category', lazy=True)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    unit = db.Column(db.String(20), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)

class CartItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)


#========================================================================================================================================
#USER
@app.route("/", methods=["GET","POST"])#binding "/" url to below function
def Home():
    form = LoginForm()
    if form.validate_on_submit():
        user =User.query.filter_by(username=form.username.data).first()
        if user:
            if bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user)
                return redirect(url_for("dashboard"))
    return render_template("index.html", form=form)

@app.route('/logout', methods=["GET","POST"])
@login_required
def logout():
    logout_user()
    return redirect(url_for('Home'))

@app.route("/register/user", methods=["GET","POST"])
def register_user():
    form = RegisterForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data)
        new_user = User(username = form.username.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for("Home"))
    
    return render_template("register_user.html", form=form)



@app.route('/User', methods=["GET","POST"])
def dashboard():
    all = Category.query.all()
    all_p = Product.query.all()
    username= current_user.username
    #current_user. get_id
    return render_template("User.html", all=all, all_p=all_p, username=username)


@app.route('/add_to_cart/<int:prod_id>', methods=["GET","POST"])
def add_product_to_cart(prod_id):
    if request.method =="POST":
        user_quantity=request.form['user_quantity']

        item= CartItem(
            user_id=current_user. get_id(),
            product_id=prod_id,
            quantity=user_quantity
        )
        db.session.add(item)
        db.session.commit()
        return redirect("/User")


@app.route('/cart', methods=["GET","POST"])
def cart():
    all = CartItem.query.all()
    all_p = Product.query.all()

    return render_template("cart.html", all=all, all_p=all_p)



@app.route('/delete_cart/<int:prod_id>', methods=['POST'])
def delete_task_cart(prod_id):
    task = Product.query.get(prod_id)
    db.session.delete(task)
    db.session.commit()
    return redirect(url_for('cart'))



#=================================================================================================================
#ADMIN
@app.route("/login/Admin", methods=["GET","POST"])
def login_admin():
    if request.method =="GET":
        return render_template("Admin.html")

@app.route("/inventory/Admin", methods=["GET","POST"])
def inventory():
    all = Category.query.all()
    all_p = Product.query.all()
    return render_template("Admin_inventory.html", all=all, all_p=all_p)

@app.route("/create/category", methods=["POST","GET"])
def add_category():
    if request.method == "POST":
        c_name=request.form['c_name']
        cat= Category(
            cat_name=c_name
        )
        db.session.add(cat)
        db.session.commit()

        return redirect("/inventory/Admin")
    
    return render_template("add_cat.html")

@app.route("/add/product", methods=["POST","GET"] )
def add_product():
    if request.method =="POST":
        p_name=request.form['p_name']
        p_price=request.form['p_price']
        p_quantity=request.form['p_quantity']
        p_unit=request.form['p_unit']
        c_id=request.form['c_id']
        
        prod= Product(
            product_name=p_name,
            price=p_price,
            unit=p_unit,
            quantity=p_quantity,
            category_id=c_id

        )
        
        db.session.add(prod)
        db.session.commit()
        return redirect("/inventory/Admin")

    cats=Category.query.all()
    return render_template("add_prod.html", cats=cats)

@app.route('/delete/<int:prod_id>', methods=['POST'])
def delete_task(prod_id):
    task = Product.query.get(prod_id)
    db.session.delete(task)
    db.session.commit()
    return redirect(url_for('inventory'))

@app.route('/edit/<int:prod_id>', methods=['GET', 'POST'])
def edit_task(prod_id):
    task = Product.query.get(prod_id)
    if request.method == 'POST':
        task.product_name = request.form['p_name']
        task.price = request.form['p_price']
        task.unit = request.form['p_unit']
        task.quantity = request.form['p_quantity']
        task.category_id = request.form['c_id']
        db.session.commit()
        return redirect(url_for('inventory'))
    cats=Category.query.all()
    return render_template('edit_admin.html', task=task, cats=cats)

@app.route('/delete_cat/<int:cat_id>', methods=['POST'])
def delete_task_cat(cat_id):
    #prod = Product.query.filter_by(category_id=cat_id).all()

    #db.session.delete(prod)
    #db.session.commit()
    
    db.session.query(Product).filter(Product.category_id==cat_id).delete()
    db.session.commit()

    task = Category.query.get(cat_id)
    db.session.delete(task)
    db.session.commit()
    return redirect(url_for('inventory'))

@app.route("/thankyou", methods=['GET', 'POST'])
def thankyou():
    return render_template("thankyou.html")

if __name__ == '__main__':
    app.debug=True
    app.run()