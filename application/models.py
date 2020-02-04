from . import db


class Test(db.Model):
    __tablename__ = "test"

    id = db.Column(db.Integer, primary_key=True)
    first = db.Column(db.String(50))

    def __repr__(self):
        return f"<Test {self.id}. {self.first}>"
