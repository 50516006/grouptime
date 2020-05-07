# -*- coding: utf-8 -*-
from grouptime.models import *
from grouptime.database import *
import getpass
#ユーザー制御用スクリプト
def create_user():
    print("input new user name")
    name = input()

    passwd = getpass.getpass(prompt="input password")
    validate_passwd  = getpass.getpass(prompt="input password one more")
    if passwd==validate_passwd:
        new_user = User(name,passwd)
        db_session.add(new_user)
        db_session.commit()
        print(new_user.id,new_user.name,"is created")

def delete_user():
    show_users()
    print("Select user by id")
    id = int(input())
    target = User.query.filter_by(id = id).first()
    print("You are going to delete {0}:{1}. Ok? (y,n)".format(target.id,target.name))
    if input()=='y' and not target is None:
        db_session.delete(target)
        db_session.commit()

def chpw():
    show_users()
    print("Select user-id which you want to change password.")
    id = int(input())
    target= User.query.filter_by(id = id).first()
    print("You are going to change ({0}:{1})'s password . Ok? (y,n)".format(target.id,target.name))
    if input() != 'y':
        print("canceled")
        return
    if target is None:
        print('you selected user who does not exist')
        return
    passwd = getpass.getpass(prompt="input password")
    validate_passwd  = getpass.getpass(prompt="input password one more")
    if passwd==validate_passwd:
        target.salt = urandom(64)
        target.hash_passwd=pbkdf2_hmac('sha256',passwd.encode('utf-8'),target.salt,100000)
        

        db_session.commit()
        print(target.id,target.name,"'s password is created")



    

def show_users():
    print("id,name")
    print("\n".join([ "{0},{1}".format(i.id,i.name)   for i in User.query.all()]))