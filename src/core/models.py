from src import db
from sqlalchemy.dialects.postgresql import ARRAY, VARCHAR
import datetime
from .helper import generate_json_rows

class User(db.Model):

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    created_on = db.Column(db.DateTime, nullable=False)
    is_admin = db.Column(db.Boolean, nullable=False, default=False)

class Adress(db.Model):

    __tablename__ = "adress"

    id = db.Column(db.Integer, primary_key=True)
    city = db.Column(db.String(255), nullable=True)
    country = db.Column(db.String(255), nullable=True)
    number = db.Column(db.String(255), nullable=True)
    other = db.Column(db.String(255), nullable=True)
    state = db.Column(db.String(255), nullable=True)
    street = db.Column(db.String(255), nullable=True)
    zip_code = db.Column(db.String(255), nullable=True)
    pep_id = db.Column(db.Integer, db.ForeignKey("person_info.id"))
    created_on = db.Column(db.DateTime, default=datetime.datetime.now)

    def __init__(self, data: dict):
        for key, val in data.items():
            self.__setattr__(key, val)

    def to_dict(self):
        res = self.__dict__.copy()
        attrs_to_remove = ["pep_id", "created_on", "id", "_sa_instance_state"]
        for attr in attrs_to_remove:
            res.pop(attr)
        return res

class Name(db.Model):

    __tablename__ = "name"

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(255))
    last_name = db.Column(db.String(255))
    middle_name = db.Column(db.String(255))
    name_type = db.Column(db.String(255), default="Primary")
    original_script_name = db.Column(db.String(255))
    whole_name = db.Column(db.String(255))
    pep_id = db.Column(db.Integer, db.ForeignKey("person_info.id"))
    created_on = db.Column(db.DateTime, default=datetime.datetime.now)

    def __init__(self, data: dict):
        for key, val in data.items():
            self.__setattr__(key, val)

    def to_dict(self):
        res = self.__dict__.copy()
        attrs_to_remove = ["pep_id", "created_on", "id", "_sa_instance_state"]
        for attr in attrs_to_remove:
            res.pop(attr)
        return res

class Sanction(db.Model):

    __tablename__ = "sanction"

    id = db.Column(db.Integer, primary_key=True)
    sanction_begin_date = db.Column(db.DateTime)
    sanction_name = db.Column(db.String(255))
    sanction_description = db.Column(db.TEXT)
    pep_id = db.Column(db.Integer, db.ForeignKey("person_info.id"))
    created_on = db.Column(db.DateTime, default=datetime.datetime.now)

    def __init__(self, data: dict):
        for key, val in data.items():
            self.__setattr__(key, val)

    def to_dict(self):
        res = self.__dict__.copy()
        attrs_to_remove = ["pep_id", "created_on", "id", "_sa_instance_state"]
        if (res["sanction_begin_date"]):
            res["saction_begin_date"] = res["sanction_begin_date"].strftime("%Y-%m-%d")
        else:
            res["saction_begin_date"] = res["sanction_begin_date"]

        res.pop("sanction_begin_date")
        for attr in attrs_to_remove:
            res.pop(attr)
        return res

class Identity(db.Model):

    __tablename__ = "identity"

    id = db.Column(db.Integer, primary_key=True)
    identification_value = db.Column(db.String(255))
    identification_type = db.Column(db.String(255))
    pep_id = db.Column(db.Integer, db.ForeignKey("person_info.id"))
    created_on = db.Column(db.DateTime, default=datetime.datetime.now)

    def __init__(self, data: dict):
        for key, val in data.items():
            self.__setattr__(key, val)

    def to_dict(self):
        res = self.__dict__.copy()
        attrs_to_remove = ["pep_id", "created_on", "id", "_sa_instance_state"]
        for attr in attrs_to_remove:
            res.pop(attr)
        return res

