import app.dataAccessor as dao


# start→evaluationにユーザ評価行を登録する
def add_evaluationRow():
    return dao.add_evaluationRow()


def add_evaluation(result, id):
    dao.add_evaluation(result, id)

# 相関を求める
