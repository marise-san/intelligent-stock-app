from flask import render_template, flash, redirect, url_for, jsonify, request
from app import app, db
from app.models.product import Product, CategoryEnum
from app.models.stock_movement import StockMovement
from app.models.user import User
from app.forms import AddProductForm, EditStockForm, EditProductForm, LoginForm, RegistrationForm
import logging
from datetime import datetime, timedelta
from flask_login import current_user, login_user, logout_user, login_required
from app.decorators import admin_required

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Usuário ou senha inválidos', 'error')
            return redirect(url_for('login'))
        login_user(user, remember=True)
        return redirect(url_for('index'))
    return render_template('login.html', title='Entrar', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Parabéns, você foi registrado com sucesso!', 'success')
        login_user(user)
        return redirect(url_for('index'))
    return render_template('register.html', title='Registrar', form=form)

@app.route('/')
@app.route('/index')
@login_required
def index():
    page = request.args.get('page', 1, type=int)
    search_query = request.args.get('search', '')
    query = Product.query
    if search_query:
        query = query.filter(Product.name.contains(search_query) | Product.barcode.contains(search_query))
    products = query.paginate(page=page, per_page=12)

    low_stock_count = Product.query.filter(Product.quantity <= Product.minimum_stock).count()
    today = datetime.utcnow().date()
    thirty_days_from_now = today + timedelta(days=30)
    expiring_soon_count = Product.query.filter(Product.expiration_date.between(today, thirty_days_from_now)).count()

    for product in products.items:
        product.is_expiring_soon = False
        if product.expiration_date:
            time_to_expiration = product.expiration_date - today
            if timedelta(days=0) <= time_to_expiration <= timedelta(days=30):
                product.is_expiring_soon = True

    form = EditStockForm()
    return render_template('index.html', title='Home', products=products, form=form, search_query=search_query, low_stock_count=low_stock_count, expiring_soon_count=expiring_soon_count)

@app.route('/add_product', methods=['GET', 'POST'])
@login_required
@admin_required
def add_product():
    form = AddProductForm()
    if form.validate_on_submit():
        try:
            product = Product(
                barcode=form.barcode.data,
                name=form.name.data,
                description=form.description.data,
                category=CategoryEnum[form.category.data],
                supplier=form.supplier.data,
                cost_price=form.cost_price.data,
                sale_price=form.sale_price.data,
                unit_of_measure=form.unit_of_measure.data,
                minimum_stock=form.minimum_stock.data,
                expiration_date=form.expiration_date.data,
                quantity=form.quantity.data
            )
            db.session.add(product)
            db.session.commit()

            movement = StockMovement(product_id=product.id, quantity=product.quantity, movement_type='entrada')
            db.session.add(movement)
            db.session.commit()

            flash('Produto cadastrado com sucesso!', 'success')
            print(f'Produto cadastrado: {product}')
            return redirect(url_for('index'))
        except Exception as e:
            logging.error(f'Erro ao cadastrar produto: {e}')
            flash('Erro ao cadastrar produto.', 'error')
    else:
        if form.errors:
            logging.error(f'Erros no formulário: {form.errors}')
            print(f'Erros no formulário: {form.errors}')
    return render_template('add_product.html', title='Cadastrar Produto', form=form)

@app.route('/edit_stock/<int:product_id>', methods=['POST'])
@login_required
def edit_stock(product_id):
    product = Product.query.get_or_404(product_id)
    form = EditStockForm()
    if form.validate_on_submit():
        try:
            old_quantity = product.quantity
            product.quantity = form.quantity.data
            db.session.commit()

            quantity_diff = product.quantity - old_quantity
            movement = StockMovement(product_id=product.id, quantity=quantity_diff, movement_type='ajuste')
            db.session.add(movement)
            db.session.commit()

            print(f'Estoque do produto {product.name} atualizado para {product.quantity}')

            # Recalculate status for the updated product
            today = datetime.utcnow().date()
            thirty_days_from_now = today + timedelta(days=30)

            is_expiring_soon = False
            if product.expiration_date:
                time_to_expiration = product.expiration_date - today
                if timedelta(days=0) <= time_to_expiration <= timedelta(days=30):
                    is_expiring_soon = True

            stock_status_text = ""
            stock_status_class = ""
            if product.quantity == 0:
                stock_status_text = "Fora de estoque"
                stock_status_class = "out-of-stock"
            elif is_expiring_soon:
                stock_status_text = "Vencimento Próximo"
                stock_status_class = "expiring-soon"
            elif product.quantity <= product.minimum_stock:
                stock_status_text = "Estoque baixo"
                stock_status_class = "low-stock"
            else:
                stock_status_text = "Em estoque"
                stock_status_class = "in-stock"

            return jsonify({
                'success': True,
                'new_quantity': product.quantity,
                'minimum_stock': product.minimum_stock,
                'expiration_date': product.expiration_date.isoformat() if product.expiration_date else None,
                'is_expiring_soon': is_expiring_soon,
                'stock_status_text': stock_status_text,
                'stock_status_class': stock_status_class
            })
        except Exception as e:
            logging.error(f'Erro ao atualizar estoque: {e}')
            return jsonify({'success': False, 'error': 'Erro ao atualizar estoque.'})
    return jsonify({'success': False, 'errors': form.errors})

@app.route('/edit_product/<int:product_id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_product(product_id):
    product = Product.query.get_or_404(product_id)
    form = EditProductForm(obj=product)
    if form.validate_on_submit():
        try:
            product.name = form.name.data
            product.description = form.description.data
            product.category = CategoryEnum[form.category.data]
            product.supplier = form.supplier.data
            product.cost_price = form.cost_price.data
            product.sale_price = form.sale_price.data
            product.minimum_stock = form.minimum_stock.data
            product.expiration_date = form.expiration_date.data
            db.session.commit()
            flash('Produto atualizado com sucesso!', 'success')
            print(f'Produto {product.name} atualizado.')
            return redirect(url_for('index'))
        except Exception as e:
            logging.error(f'Erro ao atualizar produto: {e}')
            flash('Erro ao atualizar produto.', 'error')
    return render_template('edit_product.html', title='Editar Produto', form=form, product=product)

@app.route('/delete_product/<int:product_id>', methods=['POST'])
@login_required
@admin_required
def delete_product(product_id):
    product = Product.query.get_or_404(product_id)
    try:
        quantity = product.quantity
        db.session.delete(product)
        db.session.commit()

        movement = StockMovement(product_id=product.id, quantity=-quantity, movement_type='saída')
        db.session.add(movement)
        db.session.commit()

        flash('Produto excluído com sucesso!', 'success')
        print(f'Produto {product.name} excluído.')
        return jsonify({'success': True})
    except Exception as e:
        logging.error(f'Erro ao excluir produto: {e}')
        return jsonify({'success': False, 'error': 'Erro ao excluir produto.'})

@app.route('/low_stock')
@login_required
@admin_required
def low_stock():
    products = Product.query.filter(Product.quantity <= Product.minimum_stock).all()
    return render_template('low_stock.html', title='Estoque Baixo', products=products)

@app.route('/expiring_soon')
@login_required
@admin_required
def expiring_soon():
    today = datetime.utcnow().date()
    thirty_days_from_now = today + timedelta(days=30)
    products = Product.query.filter(Product.expiration_date.between(today, thirty_days_from_now)).all()
    return render_template('expiring_soon.html', title='Vencimento Próximo', products=products)

@app.route('/inventory_report')
@login_required
@admin_required
def inventory_report():
    products = Product.query.all()
    return render_template('inventory_report.html', title='Relatório de Inventário', products=products)

@app.route('/stock_movement_report')
@login_required
@admin_required
def stock_movement_report():
    page = request.args.get('page', 1, type=int)
    movements = db.session.query(StockMovement, Product).join(Product).order_by(StockMovement.timestamp.desc()).paginate(page=page, per_page=20)
    return render_template('stock_movement_report.html', title='Relatório de Movimentação de Estoque', movements=movements)

@app.route('/manage_users')
@login_required
@admin_required
def manage_users():
    users = User.query.all()
    return render_template('manage_users.html', title='Gerenciar Usuários', users=users)

@app.route('/change_role/<int:user_id>', methods=['POST'])
@login_required
@admin_required
def change_role(user_id):
    user = User.query.get_or_404(user_id)
    new_role = request.form.get('role')
    if new_role in ['admin', 'operador']:
        user.role = new_role
        db.session.commit()
        flash(f'O papel do usuário {user.username} foi alterado para {new_role}.', 'success')
    else:
        flash('Papel inválido.', 'error')
    return redirect(url_for('manage_users'))

@app.route('/delete_user/<int:user_id>', methods=['POST'])
@login_required
@admin_required
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    if user.id == current_user.id:
        flash('Você não pode excluir a si mesmo.', 'error')
        return redirect(url_for('manage_users'))
    db.session.delete(user)
    db.session.commit()
    flash(f'Usuário {user.username} excluído com sucesso.', 'success')
    return redirect(url_for('manage_users'))
