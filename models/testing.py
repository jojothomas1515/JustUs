from models.friend import Friend


# print(sess.query(User).all())
# sess.close()
# print(sess.info)
# us1 = User(first_name="micheal", last_name='dawn', email='dawn@gmail.com',
#      password='lololo', date_of_birth=datetime.date.today())
# print(sess.add(us1))
# print(sess.commit())
# print(User.get('email', 'jojothomas1515@gmail.com'))
# for i in User.all():
#     print(i)

# fr = Friend(requester_id='1234', requested_id='123467', status='pending', date_of_request=datetime.date.today())
# fr.save()

# usr = sess.query(User).filter(User.id == '1234').first()
# usr.delete()
# print(usr.__str__())

def print_param(*one):
    print(*one)


user_1 = "3afc9e6e-99ed-4a70-9c6f-b1a1a4e7b725"
user_2 = "744f79a2-5bab-47f1-a4d6-11d0c412c6c6"
print(Friend.filter_one(
    ((Friend.requester_id == user_2) &
    (Friend.requested_id == user_1)) |
    ((Friend.requester_id == user_1) &
    (Friend.requested_id == user_2))
))
# print(Friend.get("requested_id", user_2))

# todo: delete this file