class PersonRole(db.Model):

    __tablename__ = "person_role"

    id = db.Column(db.Integer, primary_key=True)
    begin_day = db.Column(db.String(10), nullable=True)
    begin_month = db.Column(db.String(10), nullable=True)
    begin_year = db.Column(db.String(10), nullable=True)
    end_day = db.Column(db.String(10), nullable=True)
    end_month = db.Column(db.String(10), nullable=True)
    end_year = db.Column(db.String(10), nullable=True)
    occupation_title = db.Column(db.String(255))
    role_type = db.Column(db.String(255))
    pep_id = db.Column(db.Integer, db.ForeignKey("person_info.id"))
    created_on = db.Column(db.DateTime, default=datetime.datetime.now)

    def __init__(self, data: dict):
        for key, val in data.items():
            self.__setattr__(key, val)

    def to_dict(self):
        res = self.__dict__.copy()
        attrs_to_remove = ["pep_id", "created_on", "id", "_sa_instance_state"]
        for attr in attrs_to_remove:
            res.pop(attr)
        return res

class Relationship(db.Model):

    __tablename__ = "relationship"

    id = db.Column(db.Integer, primary_key=True)
    relationship_name = db.Column(db.String(255))
    owner_person_id = db.Column(db.Integer, db.ForeignKey("person_info.id"))
    related_person_id = db.Column(db.Integer, db.ForeignKey("person_info.id"))
    created_on = db.Column(db.DateTime, default=datetime.datetime.now)

    def __init__(self, data: dict):
        for key, val in data.items():
            self.__setattr__(key, val)

class Pep(db.Model):

    __tablename__ = "person_info"

    id = db.Column(db.Integer, primary_key=True)
    action = db.Column(db.String(255), nullable=True)
    list_name = db.Column(db.Integer, nullable=True)
    active_status = db.Column(db.String(255), nullable=True)
    deceased = db.Column(db.Boolean, nullable=True)
    gender = db.Column(db.String(255))
    person_type = db.Column(db.String(255))
    profile_notes = db.Column(db.String(255), nullable=True)
    sanction_list_type = db.Column(db.String(255))

    image_url = db.Column(db.String(255), nullable=True)
    birth_place = db.Column(db.String(255), nullable=True)
    birth_date = db.Column(db.DateTime, nullable=True)

    description = db.Column(db.TEXT, nullable=True)

    keyword = db.Column(ARRAY(VARCHAR(255)), nullable=True)
    source_name = db.Column(ARRAY(VARCHAR(255)), nullable=True)
    country_code = db.Column(ARRAY(VARCHAR(10)), nullable=True)
    category = db.Column(ARRAY(VARCHAR(255)), nullable=True)

    names = db.relationship("Name", backref="person_info")
    adresses = db.relationship("Adress", backref="person_info")
    sanctions = db.relationship("Sanction", backref="person_info")
    identities = db.relationship("Identity", backref="person_info")
    roles = db.relationship("PersonRole", backref="person_info")

    created_on = db.Column(db.DateTime, default=datetime.datetime.now)

    def __init__(self, data: dict):
        for key, val in data.items():
            self.__setattr__(key, val)

    def serialize(self):
        citizenship = None
        if self.country_code:
            if len(self.country_code) > 0:
                citizenship = self.country_code[0]
        return {
            "entity_type": self.person_type,
            "birthdate": self.birth_date,
            "birthpalce": self.birth_place,
            "description": self.description,
            "citizenships": citizenship,
            "gender": self.gender,
            "links": self.source_name,
            "photo_link": self.image_url,
            "fullname": self.names[0].whole_name,
            "category": self.category,
            "sanction_list_type": self.sanction_list_type,
            "occupations": [role.occupation_title for role in self.roles],
        }

    @classmethod
    def get_latest(cls, days=1):
        limit = (datetime.datetime.today() - datetime.timedelta(days)).strftime("%Y-%m-%d, %H:%M:%S")
        data = cls.query.filter(cls.created_on > limit).all()
        return generate_json_rows(data)
 
    @classmethod
    def search(cls, fullname, limit):
        query = (
            "SELECT pep_id FROM name ORDER BY SIMILARITY(whole_name, %s) DESC LIMIT %s;"
        )
        res = db.engine.execute(query, (fullname, limit))
        persons = [cls.query.get(item[0]).serialize() for item in res]
        return persons
