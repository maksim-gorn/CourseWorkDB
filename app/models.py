from app import db
from datetime import datetime

# производители - компании, которые выпускают технику
class Manufacturer(db.Model):
    __tablename__ = 'manufacturers'

    id_manufacturer = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(200), nullable=False)
    legal_address = db.Column(db.String(300), nullable=True)

    # один производитель может иметь много моделей техники, связь 1:M
    appliances = db.relationship('Appliance', back_populates='manufacturer', lazy='dynamic')

    def __repr__(self):
        return f'<Manufacturer {self.name}>'


# категории - иерархия для группировки техники, могут быть вложенными (родитель-ребёнок)
class Category(db.Model):
    __tablename__ = 'categories'

    id_category = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(200), nullable=False)
    # ссылка на родительскую категорию, null если это корневая категория
    parent_category_id = db.Column(db.Integer, db.ForeignKey('categories.id_category'), nullable=True)

    # самоссылочная связь - категория может иметь подкатегории
    children = db.relationship('Category', backref=db.backref('parent', remote_side=[id_category]), lazy='dynamic')

    # одна категория может содержать много единиц техники, связь 1:M
    appliances = db.relationship('Appliance', back_populates='category', lazy='dynamic')

    def __repr__(self):
        return f'<Category {self.name}>'


# техника - основная таблица, хранит информацию о моделях
class Appliance(db.Model):
    __tablename__ = 'appliances'

    id_model = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(200), nullable=False)
    # внешний ключ на категорию
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id_category'), nullable=False)
    # внешний ключ на производителя
    manufacturer_id = db.Column(db.Integer, db.ForeignKey('manufacturers.id_manufacturer'), nullable=False)
    # срок службы в месяцах
    service_life = db.Column(db.Integer, nullable=True)
    # сколько штук сейчас на складе
    stock_quantity = db.Column(db.Integer, default=0)
    # дата последнего обновления
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # связь с категорией - техника принадлежит одной категории
    category = db.relationship('Category', back_populates='appliances')
    # связь с производителем - техника выпущена одним производителем
    manufacturer = db.relationship('Manufacturer', back_populates='appliances')

    # одна модель может иметь несколько доп. опций
    extra_options = db.relationship('ExtraOption', back_populates='appliance', lazy='dynamic',
                                    cascade='all, delete-orphan')
    # одна модель может быть поставлена много раз
    supplies = db.relationship('Supply', back_populates='appliance', lazy='dynamic',
                               cascade='all, delete-orphan')
    # одна модель может быть продана много раз
    sales = db.relationship('Sale', back_populates='appliance', lazy='dynamic',
                            cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Appliance {self.name}>'


# дополнительные опции, которые можно добавить к конкретной модели техники
# первичный ключ составной: id_модели + название опции
class ExtraOption(db.Model):
    __tablename__ = 'extra_options'

    # внешний ключ на технику, часть составного pk
    id_model = db.Column(db.Integer, db.ForeignKey('appliances.id_model'), primary_key=True)
    # название опции, часть составного pk
    option = db.Column(db.String(200), primary_key=True)

    # каждая опция привязана к одной модели техники
    appliance = db.relationship('Appliance', back_populates='extra_options')

    def __repr__(self):
        return f'<ExtraOption {self.option} for model {self.id_model}>'


# поставки - учёт того, когда и сколько техники привезли от поставщиков
class Supply(db.Model):
    __tablename__ = 'supplies'

    # отдельный суррогатный первичный ключ
    id_supply = db.Column(db.Integer, primary_key=True, autoincrement=True)
    # внешний ключ на технику - какая модель пришла
    id_model = db.Column(db.Integer, db.ForeignKey('appliances.id_model'), nullable=False)
    # когда была поставка
    operation_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    # цена за одну штуку
    unit_price = db.Column(db.Float, nullable=False)
    # сколько штук привезли
    quantity = db.Column(db.Integer, nullable=False)
    # от кого пришла поставка
    supplier = db.Column(db.String(200), nullable=True)

    # каждая поставка относится к одной модели техники
    appliance = db.relationship('Appliance', back_populates='supplies')

    def __repr__(self):
        return f'<Supply model={self.id_model} qty={self.quantity}>'


# продавцы - сотрудники, которые оформляют продажи
class Seller(db.Model):
    __tablename__ = 'sellers'

    id_seller = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(200), unique=True, nullable=False)
    # зарплата сотрудника
    salary = db.Column(db.Float, nullable=True)
    # когда приняли на работу
    hire_date = db.Column(db.Date, nullable=False, default=datetime.utcnow)

    # один продавец может провести много продаж, связь 1:M
    sales = db.relationship('Sale', back_populates='seller', lazy='dynamic')

    def __repr__(self):
        return f'<Seller {self.first_name} {self.last_name}>'


# продажи - информация о фактах продажи техники
class Sale(db.Model):
    __tablename__ = 'sales'

    id_sale = db.Column(db.Integer, primary_key=True, autoincrement=True)
    # внешний ключ на технику - что продали
    id_model = db.Column(db.Integer, db.ForeignKey('appliances.id_model'), nullable=False)
    # внешний ключ на продавца - кто продал
    id_seller = db.Column(db.Integer, db.ForeignKey('sellers.id_seller'), nullable=False)
    # цена продажи
    sale_price = db.Column(db.Float, nullable=False)
    # когда продали
    sale_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    # срок гарантии в месяцах
    warranty_period = db.Column(db.Integer, nullable=True)
    # номер гарантийного талона
    coupon_number = db.Column(db.String(100), nullable=True)

    # каждая продажа относится к одной модели техники
    appliance = db.relationship('Appliance', back_populates='sales')
    # каждая продажа совершена одним продавцом
    seller = db.relationship('Seller', back_populates='sales')

    def __repr__(self):
        return f'<Sale {self.id_sale} model={self.id_model}>'
