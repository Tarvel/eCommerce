from flask_migrate import current
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, PasswordField, FileField, TextAreaField, MultipleFileField
from wtforms_components import SelectField as SelectFieldWithOption
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError
from flask_wtf.file import FileAllowed, FileRequired
from app.models import User
from flask_login import current_user


class RegisterForm(FlaskForm):
    first_name = StringField("First Name", validators=[DataRequired()])
    last_name = StringField("Last Name", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    confirm_password = PasswordField("Confirm password", validators=[DataRequired(), EqualTo('password', message='Passwords do not match')])
    submit = SubmitField("Sign up")

    def no_spacing(form, field):
         if ' ' in field.data:
              raise ValidationError('No spacing allowed')
         
    username = StringField("Username", validators=[DataRequired(), no_spacing])

    
    def validate_username(self, username):
            user = User.query.filter_by(username=username.data).first()
            if user:
                 raise ValidationError("Username has been chosen, use a different one")


    def validate_email(self, email):
            user = User.query.filter_by(email=email.data).first()
            if user:
                 raise ValidationError("Email exists, use a different one")



class EditProfileForm(FlaskForm):
    first_name = StringField("First Name", validators=[DataRequired()])
    last_name = StringField("Last Name", validators=[DataRequired()])
    user_img = FileField('Choose Profile Picture', validators=[FileAllowed(['jpg', 'png'], 'Images only!')])
    user_address = TextAreaField("Address")
    user_description = TextAreaField("About", render_kw={"placeholder":"About yourself"})
    user_state = SelectField('State  ', validators=[DataRequired()], choices=[('0', 'Select'), ('Kwara', 'Kwara'), ('Lagos', 'Lagos'), ('Kogi', 'Kogi')])
    user_country = SelectField("Country ", choices=["1", "2", "3", "4", "5", "6"], validators=[DataRequired()])
    user_gender =  SelectField("Gender  ", choices=[('0', 'Select'), ('Male',"Male"), ('Female', "Female")], validators=[DataRequired()])
    submit = SubmitField("Save")

    def no_spacing(form, field):
         if ' ' in field.data:
              raise ValidationError('No spacing allowed')
         
    username = StringField("Username", validators=[DataRequired(), no_spacing])

    
    def validate_username(self, username):
            if username.data != current_user.username:
                user = User.query.filter_by(username=username.data).first()
                if user:
                    raise ValidationError("Username has been chosen, use a different one")





class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Sign in")
    



class ProductForm(FlaskForm):
    product_name = StringField("Product Name", validators=[DataRequired()])
    product_description = TextAreaField("Product Description", validators=[DataRequired()])
    product_img = MultipleFileField('Product images', validators=[FileAllowed(['jpg', 'png'], 'Images only!')])
    price = StringField("Price", validators=[DataRequired()])
    category = SelectField('Category ', choices=[('0', 'Select'), ('Fashion', 'Fashion'),('Tech', 'Tech'), ('Food', 'Food'), ('Others', 'Others')])
    submit = SubmitField("Save")

    def validate_username(self, product_img):
            pic_list  = []
            for files in product_img.data:
                 pic_list.append(files) 
            if len(pic_list)<=3:
                raise ValidationError("Choose at least 3 pictures")


class SearchForm(FlaskForm):
    search = StringField( render_kw={"placeholder":"Search"})
    submit = SubmitField("Search", render_kw={"style":"display:none;"})



class DeleteForm(FlaskForm):
    delete = SubmitField("Clear notifications", render_kw={"class":"btn btn-outline-primary"})


class CartForm(FlaskForm):
    cart = SubmitField("Add to cart",  render_kw={"class":"btn btn-primary"})

class WishlistForm(FlaskForm):
    wishlist = SubmitField("wishlist",  render_kw={"class":"btn btn-light"})