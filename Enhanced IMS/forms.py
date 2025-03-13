
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, IntegerField, FloatField, SelectField
from wtforms.validators import DataRequired, Email, EqualTo, Optional, NumberRange

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class ProductForm(FlaskForm):
    name = StringField('Product Name', validators=[DataRequired()])
    description = TextAreaField('Description')
    quantity = IntegerField('Quantity', validators=[DataRequired(), NumberRange(min=0)])
    price = FloatField('Price ($)', validators=[DataRequired(), NumberRange(min=0)])
    category_id = SelectField('Category', coerce=int)
    supplier_id = SelectField('Supplier', coerce=int)
    low_stock_threshold = IntegerField('Low Stock Alert Threshold', validators=[DataRequired(), NumberRange(min=1)])
    submit = SubmitField('Add Product')

class SupplierForm(FlaskForm):
    name = StringField('Supplier Name', validators=[DataRequired()])
    contact_person = StringField('Contact Person')
    email = StringField('Email', validators=[DataRequired(), Email()])
    phone = StringField('Phone Number')
    submit = SubmitField('Add Supplier')

class OrderForm(FlaskForm):
    product_id = SelectField('Product', coerce=int, validators=[DataRequired()])
    quantity = IntegerField('Quantity', validators=[DataRequired(), NumberRange(min=1)])
    submit = SubmitField('Place Order')
