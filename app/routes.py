from flask import Blueprint, render_template, request, redirect, url_for, flash
from app import db
from app.models import (
    Appliance, Category, Manufacturer, ExtraOption,
    Supply, Seller, Sale
)
from datetime import datetime

bp = Blueprint('main', __name__)


# ── Главная ──────────────────────────────────
@bp.route('/')
def index():
    stats = {
        'appliances': Appliance.query.count(),
        'categories': Category.query.count(),
        'manufacturers': Manufacturer.query.count(),
        'supplies': Supply.query.count(),
        'sellers': Seller.query.count(),
        'sales': Sale.query.count(),
        'options': ExtraOption.query.count(),
    }
    return render_template('index.html', stats=stats)


# ══════════════════════════════════════════════
#  ТЕХНИКА (Appliance)
# ══════════════════════════════════════════════
@bp.route('/appliances')
def appliance_list():
    appliances = Appliance.query.order_by(Appliance.name).all()
    return render_template('appliance/list.html', appliances=appliances)


@bp.route('/appliances/create', methods=['GET', 'POST'])
def appliance_create():
    categories = Category.query.order_by(Category.name).all()
    manufacturers = Manufacturer.query.order_by(Manufacturer.name).all()
    if request.method == 'POST':
        a = Appliance(
            name=request.form['name'],
            category_id=request.form['category_id'],
            manufacturer_id=request.form['manufacturer_id'],
            service_life=request.form.get('service_life', type=int),
            stock_quantity=request.form.get('stock_quantity', type=int) or 0,
        )
        db.session.add(a)
        db.session.commit()
        flash('Техника добавлена', 'success')
        return redirect(url_for('main.appliance_list'))
    return render_template('appliance/form.html', appliance=None, categories=categories, manufacturers=manufacturers)


@bp.route('/appliances/<int:id>/edit', methods=['GET', 'POST'])
def appliance_edit(id):
    a = Appliance.query.get_or_404(id)
    categories = Category.query.order_by(Category.name).all()
    manufacturers = Manufacturer.query.order_by(Manufacturer.name).all()
    if request.method == 'POST':
        a.name = request.form['name']
        a.category_id = request.form['category_id']
        a.manufacturer_id = request.form['manufacturer_id']
        a.service_life = request.form.get('service_life', type=int)
        a.stock_quantity = request.form.get('stock_quantity', type=int) or 0
        db.session.commit()
        flash('Техника обновлена', 'success')
        return redirect(url_for('main.appliance_list'))
    return render_template('appliance/form.html', appliance=a, categories=categories, manufacturers=manufacturers)


@bp.route('/appliances/<int:id>/delete', methods=['POST'])
def appliance_delete(id):
    a = Appliance.query.get_or_404(id)
    db.session.delete(a)
    db.session.commit()
    flash('Техника удалена', 'success')
    return redirect(url_for('main.appliance_list'))


# ══════════════════════════════════════════════
#  КАТЕГОРИИ
# ══════════════════════════════════════════════
@bp.route('/categories')
def category_list():
    categories = Category.query.order_by(Category.name).all()
    return render_template('category/list.html', categories=categories)


@bp.route('/categories/create', methods=['GET', 'POST'])
def category_create():
    parents = Category.query.order_by(Category.name).all()
    if request.method == 'POST':
        pid = request.form.get('parent_category_id')
        c = Category(
            name=request.form['name'],
            parent_category_id=pid if pid else None,
        )
        db.session.add(c)
        db.session.commit()
        flash('Категория добавлена', 'success')
        return redirect(url_for('main.category_list'))
    return render_template('category/form.html', category=None, parents=parents)


@bp.route('/categories/<int:id>/edit', methods=['GET', 'POST'])
def category_edit(id):
    c = Category.query.get_or_404(id)
    parents = Category.query.filter(Category.id_category != id).order_by(Category.name).all()
    if request.method == 'POST':
        c.name = request.form['name']
        pid = request.form.get('parent_category_id')
        c.parent_category_id = pid if pid else None
        db.session.commit()
        flash('Категория обновлена', 'success')
        return redirect(url_for('main.category_list'))
    return render_template('category/form.html', category=c, parents=parents)


@bp.route('/categories/<int:id>/delete', methods=['POST'])
def category_delete(id):
    c = Category.query.get_or_404(id)
    if c.appliances.count() > 0:
        flash('Нельзя удалить категорию с привязанной техникой', 'danger')
        return redirect(url_for('main.category_list'))
    db.session.delete(c)
    db.session.commit()
    flash('Категория удалена', 'success')
    return redirect(url_for('main.category_list'))


# ══════════════════════════════════════════════
#  ПРОИЗВОДИТЕЛИ
# ══════════════════════════════════════════════
@bp.route('/manufacturers')
def manufacturer_list():
    manufacturers = Manufacturer.query.order_by(Manufacturer.name).all()
    return render_template('manufacturer/list.html', manufacturers=manufacturers)


