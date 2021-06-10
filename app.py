from flask import Flask, redirect, url_for, session
from flask import render_template, request
from flask_debug import Debug
import os, datetime
import bbs_login # ログイン管理モジュール
import bbs_data  # データ入出力用モジュール


# Flaskインスタンスと暗号化キーの指定
app = Flask(__name__)
app.secret_key = 'U1sNMeUkZSuuX2Zn'

# 掲示板のメイン画面
@app.route('/')
def index():
    # ログインが必要
    if not bbs_login.is_login():
        return redirect('/login')
    # ログ一覧を表示
    return render_template('index.html',
            user=bbs_login.get_user(),
            data=bbs_data.load_data())

# 編集画面を表示
@app.route('/edit/<int:id>')
def edit(id):
    # ログインが必要
    if not bbs_login.is_login():
        return redirect('/login')
    # loginユーザと編集レコードのユーザ一致を確認
    loginuser = bbs_login.get_user()
    recorduser = bbs_data.get_recorduser(id)
    if loginuser != recorduser[0]:
        return show_msg('編集できません')
    data=bbs_data.load_record(id)
    return render_template('edit.html',
            user=recorduser[0],
            data=data[0])

# ログイン画面を表示
@app.route('/login')
def login():
    return render_template('login.html')

# ログイン処理
@app.route('/try_login', methods=['POST'])
def try_login():
    user = request.form.get('user', '')
    pw = request.form.get('pw', '')
    # ログインに成功したらルートページへ飛ぶ
    if bbs_login.try_login(user, pw):
        return redirect('/')
    # 失敗した時はメッセージを表示
    return show_msg('ログインに失敗しました')

# ログアウト処理
@app.route('/logout')
def logout():
    bbs_login.try_logout()
    return show_msg('ログアウトしました')

# 書き込み処理
@app.route('/write', methods=['POST'])
def write():
    # ログインが必要
    if not bbs_login.is_login():
        return redirect('/login')
    # フォームのテキストを取得
    ta = request.form.get('ta', '')
    if ta == '': return show_msg('書込が空でした。')
    # データに追記保存
    bbs_data.save_data(
            user=bbs_login.get_user(),
            text=ta)
    return redirect('/')

# 変更処理
@app.route('/edit', methods=['POST'])
def try_edit():
    # ログインが必要
    if not bbs_login.is_login():
        return redirect('/login')
    # フォームを取得
    id = request.form.get('ed-id', '')
    ta = request.form.get('ta', '')
    if ta == '': return show_msg('書込が空でした。')
    # データを変更して保存
    bbs_data.edit_data(
            id=id,
            text=ta)
    return redirect('/')

# 削除処理
@app.route('/delete', methods=['POST'])
def try_delete():
    # ログインが必要
    if not bbs_login.is_login():
        return redirect('/login')
    # フォームを取得
    id = request.form.get('de-id', '')
    # 指定レコードを削除
    bbs_data.delete_data(
            id=id)
    return redirect('/')

# テンプレートを利用してメッセージを出力
def show_msg(msg):
    
    return render_template('msg.html', msg=msg)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

