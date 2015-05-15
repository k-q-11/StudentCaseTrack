from project import mydb
from project.models import User, Case, Student
# create the database and the table
mydb.create_all()

mydb.session.add(User('Henrik Bechmann', 'hebec@dtu.dk', '123456'))

#mydb.session.add(Case('1', 'Bo', '1'))
#mydb.session.add(Case('2', 'Pia', '2'))

mydb.session.commit()