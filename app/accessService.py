from app import dataAccessor


# start→evaluationにユーザ評価行を登録する
def add_evaluationRow():
    return dataAccessor.add_evaluationRow_dao()


def add_evaluation(name, eval, id):
    dataAccessor.add_evaluation_dao(name, eval, id)


def select_member(id):
    return dataAccessor.find_member_name_by_id_dao(id)


def get_twitter(name):
    return dataAccessor.get_twitter(name)
