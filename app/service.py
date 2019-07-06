import app.dataAccessor as dao


# start→evaluationにユーザ評価行を登録する
def add_evaluationRow():
    return dao.add_evaluationRow()


def add_evaluation(name, eval, id):
    dao.add_evaluation(name, eval, id)


def select_member(id):
    return dao.find_member_name_by_id(id)
