from werkzeug.security import \
    (generate_password_hash, check_password_hash)
from sqlalchemy import \
    (and_, or_, text, desc, asc)
import variables as v
from flask import make_response, request

from flask_login import UserMixin

def getPatients():
    """Devuelve la lista de pacientes
    
    Returns:
        lista de pacientes -- lista de los pacientes en la base de datos
    """
    return User.query.filter(User.utype=="2").all()


def getPatient(idu):
    return load_user(idu)

def getEvaluation(idu):
    return Evolution.query.filter(Evolution.idu==idu).order_by(Evolution.date.desc()).limit(2).all()

def getEvaluations(idu):
    return Evolution.query.filter(Evolution.idu==idu).order_by(Evolution.date.asc()).all()

def loadAllEvolution(idu):
    return Evolution.query.filter(Evolution.idu==idu).order_by(desc(Evolution.date)).all()

def loadData(idu, date):
    return Evolution.query.filter(and_(Evolution.idu==idu, Evolution.date==date)).first()

def howManyData(idu):
    return Evolution.query.filter(Evolution.idu == idu).count()


@v.login_manager.user_loader
def load_user(user_id):
    """Get user by id.

    Arguments:
        user_id {int} -- user identificator.

    Returns:
        User -- User with that id.
    """
    return User.query.get(user_id)


usr_vid = v.db.Table("usr_vid", v.db.Model.metadata,
                     v.db.Column("idu", v.db.Integer, v.db.ForeignKey("User.idu")),
                     v.db.Column("idv", v.db.Integer, v.db.ForeignKey("Videos.idv")))


class User(v.db.Model, UserMixin):

    __tablename__ = "Users"

    idu = v.db.Column(v.db.Integer, primary_key=True)
    identity_name = v.db.Column(v.db.Text, unique=True, index=True)
    utype = v.db.Column(v.db.Integer)
    name = v.db.Column(v.db.String(25))
    password = v.db.Column(v.db.String(128))
    token = v.db.Column(v.db.String(128), unique=True, index=True)

    def __init__(self, identity_name, utype, name, password, token):
        self.identity_name = identity_name
        self.utype = utype
        self.name = name
        self.set_password(password)
        self.token = token

    def get_id(self):
        return self.idu

    def set_password(self, password):
        self.password = generate_password_hash(password)
        v.db.session.commit()

    def check_password(self, password):
        return check_password_hash(self.password, password)

    @property
    def is_authenticated(self):
        tkn = request.cookies.get('token')
        if tkn == self.token:
            return True
        return False

    def __str__(self):
        return self.identity_name+" token:"+self.token


class Videos(v.db.Model):

    __tablename__ = "Videos"

    idv = v.db.Column(v.db.Integer, primary_key=True)
    name = v.db.Column(v.db.Text)
    url = v.db.Column(v.db.Text)

    def __init__(self, name, url):
        self.name = name
        self.url = url


class Evolution(v.db.Model):

    __tablename__ = "Evolution"

    idu = v.db.Column(v.db.Integer, primary_key=True)
    date = v.db.Column(v.db.Integer, primary_key=True)
    data = v.db.Column(v.db.Integer)

    def __init__(self, idu, date, data):
        self.idu = idu
        self.date = date
        self.data = data