@bp.route('/manufacturers/create', methods=['GET', 'POST'])
def manufacturer_create():
    if request.method == 'POST':
        m = Manufacturer(
            name=request.form['name'],
            legal_address=request.form.get('legal_address'),
        )
        db.session.add(m)
        db.session.commit()
        flash('Производитель добавлен', 'success')
        return redirect(url_for('main.manufacturer_list'))
    return render_template('manufacturer/form.html', manufacturer=None)


@bp.route('/manufacturers/<int:id>/edit', methods=['GET', 'POST'])
def manufacturer_edit(id):
    m = Manufacturer.query.get_or_404(id)
    if request.method == 'POST':
        m.name = request.form['name']
        m.legal_address = request.form.get('legal_address')
        db.session.commit()
        flash('Производитель обновлён', 'success')
        return redirect(url_for('main.manufacturer_list'))
    return render_template('manufacturer/form.html', manufacturer=m)


@bp.route('/manufacturers/<int:id>/delete', methods=['POST'])
def manufacturer_delete(id):
    m = Manufacturer.query.get_or_404(id)
    if m.appliances.count() > 0:
        flash('Нельзя удалить производителя с привязанной техникой', 'danger')
        return redirect(url_for('main.manufacturer_list'))
    db.session.delete(m)
    db.session.commit()
    flash('Производитель удалён', 'success')
    return redirect(url_for('main.manufacturer_list'))


# ══════════════════════════════════════════════
#  ДОПОЛНИТЕЛЬНЫЕ ОПЦИИ (привязаны к технике)
# ══════════════════════════════════════════════
@bp.route('/appliances/<int:id>/options')
def extra_option_list(id):
    appliance = Appliance.query.get_or_404(id)
    return render_template('extra_option/list.html', appliance=appliance)


@bp.route('/appliances/<int:id>/options/add', methods=['POST'])
def extra_option_add(id):
    appliance = Appliance.query.get_or_404(id)
    option_name = request.form.get('option', '').strip()
    if option_name:
        # check if already exists
        existing = ExtraOption.query.filter_by(id_model=id, option=option_name).first()
        if existing:
            flash('Такая опция уже существует', 'warning')
        else:
            db.session.add(ExtraOption(id_model=id, option=option_name))
            db.session.commit()
            flash('Опция добавлена', 'success')
    return redirect(url_for('main.extra_option_list', id=id))


@bp.route('/appliances/<int:id>/options/<option>/delete', methods=['POST'])
def extra_option_delete(id, option):
    opt = ExtraOption.query.filter_by(id_model=id, option=option).first_or_404()
    db.session.delete(opt)
    db.session.commit()
    flash('Опция удалена', 'success')
    return redirect(url_for('main.extra_option_list', id=id))


# ══════════════════════════════════════════════
#  ПОСТАВКИ
# ══════════════════════════════════════════════
@bp.route('/supplies')
def supply_list():
    supplies = Supply.query.order_by(Supply.operation_date.desc()).all()
    return render_template('supply/list.html', supplies=supplies)


@bp.route('/supplies/create', methods=['GET', 'POST'])
def supply_create():
    appliances = Appliance.query.order_by(Appliance.name).all()
    if request.method == 'POST':
        s = Supply(
            id_model=request.form['id_model'],
            operation_date=datetime.fromisoformat(request.form['operation_date']),
            unit_price=request.form.get('unit_price', type=float),
            quantity=request.form.get('quantity', type=int),
            supplier=request.form.get('supplier'),
        )
        # Update stock
        app = Appliance.query.get(s.id_model)
        if app:
            app.stock_quantity = (app.stock_quantity or 0) + s.quantity
        db.session.add(s)
        db.session.commit()
        flash('Поставка добавлена', 'success')
        return redirect(url_for('main.supply_list'))
    return render_template('supply/form.html', supply=None, appliances=appliances)


@bp.route('/supplies/<int:id>/edit', methods=['GET', 'POST'])
def supply_edit(id):
    s = Supply.query.get_or_404(id)
    appliances = Appliance.query.order_by(Appliance.name).all()
    if request.method == 'POST':
        old_qty = s.quantity
        s.id_model = request.form['id_model']
        s.operation_date = datetime.fromisoformat(request.form['operation_date'])
        s.unit_price = request.form.get('unit_price', type=float)
        s.quantity = request.form.get('quantity', type=int)
        s.supplier = request.form.get('supplier')
        # Adjust stock
        app = Appliance.query.get(s.id_model)
        if app:
            app.stock_quantity = (app.stock_quantity or 0) - old_qty + s.quantity
        db.session.commit()
        flash('Поставка обновлена', 'success')
        return redirect(url_for('main.supply_list'))
    return render_template('supply/form.html', supply=s, appliances=appliances)


@bp.route('/supplies/<int:id>/delete', methods=['POST'])
def supply_delete(id):
    s = Supply.query.get_or_404(id)
    app = Appliance.query.get(s.id_model)
    if app:
        app.stock_quantity = max(0, (app.stock_quantity or 0) - s.quantity)
    db.session.delete(s)
    db.session.commit()
    flash('Поставка удалена', 'success')
    return redirect(url_for('main.supply_list'))


