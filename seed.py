"""Скрипт инициализации БД — создаёт таблицы и наполняет тестовыми данными."""

from app import create_app, db
from app.models import (
    Category, Manufacturer, Appliance,
    ExtraOption, Supply, Seller, Sale
)
from datetime import datetime, date


def seed():
    app = create_app()
    with app.app_context():
        db.drop_all()
        db.create_all()

        # ── Категории (C5) ──────────────────────────
        cat_electronics = Category(name='Электроника')
        cat_computers = Category(name='Компьютеры', parent=cat_electronics)
        cat_laptops = Category(name='Ноутбуки', parent=cat_computers)
        cat_smartphones = Category(name='Смартфоны', parent=cat_electronics)
        cat_audio = Category(name='Аудиотехника', parent=cat_electronics)
        db.session.add_all([cat_electronics, cat_computers, cat_laptops, cat_smartphones, cat_audio])

        # ── Производители (C7) ──────────────────────
        mfr_apple = Manufacturer(name='Apple Inc.', legal_address='1 Apple Park Way, Cupertino, CA')
        mfr_samsung = Manufacturer(name='Samsung Electronics', legal_address='129 Samsung-ro, Suwon, South Korea')
        mfr_lenovo = Manufacturer(name='Lenovo Group', legal_address='6 Changi Business Park, Singapore')
        mfr_sony = Manufacturer(name='Sony Corporation', legal_address='1-7-1 Konan, Minato-ku, Tokyo')
        db.session.add_all([mfr_apple, mfr_samsung, mfr_lenovo, mfr_sony])

        # ── Техника (C1) ────────────────────────────
        app_mbp = Appliance(name='MacBook Pro 14" M3', category=cat_laptops, manufacturer=mfr_apple,
                            service_life=60, stock_quantity=12)
        app_galaxy = Appliance(name='Samsung Galaxy S24', category=cat_smartphones, manufacturer=mfr_samsung,
                               service_life=36, stock_quantity=30)
        app_thinkpad = Appliance(name='Lenovo ThinkPad X1 Carbon', category=cat_laptops, manufacturer=mfr_lenovo,
                                 service_life=48, stock_quantity=8)
        app_wh1000 = Appliance(name='Sony WH-1000XM5', category=cat_audio, manufacturer=mfr_sony,
                               service_life=24, stock_quantity=25)
        app_iphone = Appliance(name='iPhone 15 Pro', category=cat_smartphones, manufacturer=mfr_apple,
                               service_life=36, stock_quantity=20)
        db.session.add_all([app_mbp, app_galaxy, app_thinkpad, app_wh1000, app_iphone])

        # ── Дополнительные опции (C2) ───────────────
        opts = [
            ExtraOption(id_model=1, option='Garantia extendida 3 años'),
            ExtraOption(id_model=1, option='Teclado retroiluminado'),
            ExtraOption(id_model=1, option='Cargador USB-C 96W'),
            ExtraOption(id_model=2, option='Cargador inalámbrico'),
            ExtraOption(id_model=2, option='Funda de silicona'),
            ExtraOption(id_model=3, option='Docking Station USB-C'),
            ExtraOption(id_model=4, option='Estuche de transporte'),
            ExtraOption(id_model=5, option='AppleCare+ 2 años'),
        ]
        db.session.add_all(opts)

        # ── Поставки (C4) ───────────────────────────
        supplies = [
            Supply(id_model=1, operation_date=datetime(2026, 1, 15), unit_price=1800.0, quantity=10, supplier='Apple Distributor GmbH'),
            Supply(id_model=2, operation_date=datetime(2026, 2, 10), unit_price=750.0, quantity=25, supplier='Samsung C&T'),
            Supply(id_model=3, operation_date=datetime(2026, 3, 5), unit_price=1450.0, quantity=5, supplier='Lenovo EMEA'),
            Supply(id_model=4, operation_date=datetime(2026, 3, 20), unit_price=280.0, quantity=20, supplier='Sony Logistics'),
            Supply(id_model=1, operation_date=datetime(2026, 4, 1), unit_price=1750.0, quantity=5, supplier='Apple Distributor GmbH'),
            Supply(id_model=5, operation_date=datetime(2026, 5, 12), unit_price=1100.0, quantity=15, supplier='Apple Distributor GmbH'),
            Supply(id_model=2, operation_date=datetime(2026, 6, 1), unit_price=720.0, quantity=10, supplier='Samsung C&T'),
        ]
        db.session.add_all(supplies)

        # ── Продавцы (C6) ───────────────────────────
        sellers = [
            Seller(first_name='Иван', last_name='Петров', email='ivan.petrov@shop.ru', salary=65000.0, hire_date=date(2024, 3, 1)),
            Seller(first_name='Мария', last_name='Сидорова', email='maria.sidorova@shop.ru', salary=72000.0, hire_date=date(2023, 11, 15)),
            Seller(first_name='Алексей', last_name='Кузнецов', email='alexey.kuznetsov@shop.ru', salary=58000.0, hire_date=date(2025, 1, 10)),
        ]
        db.session.add_all(sellers)

        # ── Продажи (C3) ────────────────────────────
        sales = [
            Sale(id_model=1, id_seller=1, sale_price=2199.0, sale_date=datetime(2026, 4, 10), warranty_period=24, coupon_number='WRN-001'),
            Sale(id_model=2, id_seller=2, sale_price=899.0, sale_date=datetime(2026, 4, 15), warranty_period=12, coupon_number='WRN-002'),
            Sale(id_model=5, id_seller=2, sale_price=1399.0, sale_date=datetime(2026, 5, 5), warranty_period=24, coupon_number='WRN-003'),
            Sale(id_model=4, id_seller=3, sale_price=349.0, sale_date=datetime(2026, 5, 20), warranty_period=12, coupon_number='WRN-004'),
            Sale(id_model=3, id_seller=1, sale_price=1799.0, sale_date=datetime(2026, 6, 1), warranty_period=36, coupon_number='WRN-005'),
            Sale(id_model=1, id_seller=3, sale_price=2099.0, sale_date=datetime(2026, 6, 15), warranty_period=24, coupon_number='WRN-006'),
        ]
        db.session.add_all(sales)

        db.session.commit()
        print('[OK] База данных создана и наполнена тестовыми данными.')
        print(f'   Таблицы: {list(db.metadata.tables.keys())}')
        print(f'   Категорий:     {Category.query.count()}')
        print(f'   Производителей: {Manufacturer.query.count()}')
        print(f'   Техники:       {Appliance.query.count()}')
        print(f'   Доп. опций:    {ExtraOption.query.count()}')
        print(f'   Поставок:      {Supply.query.count()}')
        print(f'   Продавцов:     {Seller.query.count()}')
        print(f'   Продаж:        {Sale.query.count()}')


if __name__ == '__main__':
    seed()