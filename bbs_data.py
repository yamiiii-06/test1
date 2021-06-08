import mysql.connector
import os, datetime

#DB接続
def conn_db():
      conn = mysql.connector.connect(
              host = '127.0.0.1',      #localhostでもOK
              user = 'mysql',
              passwd = 'mysql1234',
              db = 'test1'
      )
      return conn

# DBからデータを読み出す--- (*2)
def load_data():
    sql = 'SELECT * FROM input'
    conn = conn_db()              #ここでDBに接続
    cursor = conn.cursor()       #カーソルを取得
    cursor.execute(sql)             #selectを投げる
    rows = cursor.fetchall()      #selectの結果を全件タプルに格納
    return rows

# ログファイルへ書き出す --- (*3)
#def save_data(data_list):
#    with open(SAVE_FILE, 'wt', encoding='utf-8') as f:
#       json.dump(data_list, f)

# DBへ書き込み --- (*4)
def save_data(user, text):
    conn = conn_db()   #コネクションが切れたときに再接続してくれるように設定
    cursor = conn.cursor()                  #カーソル取得
    # レコードを用意
    tm = get_datetime_now()
    data = (user, text, tm)
    sql = "INSERT INTO input(name,text,date) VALUES(%s,%s,%s)"
    #レコード挿入
    cursor.execute(sql,data)
# 先頭にレコードを追記して保存 --- (*5)
#data_list = load_data()
#data_list.insert(0, data)
#save_data(data_list)

# 日時を文字列で得る
def get_datetime_now():
    now = datetime.datetime.now()
    return "{0:%Y/%m/%d %H:%M}".format(now)
