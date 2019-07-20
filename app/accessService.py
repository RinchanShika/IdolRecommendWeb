from app import dataAccessor


# start→evaluationにユーザ評価行を登録する
def add_evaluationRow():
    return dataAccessor.add_evaluationRow_dao()


def add_evaluation(name, eval, id):
    return dataAccessor.add_evaluation_dao(name, eval, id)


def select_member(id):
    return dataAccessor.find_member_name_by_id_dao(id)


def get_twitter(name):
    return dataAccessor.get_twitter(name)


def show_evaluation():
    return dataAccessor.show_evaluation_data()


def calc_similarity(id):
    return dataAccessor.calc_similarity(id)

def add_member(member):
    return dataAccessor.add_addmember(member)


def check_member(check_member):
    return dataAccessor.find_member_by_name_and_group_name(check_member)


def get_addmember():
    return dataAccessor.get_addmember()


def aproval(id):
    return dataAccessor.aproval_member(id)

def disaproval(id):
    return dataAccessor.disaproval_member(id)