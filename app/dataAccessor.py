import sqlite3
from contextlib import closing
from app import MemberList
import pandas as pd
import numpy as np
import os
import shutil

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
        c.execute('select * from evaluation')
        print(c.fetchall())
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


def insert_csv():
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


def calc_similarity(id):
    dbname = 'IdolRecommendWebDB'
    with closing(sqlite3.connect(dbname)) as conn:
        target_user_df = pd.read_sql_query('select * from evaluation where id = ' + str(id), conn)
        target_user_org = target_user_df.iloc[0, 1:].values
        print(target_user_org)

        similarities = []
        ids = []
        compare_user_df = pd.read_sql_query('select * from evaluation', conn)
        print(compare_user_df)
        for i in range(len(compare_user_df)):
            target_user = target_user_org
            print('-----------------------------------')
            print(i+1)
            if i + 1 != int(id):
                compare_user = compare_user_df.iloc[i, 1:].values
                columns_count = len(target_user)
                for j in range(columns_count):
                    if target_user[j] is None or np.isnan(target_user[j]):
                        target_user[j] = None
                        compare_user[j] = None
                    elif compare_user[j] is None or np.isnan(compare_user[j]):
                        target_user[j] = None
                        compare_user[j] = None

                target_user = [x for x in target_user if x is not None]
                compare_user = [y for y in compare_user if y is not None]

                s1 = pd.Series(target_user)
                s2 = pd.Series(compare_user)

                res = s1.astype('int').corr(s2.astype('int'))
                if ~np.isnan(res):
                    ids.append(i+1)
                    similarities.append(res)
        print('===========================')
        result = dict(zip(ids, similarities))
        result_sort = sorted(result.items(), key=lambda x: x[1], reverse=True)
        print(result_sort)
        print(result_sort[0])
        print(result_sort[0][0])
        similarity_df = pd.read_sql_query('select * from evaluation where id = ' + str(result_sort[0][0]) +
                                            ' or id = ' + str(result_sort[1][0]) +
                                            ' or id = ' + str(result_sort[2][0]), conn)
        df = pd.concat([target_user_df, similarity_df])
        print(df)

        names = []
        points = []
        for i in range(len(df.columns)):
            if df.iloc[0, i] is None:
                if df.iloc[1, i] is None:
                    rec1 = 0
                else:
                    rec1 = int(df.iloc[1, i])
                if df.iloc[2, i] is None:
                    rec2 = 0
                else:
                    rec2 = int(df.iloc[2, i])
                if df.iloc[3, i] is None:
                    rec3 = 0
                else:
                    rec3 = int(df.iloc[3, i])
                if rec1 + rec2 + rec3 >= 1:
                    names.append(df.columns[i])
                    rec1_points = rec1 * float(result_sort[0][1])
                    rec2_points = rec2 * float(result_sort[1][1])
                    rec3_points = rec3 * float(result_sort[2][1])
                    points.append(rec1_points + rec2_points + rec3_points)
        recommend = dict(zip(names, points))
        recommend_sort = sorted(recommend.items(), key=lambda x: x[1], reverse=True)
        print(recommend_sort)

        recommend_list = []
        count = 0
        for item in recommend_sort:
            recommend_list.append(item[0])
            count = count + 1
            if count >= 10:
                break
        print(recommend_list)
        return recommend_list


def show_evaluation_data():
    dbname = 'IdolRecommendWebDB'
    with closing(sqlite3.connect(dbname)) as conn:
        df = pd.read_sql_query('select * from evaluation', conn)
        result_str = []
        df_columns_str = [str(n) for n in df.columns.tolist()]
        result_str.append(df_columns_str)
        for i in range(len(df)):
            result_numpy = df.iloc[i, :].values
            result = [str(n) for n in result_numpy]
            result_str.append(result)
    return result_str


def create_addmember_table():
    dbname = 'IdolRecommendWebDB'
    with closing(sqlite3.connect(dbname)) as conn:
        c = conn.cursor()
        # テーブル削除
        c.execute('drop table if exists addmember')
        # テーブル作成
        create_member_table = '''create table if not exists addmember(id integer primary key autoincrement, name text, 
        group_name text, twitter_id text, instagram_id text,img_name text)'''
        c.execute(create_member_table)
        conn.commit()


def add_addmember(member):
    dbname = 'IdolRecommendWebDB'
    with closing(sqlite3.connect(dbname)) as conn:
        c = conn.cursor()
        insert_member_sql = '''insert into addmember(name,group_name,twitter_id,instagram_id,img_name) values(?,?,?,?,?)'''
        c.execute(insert_member_sql, (member[0], member[1], member[2], member[3], member[4],))
        conn.commit()

        c.execute('select * from addmember')
        print(c.fetchall())


def find_member_by_name_and_group_name(check_member):
    dbname = 'IdolRecommendWebDB'
    with closing(sqlite3.connect(dbname)) as conn:
        c = conn.cursor()
        check_added_member = '''select * from member where name = ? and group_name = ?'''
        c.execute(check_added_member, (check_member[0], check_member[1]))

        result = c.fetchall()
        print(result)
        print(len(result))
        if len(result) == 0:
            return False
        else:
            return True


def get_addmember():
    dbname = 'IdolRecommendWebDB'
    with closing(sqlite3.connect(dbname)) as conn:
        c = conn.cursor()
        get_member = '''select * from addmember'''
        c.execute(get_member)
        result = c.fetchall()
        return result


def aproval_member(id):
    dbname = 'IdolRecommendWebDB'
    with closing(sqlite3.connect(dbname)) as conn:
        c = conn.cursor()
        get_member = '''select name,group_name,twitter_id,instagram_id,img_name from addmember where id = ?'''
        c.execute(get_member, (id,))
        result = c.fetchall()[0]

        insert_member_sql = '''insert into member(name,group_name,twitter_id,instagram_id) values(?,?,?,?)'''
        c.execute(insert_member_sql, (result[0], result[1], result[2], result[3]))

        dir_name = './static/img/' + result[0]
        os.makedirs(dir_name, exist_ok=True)
        img_filename = './static/etcimg/' + result[4]
        new_img_filename = dir_name + '/' + result[0] + ' (1).jpg'
        shutil.copyfile(img_filename, new_img_filename)

        c.execute(' alter table evaluation add column ' + result[0] + ' [ int]')
        c.execute('delete from addmember where id = ?', (id, ))
        conn.commit()


def disaproval_member(id):
    dbname = 'IdolRecommendWebDB'
    with closing(sqlite3.connect(dbname)) as conn:
        c = conn.cursor()
        c.execute('delete from addmember where id = ?',(id, ))
        conn.commit()


def any_sql():
    dbname = 'IdolRecommendWebDB'
    with closing(sqlite3.connect(dbname)) as conn:
        c = conn.cursor()
        c.execute('delete from member where name = 柊宇咲')


