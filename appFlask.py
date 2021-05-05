from flask import Flask, request
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

class DatabaseMeteo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ville = db.Column(db.String(100), nullable=False)
    temperature = db.Column(db.Integer, nullable=False)
    humidite = db.Column(db.Integer, nullable=False)
    
#db.create_all() 

meteo_put_args = reqparse.RequestParser()
meteo_put_args.add_argument("ville", type=str, help="Nom de la ville", required=True)
meteo_put_args.add_argument("temperature", type=int, help="Temperature de la ville", required=True)
meteo_put_args.add_argument("humidite", type=int, help="Humidite de la ville", required=True)

modelChamps = {
    'id': fields.Integer,
    'ville':fields.String,
    'temperature': fields.Integer,
    'humidite': fields.Integer,
    }

    
class maBase(Resource):
  @marshal_with(modelChamps)
  def get(self, id_meteo):
      resultat = DatabaseMeteo.query.filter_by(id=id_meteo).first()
      if not resultat:
          abort(404, message="Probleme")
      return resultat 

  @marshal_with(modelChamps) 
  def put(self, id_meteo):
      args = meteo_put_args.parse_args()
      resultat = DatabaseMeteo.query.filter_by(id=id_meteo).first()
      if resultat:
          abort(409, message="Probleme")
          
      meteo = DatabaseMeteo(id=id_meteo, ville=args['ville'],temperature=args['temperature'], humidite=args['humidite'])
      db.session.add(meteo)
      db.session.commit()
      return meteo, 201
    
  def delete(self, id_meteo):
      resultat = DatabaseMeteo.query.filter_by(id=id_meteo).first()
      if not resultat:
          abort(404, message="Probleme")
      db.session.delete(resultat)
      db.session.commit()
      return "", 204

api.add_resource(maBase, "/mabase/<int:id_meteo>")


if __name__ == "__main__":
  app.run(host='10.0.0.36', port=5000)
