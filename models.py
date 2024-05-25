from main import db

class Campeonato(db.Model):
    __tablename__ = "Campeonatos"
    div = db.Column(db.String(3), primary_key = True, nullable = False)
    ano = db.Column(db.Integer, primary_key = True, nullable = False)
    regiao = db.Column(db.String(20))
    nome = db.Column(db.String(50))

    def __repr__(self):
        return f"Campeonato(div={self.div!r}, ano={self.ano!r}, regiao={self.regiao!r}, nome={self.nome!r})"

class Times(db.Model):
    __tablename__ = "Times"
    nome = db.Column(db.String(50), primary_key = True, nullable = False)

    def __repr__(self):
        return f"Times(nome={self.nome!r})"
    
class TPC(db.Model):
    __tablename__ = "Times por Campeonato"
    CampAno = db.Column(db.Integer, primary_key = True, nullable = False)
    Div = db.Column(db.String(3), primary_key = True, nullable = False)
    Time = db.Column(db.String(50), primary_key = True, nullable = False)

    def __repr__(self):
        return f"TPC(CampAno = {self.CampAno!r}, Div = {self.Div!r}, Time = {self.Time!r})"




