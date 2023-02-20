from flask import Flask,flash, render_template,redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField,SelectField,TextAreaField
from wtforms.validators import DataRequired
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.orm import relationship
from forms import RegisterForm,LoginForm,Create_Cafe_Form
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user
from test import places,get_user_location

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///cafes.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
Bootstrap(app)
db = SQLAlchemy(app)




app.app_context().push()

login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class Cafe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=True)
    address = db.Column(db.String(200), nullable=True)
    city = db.Column(db.String(50), nullable=True)
    state = db.Column(db.String(2), nullable=True)
    zip_code = db.Column(db.String(10), nullable=True)
    latitude = db.Column(db.Float, nullable=True)
    longitude = db.Column(db.Float, nullable=True)
    description = db.Column(db.Text, nullable=True)
    wifi = db.Column(db.Boolean, nullable=True)
    power_outlets = db.Column(db.Boolean, nullable=True)
    img_url = db.Column(db.String(500), nullable=True)


class User(UserMixin,db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    profile_pic_url = db.Column(db.String(200))
    phone_number = db.Column(db.String(20))

    def __repr__(self):
        return '<User {}>'.format(self.username)

db.create_all()



@app.route('/')
def index():
    cafe = Cafe.query.all()
    return render_template('index.html', cafe=cafe)

@app.route('/nearby_cafes')
def cafe_list():
    get_user_location()
    new_places= places[::4]
    return render_template('nearby_cafes.html', places1=new_places)



@app.route('/login', methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data

        user = User.query.filter_by(email=email).first()
        
        if user and check_password_hash(user.password_hash, password):
            login_user(user)
            return redirect(url_for('index'))
          
    return render_template("login.html", form=form)


@app.route('/register', methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():

        hash_and_salted_password = generate_password_hash(
            form.password.data,
            method='pbkdf2:sha256',
            salt_length=8
        )
        new_user = User(
            email=form.email.data,
            name=form.name.data,
            password_hash=hash_and_salted_password,
        )
        db.session.add(new_user)
        db.session.commit()
        flash('Successfully registered!! ')
  
        
        return redirect(url_for("login"))

    return render_template("register.html", form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/user/profile')
@login_required
def user_profile():
    user = User.query.filter_by(id=current_user.id).first()
    return render_template('user_profile.html', user=user)



@app.route('/create_cafe', methods=['GET', 'POST'])
def create_cafe():
    form = Create_Cafe_Form()
    if request.method == 'POST':
        name = request.form['name']
        city = request.form['city']
        description = request.form['description']
        img_url = request.form['image']
        wifi = True if 'wifi' in request.form else False
        power_outlets = True if 'power_outlets' in request.form else False
        # Create a new Cafe object and add it to the database
        cafe = Cafe(name=name, city=city,img_url = img_url, description=description, wifi=wifi, power_outlets=power_outlets)
        db.session.add(cafe)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('create_cafe.html',form=form)

@app.route('/delete_cafe/<int:id>', methods=['GET', 'POST'])
def delete_cafe(id):
    cafe = Cafe.query.get(id)
    if request.method == 'POST':
        db.session.delete(cafe)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('delete_cafe.html', cafe=cafe)


if __name__ == '__main__':
    app.run(debug=True)


