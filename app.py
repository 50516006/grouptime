# -*- coding: utf-8 -*-
from collections import defaultdict
from datetime import datetime

from flask import Flask, Response, abort, render_template,request,redirect,jsonify
from flask_login import (LoginManager, UserMixin, login_required, login_user,
                         logout_user,current_user)



from grouptime.database import db_session
from grouptime.models import Group,User




app = Flask(__name__)
app.config["DEBUG"] = True
app.secret_key='ultra_super_secret_key'
login_manager = LoginManager()
login_manager.init_app(app)

login_manager.login_view='login'


#リスト表示のメイン画面
@app.route("/")
def index():

    return (render_template("index.html"))

#idに対応したグループを詳細表示する
@app.route("/<id>")
def show_content(id):
    content = Group.query.filter_by(id=id).first()
    if content is None:
        abort(404)
    return render_template("show_content.html", content=content)

#idに対応するグループを作成する
@app.route("/api/set/<id>")
@login_required
def setter(id):
    if not id.isdecimal():
        return '不正な入力です'
    
    content = Group.query.filter_by(id=id).first()
    if content is None:
        nc = Group(id)
        db_session.add(nc)
        db_session.commit()
        return "追加成功"
    else:
        return "既存"

#idに対応するグループを削除する
@app.route("/api/remove/<id>")
@login_required
def remover(id):
    if not id.isdecimal():
        return '不正な入力です'
    content = Group.query.filter_by(id=id).first()
    if content is None:
        return "存在しない"
    else:
        db_session.delete(content)
        db_session.commit()
        return "削除成功"

#すべてのグループを削除する
@app.route("/api/all_delete")
@login_required
def all_delete():
    contents = Group.query.all()
    for i in contents:
        db_session.delete(i)
    db_session.commit()
    return ("全削除成功")

#リストの部分だけを返す
@app.route("/api/contents")
def get_content():

    contents = Group.query.all()
    contents.sort(key=lambda i: i.time)
    return (render_template("contents.html", contents=contents))


#ログインページ
@app.route('/auth/login',methods=['GET'])
def login_get():
    return render_template('login.html')

#ログインページ(処理実行)
@app.route('/auth/login',methods=['POST'])
def login_post():
    id=int(request.form.get('id'))
    name = request.form.get('name')
    passwd = request.form.get('passwd')
    remember = True if request.form.get('remember') else False
    user=User.query.filter_by(id=id).first()
    if user.is_collect(name,passwd):
        login_user(user,remember=remember)
        return redirect('/')    
    else:
        return("login.html")

#ログインできているか確認
@app.route('/auth/test')
@login_required
def is_login():
    return('OK! You Are '+current_user.name)

#ログアウトページ
@app.route('/auth/logout')
@login_required
def logout():
    logout_user()
    return('OK! Logout!')

#idでユーザーを探す
@login_manager.user_loader
def load_user(user_id):
    return User.query.filter_by(id=user_id).first()



if __name__ == "__main__":
    app.run(host='0.0.0.0', port=9080)
