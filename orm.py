from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from flask import Flask, request, jsonify
from flask_marshmallow import Marshmallow

app = Flask(__name__)
ma = Marshmallow(app)
engine = create_engine('sqlite:///clientDatabase.sqlite', echo=True)
Base = declarative_base()
Session = sessionmaker()
Session.configure(bind=engine)
session = Session()

class Client(Base):
    __tablename__ = "client"
    id = Column('id', Integer, primary_key=True)
    name = Column('name', String)
    email = Column('email', String, unique=True)

    def __init__(self, name, email):
        self.name = name
        self.email = email

#Client Schema
class ClientSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'email')

#initialize schema. this helps serialization
client_schema = ClientSchema()
clients_schema = ClientSchema(many=True)

#Home route
@app.route("/")
def home():
    return "Hello"

#Creates a new user
@app.route('/register', methods=['POST'])
def new_user():
    if request.content_type == 'application/json':
        data = request.get_json()
        name = data.get('name')
        email = data.get('email')

        reg = Client(name, email)
        session.add(reg)
        session.commit()
        return client_schema.jsonify(reg)
    return jsonify('Something went wrong')

#Get all client data
@app.route('/getClient', methods=['GET'])
def clients_data():

    all_data = session.query(Client).all()
    result = clients_schema.dump(all_data)
    return jsonify(result)

Base.metadata.create_all(engine)
if __name__ == "__main__":
    app.run(debug=True)
