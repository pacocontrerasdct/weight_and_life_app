from application.models import db, Admin, Weight, Trip
from datetime import datetime as dt

# Create a handler for our read (GET) weights
def read(current_user_):
  """
  This function responds to a request for table 'weights'
  with the complete list of weights
  """
  user_id = current_user_.id

  return Weight.query.filter_by(admin_id=user_id).limit(10).all()

# Create a handler for our insert (POST) weights
def insert(current_user_, weight_, date_):
  """
  This function responds to a request to insert
  a new record into table 'weights' for a logged user
  """
  newWeight = Weight(
              admin_id=current_user_.id,
              created=dt.utcnow(),
              weight=weight_,
              weight_date=date_
              )
  db.session.add(newWeight)
  db.session.commit()
  return True

# Create a handler for update (POST) a weight
def update(weightId_, weight_, date_):
  """
  This function responds to a request to update
  a record from table 'weights' for a logged user
  """
  weight = Weight.query.filter_by(id=weightId_).first()
  weight.weight = weight_
  weight.weight_date = date_
  db.session.commit()
  return True

# Create a handler for edit (POST) a weight
def edit(weightId_):
  """
  This function responds to a request to delete
  a record from table 'weights' for a logged user
  """
  weight = Weight.query.filter_by(id=weightId_).first()
  return weight

# Create a handler for delete (POST) a weight
def delete(weightId_):
  """
  This function responds to a request to delete
  a record from table 'weights' for a logged user
  """
  weight = Weight.query.filter_by(id=weightId_).first()
              
  db.session.delete(weight)
  db.session.commit()
  return True
