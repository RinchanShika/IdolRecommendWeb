import sqlite3
from contextlib import closing
from app import MemberList
import pandas as pd


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
        c.execute('PRAGMA TABLE_INFO(evaluation)')
        print(c.fetchall())
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
        print(name)
        c.execute(update_sql)
        conn.commit()
        return eval


def find_member_name_by_id_dao(id):
    dbname = 'IdolRecommendWebDB'
    with closing(sqlite3.connect(dbname)) as conn:
        c = conn.cursor()
        select_sql = "select name from member where id = ?"
        c.execute(select_sql, (str(id),))
        return str(c.fetchone()[0])


def get_twitter(name):
    dbname = 'IdolRecommendWebDB'
    with closing(sqlite3.connect(dbname)) as conn:
        c = conn.cursor()
        select_sql = 'select group_name, twitter_id from member where name = ?'
        c.execute(select_sql, (name,))
        result = c.fetchone()
        group_name = result[0]
        twitter_id = result[1]
        result_set = [group_name, twitter_id]
        return result_set


def add_twitter():
    dbname = 'IdolRecommendWebDB'
    with closing(sqlite3.connect(dbname)) as conn:
        c = conn.cursor()
        group_count = len(MemberList.groupList)

        for i in range(group_count):
            for j in range(len(MemberList.groupList[i])):
                if j == 0:
                    continue
                name = MemberList.groupList[i][j]
                twitter = MemberList.groupTwitterList[i][j]
                update_sql = "update member set twitter_id  = '" + str(twitter) + "' where name = '" + str(name) + "'"
                print(update_sql)
                c.execute(update_sql)

        conn.commit()
        c.execute('select * from member')
        print(c.fetchall())


def any_sql():
    dbname = 'IdolRecommendWebDB'
    with closing(sqlite3.connect(dbname)) as conn:
        c = conn.cursor()


def insert_csv():
    import pandas as pd
    df = pd.read_csv('C:/Users/yasug/Downloads/Untitled form (Responses) - Sheet4 (1).csv')
    columns_name = df.columns
    row_count = 33
    print(columns_name)

    dbname = 'IdolRecommendWebDB'
    with closing(sqlite3.connect(dbname)) as conn:
        c = conn.cursor()

        for i in range(row_count):
            df_row = df.iloc[i, :].values
            c.execute('insert into evaluation default values')
            id = c.lastrowid
            for j in range(len(columns_name)):
                name = columns_name[j]
                if columns_name[j] == '小山さゆ':
                   name = '小山ひな'
                if columns_name[j] == '神崎颯花':
                    name = '神﨑風花'
                if columns_name[j] == '松下玲緒奈':
                    name = '松下玲緒菜'
                update_sql = 'update evaluation set ' + str(name) + ' = ' + str(df_row[j]) + ' where id = ' + str(id)
                c.execute(update_sql)
                conn.commit()


def calc_similarity():
    for i in range(csv_rows_count - 1):
        target_sum_points = 0
        comp_sum_points = 0
        sum_multi_points = 0
        target_sum_square_points = 0
        comp_sum_square_point = 0
        if csv_input.iloc[i, 0] != target_user:
            comp_user = csv_input.iloc[i, 0]
            print(comp_user)
            comp_row = csv_input.iloc[i, 1:35]
            comp_row_check = csv_input.iloc[i, 39:43]
            s1 = pd.Series(target_row)
            s2 = pd.Series(comp_row)


            try:
                res = s1.astype('int').corr(s2.astype('int'))
            except:
                pass
            if res > 0.50:
                similarities.append(target_user + ':' + comp_user + '=' + str(res))
                # for k in range(8):
                #     print('T:' + str(target_row_check[k]) + 'C:' + str(comp_row_check[k]))
                print('森みはる→T:' + str(target_row_check[0]) + 'C:' + str(comp_row_check[0]))
            print(res)

    print(similarities)


def show_evaluation_data():
    dbname = 'IdolRecommendWebDB'
    with closing(sqlite3.connect(dbname)) as conn:
        df = pd.read_sql_query('select * from evaluation', conn)
        print(df)
        result_str = []
        df_columns_str = [str(n) for n in df.columns.tolist()]
        result_str.append(df_columns_str)
        for i in range(len(df)):
            result_numpy = df.iloc[i, :].values
            result = [str(n) for n in result_numpy]
            result_str.append(result)
    return result_str