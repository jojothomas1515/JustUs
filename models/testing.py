from base_model import sess, Base, engine
from  user import User
from friend import Friend
import datetime
Base.metadata.create_all(engine)
print(sess.query(User).all())
# us1 = User(first_name="micheal", last_name='dawn', email='dawn@gmail.com',
#      password='lololo', date_of_birth=datetime.date.today())
# print(sess.add(us1))
# print(sess.commit())
# print(sess.query(User).all())

# fr = Friend(requester_id='1234', requested_id='123467', status='pending', date_of_request=datetime.date.today())
# fr.save()

usr = sess.query(User).filter(User.id == '1234').first()
usr.delete()
print(usr.__str__())