# ══════════════════════════════════════════════
#  ПРОДАВЦЫ
# ══════════════════════════════════════════════
@bp.route('/sellers')
def seller_list():
    sellers = Seller.query.order_by(Seller.last_name, Seller.first_name).all()
    return render_template('seller/list.html', sellers=sellers)


@bp.route('/sellers/create', methods=['GET', 'POST'])
def seller_create():
    if request.method == 'POST':
        s = Seller(
            first_name=request.form['first_name'],
            last_name=request.form['last_name'],
            email=request.form['email'],
            salary=request.form.get('salary', type=float),
            hire_date=datetime.strptime(request.form['hire_date'], '%Y-%m-%d').date(),
        )
        db.session.add(s)
        db.session.commit()
        flash('Продавец добавлен', 'success')
        return redirect(url_for('main.seller_list'))
    return render_template('seller/form.html', seller=None)


@bp.route('/sellers/<int:id>/edit', methods=['GET', 'POST'])
def seller_edit(id):
    s = Seller.query.get_or_404(id)
    if request.method == 'POST':
        s.first_name = request.form['first_name']
        s.last_name = request.form['last_name']
        s.email = request.form['email']
        s.salary = request.form.get('salary', type=float)
        s.hire_date = datetime.strptime(request.form['hire_date'], '%Y-%m-%d').date()
        db.session.commit()
        flash('Продавец обновлён', 'success')
        return redirect(url_for('main.seller_list'))
    return render_template('seller/form.html', seller=s)


@bp.route('/sellers/<int:id>/delete', methods=['POST'])
def seller_delete(id):
    s = Seller.query.get_or_404(id)
    if s.sales.count() > 0:
        flash('Нельзя удалить продавца с проведёнными продажами', 'danger')
        return redirect(url_for('main.seller_list'))
    db.session.delete(s)
    db.session.commit()
    flash('Продавец удалён', 'success')
    return redirect(url_for('main.seller_list'))


# ══════════════════════════════════════════════
#  ПРОДАЖИ
# ══════════════════════════════════════════════
@bp.route('/sales')
def sale_list():
    sales = Sale.query.order_by(Sale.sale_date.desc()).all()
    return render_template('sale/list.html', sales=sales)


@bp.route('/sales/create', methods=['GET', 'POST'])
def sale_create():
    appliances = Appliance.query.order_by(Appliance.name).all()
    sellers = Seller.query.order_by(Seller.last_name, Seller.first_name).all()
    if request.method == 'POST':
        id_model = request.form['id_model']
        qty = 1
        app = Appliance.query.get(id_model)
        if not app or (app.stock_quantity or 0) < qty:
            flash('Недостаточно товара на складе', 'danger')
            return redirect(url_for('main.sale_create'))

        s = Sale(
            id_model=id_model,
            id_seller=request.form['id_seller'],
            sale_price=request.form.get('sale_price', type=float),
            sale_date=datetime.fromisoformat(request.form['sale_date']),
            warranty_period=request.form.get('warranty_period', type=int),
            coupon_number=request.form.get('coupon_number'),
        )
        app.stock_quantity = (app.stock_quantity or 0) - qty
        db.session.add(s)
        db.session.commit()
        flash('Продажа оформлена', 'success')
        return redirect(url_for('main.sale_list'))
    return render_template('sale/form.html', sale=None, appliances=appliances, sellers=sellers)


@bp.route('/sales/<int:id>/edit', methods=['GET', 'POST'])
def sale_edit(id):
    s = Sale.query.get_or_404(id)
    appliances = Appliance.query.order_by(Appliance.name).all()
    sellers = Seller.query.order_by(Seller.last_name, Seller.first_name).all()
    if request.method == 'POST':
        old_model = s.id_model
        s.id_model = request.form['id_model']
        s.id_seller = request.form['id_seller']
        s.sale_price = request.form.get('sale_price', type=float)
        s.sale_date = datetime.fromisoformat(request.form['sale_date'])
        s.warranty_period = request.form.get('warranty_period', type=int)
        s.coupon_number = request.form.get('coupon_number')

        # Restore stock for old model, deduct for new
        old_app = Appliance.query.get(old_model)
        if old_app:
            old_app.stock_quantity = (old_app.stock_quantity or 0) + 1
        new_app = Appliance.query.get(s.id_model)
        if new_app and (new_app.stock_quantity or 0) >= 1:
            new_app.stock_quantity = (new_app.stock_quantity or 0) - 1
        else:
            flash('Недостаточно товара на складе для новой модели', 'danger')
            return redirect(url_for('main.sale_list'))

        db.session.commit()
        flash('Продажа обновлена', 'success')
        return redirect(url_for('main.sale_list'))
    return render_template('sale/form.html', sale=s, appliances=appliances, sellers=sellers)


@bp.route('/sales/<int:id>/delete', methods=['POST'])
def sale_delete(id):
    s = Sale.query.get_or_404(id)
    # Restore stock
    app = Appliance.query.get(s.id_model)
    if app:
        app.stock_quantity = (app.stock_quantity or 0) + 1
    db.session.delete(s)
    db.session.commit()
    flash('Продажа отменена', 'success')
    return redirect(url_for('main.sale_list'))