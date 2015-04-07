from views import mydb
from models import User, Case
# create the database and the table
mydb.create_all()

mydb.session.add(User('KevinQ', 'k_q_11@zoho.com', '123456'))

#mydb.session.add(Case('1', 'Bo', '1'))
#mydb.session.add(Case('2', 'Pia', '2'))

mydb.session.commit()