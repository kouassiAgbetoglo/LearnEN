from config import db, ma


class Word(db.Model):
    __tablename__ = "WORDS"
    word_id = db.Column(db.Integer, primary_key=True)
    en_translation = db.Column(db.String(32))
    fr_translation = db.Column(db.String(32))
    
class WordSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Word
        load_instance = True
        sqla_session = db.session


