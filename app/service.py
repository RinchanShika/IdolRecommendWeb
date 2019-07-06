from app.dataAccessor import *


# start→evaluationにユーザ評価行を登録する
def add_evaluationRow():
    return add_evaluationRow_dao()


def add_evaluation(name, eval, id):
    add_evaluation_dao(name, eval, id)


def select_member(id):
    return find_member_name_by_id_dao(id)
