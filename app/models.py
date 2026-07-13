from app import db
from datetime import datetime


# ──────────────────────────────────────────────
# C7 — Производители
# ──────────────────────────────────────────────
class Manufacturer(db.Model):
    __tablename__ = 'manufacturers'

    id_manufacturer = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(200), nullable=False)
    legal_address = db.Column(db.String(300), nullable=True)

    # Связь: 1:M → Техника
    appliances = db.relationship('Appliance', back_populates='manufacturer', lazy='dynamic')

    def __repr__(self):
        return f'<Manufacturer {self.name}>'


# ──────────────────────────────────────────────
# C5 — Категории (самоссылочная)
# ──────────────────────────────────────────────
class Category(db.Model):
    __tablename__ = 'categories'

    id_category = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(200), nullable=False)
    parent_category_id = db.Column(db.Integer, db.ForeignKey('categories.id_category'), nullable=True)

    # Самоссылочная связь
    children = db.relationship('Category', backref=db.backref('parent', remote_side=[id_category]), lazy='dynamic')

    # Связь: 1:M → Техника
    appliances = db.relationship('Appliance', back_populates='category', lazy='dynamic')

    def __repr__(self):
        return f'<Category {self.name}>'


# ──────────────────────────────────────────────
# C1 — Техника (Appliance)
# ──────────────────────────────────────────────
class Appliance(db.Model):
    __tablename__ = 'appliances'

    id_model = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(200), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id_category'), nullable=False)
    manufacturer_id = db.Column(db.Integer, db.ForeignKey('manufacturers.id_manufacturer'), nullable=False)
    service_life = db.Column(db.Integer, nullable=True)          # срок службы в месяцах
    stock_quantity = db.Column(db.Integer, default=0)            # количество на складе
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Внешние связи
    category = db.relationship('Category', back_populates='appliances')
    manufacturer = db.relationship('Manufacturer', back_populates='appliances')

    # Связи: 1:M → ДопОпции, Поставка, Продажа
    extra_options = db.relationship('ExtraOption', back_populates='appliance', lazy='dynamic',
                                    cascade='all, delete-orphan')
    supplies = db.relationship('Supply', back_populates='appliance', lazy='dynamic',
                               cascade='all, delete-orphan')
    sales = db.relationship('Sale', back_populates='appliance', lazy='dynamic',
                            cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Appliance {self.name}>'


# ──────────────────────────────────────────────
# C2 — Дополнительные опции (составной PK)
# ──────────────────────────────────────────────
class ExtraOption(db.Model):
    __tablename__ = 'extra_options'

    id_model = db.Column(db.Integer, db.ForeignKey('appliances.id_model'), primary_key=True)
    option = db.Column(db.String(200), primary_key=True)

    # Связь
    appliance = db.relationship('Appliance', back_populates='extra_options')

    def __repr__(self):
        return f'<ExtraOption {self.option} for model {self.id_model}>'


# ──────────────────────────────────────────────
# C4 — Поставка
# ──────────────────────────────────────────────
class Supply(db.Model):
    __tablename__ = 'supplies'

    id_supply = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_model = db.Column(db.Integer, db.ForeignKey('appliances.id_model'), nullable=False)
    operation_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    unit_price = db.Column(db.Float, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    supplier = db.Column(db.String(200), nullable=True)

    # Связь
    appliance = db.relationship('Appliance', back_populates='supplies')

    def __repr__(self):
        return f'<Supply model={self.id_model} qty={self.quantity}>'


# ──────────────────────────────────────────────
# C6 — Продавцы
# ──────────────────────────────────────────────
class Seller(db.Model):
    __tablename__ = 'sellers'

    id_seller = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(200), unique=True, nullable=False)
    salary = db.Column(db.Float, nullable=True)
    hire_date = db.Column(db.Date, nullable=False, default=datetime.utcnow)

    # Связь: 1:M → Продажа
    sales = db.relationship('Sale', back_populates='seller', lazy='dynamic')

    def __repr__(self):
        return f'<Seller {self.first_name} {self.last_name}>'


# ──────────────────────────────────────────────
# C3 — Продажа
# ──────────────────────────────────────────────
class Sale(db.Model):
    __tablename__ = 'sales'

    id_sale = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_model = db.Column(db.Integer, db.ForeignKey('appliances.id_model'), nullable=False)
    id_seller = db.Column(db.Integer, db.ForeignKey('sellers.id_seller'), nullable=False)
    sale_price = db.Column(db.Float, nullable=False)
    sale_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    warranty_period = db.Column(db.Integer, nullable=True)      # срок гарантии в месяцах
    coupon_number = db.Column(db.String(100), nullable=True)

    # Связи
    appliance = db.relationship('Appliance', back_populates='sales')
    seller = db.relationship('Seller', back_populates='sales')

    def __repr__(self):
        return f'<Sale {self.id_sale} model={self.id_model}>'