import app as a


# start→evaluationにユーザ評価行を登録する
def add_evaluationRow():
    return a.dataAccessor.add_evaluationRow_dao()


def add_evaluation(name, eval, id):
    a.dataAccessoradd_evaluation_dao(name, eval, id)


def select_member(id):
    return a.dataAccessorfind_member_name_by_id_dao(id)
