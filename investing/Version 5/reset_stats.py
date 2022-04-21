import os

user_list = os.listdir('users')


for user in user_list:
    file = open(user, 'w')

    file.close()