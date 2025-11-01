from app import db
import enum

class CategoryEnum(enum.Enum):
    ALIMENTACAO = 'Alimentação'
    BEBIDAS = 'Bebidas'
    HIGIENE = 'Higiene'
    LIMPEZA = 'Limpeza'
    PADARIA = 'Padaria'
    ACOUGUE = 'Açougue'
    HORTIFRUTI = 'Hortifruti'
    OUTROS = 'Outros'

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    barcode = db.Column(db.String(128), index=True, unique=True)
    name = db.Column(db.String(128), index=True)
    description = db.Column(db.String(256))
    category = db.Column(db.Enum(CategoryEnum), nullable=False)
    supplier = db.Column(db.String(128))
    cost_price = db.Column(db.Float)
    sale_price = db.Column(db.Float)
    unit_of_measure = db.Column(db.String(32))
    minimum_stock = db.Column(db.Integer)
    expiration_date = db.Column(db.Date)
    quantity = db.Column(db.Integer, default=0)

    def __repr__(self):
        return f'<Product {self.name}>'
