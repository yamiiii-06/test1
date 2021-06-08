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


# 掲示板データ読み込み
def load_data():
    conn = conn_db()            #DB接続
    cursor = conn.cursor()      #カーソルを取得   
    sql = 'SELECT * FROM input'
    cursor.execute(sql)         #実行
    rows = cursor.fetchall()    #結果を全件タプルに格納
    cursor.close()              #カーソル終了
    conn.close()                #DB切断
    return rows

# 指定レコード読み込み
def load_record(id):
    conn = conn_db()            #DB接続
    cursor = conn.cursor()      #カーソルを取得   
    sql = 'SELECT * FROM input WHERE id=%s'
    cursor.execute(sql, [id])     #実行
    rows = cursor.fetchall()    #結果を全件タプルに格納
    cursor.close()              #カーソル終了
    conn.close()                #DB切断
    return rows

# 書き込みデータをinputテーブルへ書き込み
def save_data(user, text):
    try:
        conn = conn_db()            #DB接続
        cursor = conn.cursor()      #カーソル取得
        # レコードを用意
        tm = get_datetime_now()
        data = (user, text, tm)
        sql = "INSERT INTO input(name,text,date) VALUES(%s,%s,%s)"
        cursor.execute(sql,data)    #実行
        conn.commit()               #コミット
    except:
        print('例外発生')
    else:
        print('')
    finally:
        cursor.close()              #カーソル終了
        conn.close()                #DB切断

# レコードのユーザ確認
def get_recorduser(id):
    conn = conn_db()            #DB接続
    cursor = conn.cursor()      #カーソルを取得   
    sql = 'SELECT name FROM input WHERE id=%s'
    cursor.execute(sql, [id])     #実行
    rows = cursor.fetchall()    #結果を全件タプルに格納
    cursor.close()              #カーソル終了
    conn.close()                #DB切断
    return rows[0]


# 日時を文字列で得る
def get_datetime_now():
    now = datetime.datetime.now()
    return "{0:%Y/%m/%d %H:%M}".format(now)
