from database import db

class ItemModel(db.Model):
    __tablename__ = 'items'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    price = db.Column(db.Float(precision=2))
    store_id = db.Column(db.Integer, db.ForeignKey('stores.id'))
    store = db.relationship('StoreModel')

    def __init__(self, name, price, store_id, _id=None):
        self.id = _id
        self.name = name
        self.price = price
        self.store_id = store_id
    
    def json(self):
        if self.id:
            return {'id': self.id,'name': self.name, 'price': self.price, 'store_id': self.store_id}
        return {'name': self.name, 'price': self.price, 'store_id': self.store_id}
    
    def save(self):
        try:
            db.session.add(self)
            db.session.commit()
        except:
            return {"message": "An error occurred inserting item"}, 500

    
    def delete(self):
        try:
            db.session.delete(self)
            db.session.commit()
        except:
            return {'message': 'An error occurred updating the item'}, 500

    @classmethod
    def find_by_item_name(cls, name):
        return cls.query.filter_by(name=name).first()
    
    @classmethod
    def find_by_item_id(cls, id):
        return cls.query.filter_by(id=id).first()
    
    @classmethod 
    def find_all_items(cls):
        items = cls.query.all()
        return [item.json() for item in items]
        