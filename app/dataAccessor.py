import sqlite3
from contextlib import closing
from . import MemberList


# データベース、テーブルを作成する
def create_table():
    dbname = 'IdolRecommendWebDB'
    with closing(sqlite3.connect(dbname)) as conn:
        c = conn.cursor()
        # テーブル削除
        c.execute('drop table if exists member')
        c.execute('drop table if exists evaluation')
        # テーブル作成
        create_member_table = '''create table if not exists member(id integer primary key autoincrement, name text, 
        group_name text, twitter_id text, instagram_id text)'''
        c.execute(create_member_table)
        create_evaluation_table = '''create table if not exists evaluation(id integer primary key autoincrement)'''
        c.execute(create_evaluation_table)
        # 値設定
        insert_member_sql = '''insert into member(name,group_name) values(?,?)'''
        # add_column_to_evaluation = ''' alter table evaluation add column ? [ int]'''
        for group in MemberList.groupList:
            for i in range(len(group)):
                if i == 0:
                    continue
                c.execute(insert_member_sql, (group[i], group[0]))
                c.execute(' alter table evaluation add column ' + str(group[i]) + ' [ int]')
        conn.commit()


# グループを追加する
# グループは[group_name,name1,name2,……]のList型groupで与えられる
def add_group_dao(group):
    for i in range(len(group)):
        if i == 0:
            continue
        add_member_dao(group[i], group[0])


# メンバーを追加する
def add_member_dao(name, group_name):
    dbname = 'IdolRecommendWebDB'
    with closing(sqlite3.connect(dbname)) as conn:
        c = conn.cursor()
        # 値設定
        insert_member_sql = '''insert into member(name,group_name) values(?,?)'''
        c.execute(insert_member_sql, (name, group_name))
        c.execute(' alter table evaluation add column ' + str(name) + ' [ int]')
        conn.commit()


# ユーザの評価行を作成
# ユーザの行をidとして返す
def add_evaluationRow_dao():
    dbname = 'IdolRecommendWebDB'
    with closing(sqlite3.connect(dbname)) as conn:
        c = conn.cursor()
        c.execute('insert into evaluation default values')
        id = c.lastrowid
        conn.commit()
    return id


def add_evaluation_dao(name, eval, id):
    dbname = 'IdolRecommendWebDB'
    with closing(sqlite3.connect(dbname)) as conn:
        c = conn.cursor()
        update_sql = 'update evaluation set ' + name + ' = ' + str(eval) + ' where id = ' + str(id)
        c.execute(update_sql)
        conn.commit()


def find_member_name_by_id_dao(id):
    dbname = 'IdolRecommendWebDB'
    with closing(sqlite3.connect(dbname)) as conn:
        c = conn.cursor()
        select_sql = "select name from member where id = ?"
        c.execute(select_sql, (str(id),))
        return str(c.fetchone()[0])
