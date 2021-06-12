from app import db

class Aparelho(db.Model):
    #Classe Aparelho para criação do banco de dados sqlite3
    
    __tablename__ = "aparelhos"
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(80), unique=False, nullable=False)
    comodo = db.Column(db.String(120), unique=False, nullable=False)
    ip = db.Column(db.String(120), unique=False, nullable=False)
    consumo = db.Column(db.Integer, unique=False, nullable=False)
    
    def __repr__(self):
        return '<Aparelho %r>' % self.nome

class Sensor(db.Model):
    #Classe sensor para criação do banco de dados sqlite3
    __tablename__ = "sensores"
    id = db.Column(db.Integer, primary_key=True)
    comodo = db.Column(db.String(120), unique=False, nullable=False)
    temp = db.Column(db.Float, unique=False, nullable=False)
     
    def __repr__(self):
        return '<Sensor %r>' % self.nome
