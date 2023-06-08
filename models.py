from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Total_Experiments(db.Model):
  __tablename__ = 'total_experiments'
  user_id = db.Column(db.Integer, unique=True, nullable=False, primary_key=True)
  number_of_experiments = db.Column(db.Integer, nullable=False)

class Average_Experiments(db.Model):
  __tablename__ = 'average_experiments'
  id = db.Column(db.Integer, primary_key=True)
  average_experiments = db.Column(db.Float, nullable=False)

class Most_Commonly_Experimented_Compound(db.Model):
  __tablename__ = 'most_commonly_experimented_compound'
  id = db.Column(db.Integer, primary_key=True)
  most_commonly_experimented_compound = db.Column(db.String(100), nullable=False)