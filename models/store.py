from database import db

class StoreModel(db.Model):
    __tablename__ = 'stores'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    items = db.relationship('ItemModel', lazy="dynamic")

    def __init__(self, name, _id=None):
        self.id = _id
        self.name = name
    
    def json(self):
        if self.id:
            return {'id': self.id,'name': self.name, 'items': [item.json() for item in self.items.all()]}
        return {'name': self.name, 'items': [item.json() for item in self.items.all()] }
    
    def save(self):
        try:
            db.session.add(self)
            db.session.commit()
        except:
            return {"message": "An error occurred while creating the store."}, 500

    
    def delete(self):
        try:
            db.session.delete(self)
            db.session.commit()
        except:
            return {'message': 'An error occurred deleting the store'}, 500

    @classmethod
    def find_by_store_name(cls, name):
        return cls.query.filter_by(name=name).first()
    
    @classmethod
    def find_by_store_id(cls, id):
        return cls.query.filter_by(id=id).first()
    
    @classmethod 
    def find_all_stores(cls):
        stores = cls.query.all()
        return [store.json() for store in stores]
        