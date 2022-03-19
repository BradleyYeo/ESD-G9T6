from database import db


class ContinuousResource(db.Model):
    __tablename__ = "inventory"

    id = db.Column(db.String(36), primary_key=True, unique=True)
    product_name = db.Column(db.String(36), primary_key=False, unique=True)  # orange juice
    quantity = db.Column(db.Integer(6), primary_key=False, unique=False)  # 3
    price = db.Column(db.Integer(6), primary_key=False, unique=False)

    allocations = db.relationship("ContinuousResourceAllocation")

