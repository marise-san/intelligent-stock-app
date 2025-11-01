from app import db
from datetime import datetime

class StockMovement(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    movement_type = db.Column(db.String(32), nullable=False)  # 'entrada', 'saída', 'ajuste'
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def __repr__(self):
        return f'<StockMovement {self.product_id} {self.movement_type} {self.quantity}>'
