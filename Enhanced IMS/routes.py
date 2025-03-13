
from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from app import app, db
from models import User, Product, Category, Supplier, Order
from forms import LoginForm, ProductForm, SupplierForm, OrderForm

@app.route('/')
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password')
    
    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/dashboard')
@login_required
def dashboard():
    # Get low stock products
    low_stock = Product.query.filter(Product.quantity <= Product.low_stock_threshold).all()
    
    # Get recent orders
    recent_orders = Order.query.order_by(Order.order_date.desc()).limit(5).all()
    
    return render_template('dashboard.html', low_stock=low_stock, recent_orders=recent_orders)

@app.route('/products', methods=['GET', 'POST'])
@login_required
def products():
    form = ProductForm()
    
    # Populate category choices
    form.category_id.choices = [(c.id, c.name) for c in Category.query.all()]
    
    # Populate supplier choices
    form.supplier_id.choices = [(s.id, s.name) for s in Supplier.query.all()]
    
    if form.validate_on_submit():
        product = Product(
            name=form.name.data,
            description=form.description.data,
            quantity=form.quantity.data,
            price=form.price.data,
            category_id=form.category_id.data,
            supplier_id=form.supplier_id.data,
            low_stock_threshold=form.low_stock_threshold.data
        )
        db.session.add(product)
        db.session.commit()
        flash('Product added successfully!')
        return redirect(url_for('products'))
    
    products = Product.query.all()
    return render_template('products.html', form=form, products=products)

@app.route('/edit_product/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_product(id):
    product = Product.query.get_or_404(id)
    form = ProductForm(obj=product)
    
    # Populate category choices
    form.category_id.choices = [(c.id, c.name) for c in Category.query.all()]
    
    # Populate supplier choices
    form.supplier_id.choices = [(s.id, s.name) for s in Supplier.query.all()]
    
    if form.validate_on_submit():
        product.name = form.name.data
        product.description = form.description.data
        product.quantity = form.quantity.data
        product.price = form.price.data
        product.category_id = form.category_id.data
        product.supplier_id = form.supplier_id.data
        product.low_stock_threshold = form.low_stock_threshold.data
        
        db.session.commit()
        flash('Product updated successfully!')
        return redirect(url_for('products'))
    
    return render_template('products.html', form=form, products=Product.query.all(), edit=True)

@app.route('/delete_product/<int:id>', methods=['POST'])
@login_required
def delete_product(id):
    product = Product.query.get_or_404(id)
    db.session.delete(product)
    db.session.commit()
    flash('Product deleted successfully!')
    return redirect(url_for('products'))

@app.route('/suppliers', methods=['GET', 'POST'])
@login_required
def suppliers():
    form = SupplierForm()
    
    if form.validate_on_submit():
        supplier = Supplier(
            name=form.name.data,
            contact_person=form.contact_person.data,
            email=form.email.data,
            phone=form.phone.data
        )
        db.session.add(supplier)
        db.session.commit()
        flash('Supplier added successfully!')
        return redirect(url_for('suppliers'))
    
    suppliers = Supplier.query.all()
    return render_template('suppliers.html', form=form, suppliers=suppliers)

@app.route('/edit_supplier/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_supplier(id):
    supplier = Supplier.query.get_or_404(id)
    form = SupplierForm(obj=supplier)
    
    if form.validate_on_submit():
        supplier.name = form.name.data
        supplier.contact_person = form.contact_person.data
        supplier.email = form.email.data
        supplier.phone = form.phone.data
        
        db.session.commit()
        flash('Supplier updated successfully!')
        return redirect(url_for('suppliers'))
    
    return render_template('suppliers.html', form=form, suppliers=Supplier.query.all(), edit=True)

@app.route('/delete_supplier/<int:id>', methods=['POST'])
@login_required
def delete_supplier(id):
    supplier = Supplier.query.get_or_404(id)
    db.session.delete(supplier)
    db.session.commit()
    flash('Supplier deleted successfully!')
    return redirect(url_for('suppliers'))

@app.route('/orders', methods=['GET', 'POST'])
@login_required
def orders():
    form = OrderForm()
    
    # Populate product choices
    form.product_id.choices = [(p.id, p.name) for p in Product.query.all()]
    
    if form.validate_on_submit():
        product = Product.query.get(form.product_id.data)
        
        if product.quantity >= form.quantity.data:
            # Create new order
            order = Order(
                product_id=form.product_id.data,
                quantity=form.quantity.data,
                user_id=current_user.id
            )
            
            # Update product quantity
            product.quantity -= form.quantity.data
            
            db.session.add(order)
            db.session.commit()
            flash('Order placed successfully!')
        else:
            flash('Insufficient stock!')
        
        return redirect(url_for('orders'))
    
    orders = Order.query.order_by(Order.order_date.desc()).all()
    return render_template('orders.html', form=form, orders=orders)

@app.route('/complete_order/<int:id>', methods=['POST'])
@login_required
def complete_order(id):
    order = Order.query.get_or_404(id)
    order.status = 'completed'
    db.session.commit()
    flash('Order marked as completed!')
    return redirect(url_for('orders'))
