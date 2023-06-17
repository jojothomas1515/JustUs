from base_model import sess
from  user import User
import datetime
print(sess.query(User).all())
us1 = User(id="1234", first_name="jojo", last_name='thomas', email='jojothomas1515@gmail.com',
     password='lololo', date_of_birth=datetime.date.today())
print(sess.add(us1))
print(sess.commit())
print(sess.query(User).all())