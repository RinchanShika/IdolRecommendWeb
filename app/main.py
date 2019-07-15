from flask import Flask, render_template, jsonify, session, request
from app import accessService
import random
import glob
import copy


app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
app.secret_key = 'auhgushfuwe'


@app.route('/')
def top_page():
    return render_template('index.html', title='Recommend Your OSHIMEN')


@app.route('/watchGirls')
def start():
    if 'id' not in session:
        id = accessService.add_evaluationRow()
        print(str(id))
        session['id'] = id
    member_list = []
    session['member_list'] = member_list
    like_members = []
    session['like_members'] = like_members
    return render_template('watchIdols.html', title='Watch Cute and Beautiful Girls')


@app.route('/getFirstList')
def get_first_list():

    member_list = session['member_list']
    member_list.clear()
    member_folder_list = glob.glob('static/img/*')
    for member_folder in member_folder_list:
        if '\\' in member_folder:
            split_path = member_folder.split('\\')
        else:
            split_path = member_folder.split('img/')
        member_list.append(split_path[1])

    member_count = len(member_list)
    num = random.randint(1, member_count)
    name1 = member_list.pop(num - 1)

    file_name = name1 + ' (1).jpg'
    image1 = file_name

    num = random.randint(1, len(member_list))
    name2 = member_list.pop(num - 1)
    file_name = name2 + ' (1).jpg'
    image2 = file_name

    data = {
        "name1": name1,
        "image1": image1,
        "name2": name2,
        "image2": image2
    }
    print(data)
    session['member_list'] = member_list
    return jsonify({'data': data})


@app.route('/putEvaluation', methods=['POST'])
def putEvaluation():
    member_list = session['member_list']
    like_members = session['like_members']
    print(member_list)
    print(like_members)
    member_count = len(member_list)
    print(member_count)
    data = request.get_json()
    put_eval = data['eval']
    put_name = data['name']
    eval_points = accessService.add_evaluation(put_name, put_eval, session['id'])
    print(str(eval_points))
    if eval_points == 1:
        like_members.append(put_name)
        print(like_members)
    num = random.randint(1, member_count)
    name = member_list.pop(num - 1)
    file_name = name + ' (1).jpg'
    image = file_name
    data = {
        "name": name,
        "image": image
    }
    session['member_list'] = member_list
    session['like_members'] = like_members
    return jsonify({'data': data})


@app.route('/endEvaluation')
def endEvaluation():
    accessService.calc_similarity(session['id'])
    return render_template('likelist.html', title='Your OSHIMEN List')


@app.route('/recommend')
def rendering_recommend():
    return render_template('recommendlist.html', title='Your OSHIMEN List')


@app.route('/displaylikelist')
def display_like_list():
    member_list = session['member_list']
    like_members = session['like_members']
    like_list = copy.copy(like_members)

    like_list_twitter = []
    like_list_group = []
    for member in like_list:
        result_set = accessService.get_twitter(member)
        like_list_group.append((result_set[0]))
        like_list_twitter.append(result_set[1])

    data = {
        "like_list": like_list,
        "like_list_twitter": like_list_twitter,
        "like_list_group": like_list_group
    }
    like_members.clear()
    session['like_members'] = like_members
    return jsonify({'data': data})


@app.route('/displayrecommendlist')
def display_recommend_list():
    recommend_list = accessService.calc_similarity(session['id'])
    recommend_list_twitter = []
    recommend_list_group = []
    for member in recommend_list:
        result_set = accessService.get_twitter(member)
        recommend_list_group.append((result_set[0]))
        recommend_list_twitter.append(result_set[1])
    data = {
        "like_list": recommend_list,
        "like_list_twitter": recommend_list_twitter,
        "like_list_group": recommend_list_group
    }
    return jsonify({'data': data})


@app.route('/admin')
def admin():
    return render_template('admin.html', title='admin page')


@app.route('/evaluationdata')
def evaluationdata():
    return render_template('evaluationdata.html', title='admin page')


@app.route('/showevaluation')
def show_evaluation():
    result = accessService.show_evaluation()
    data = {
        "data": result
    }
    return jsonify(data)


# おまじない
if __name__ == "__main__":
    app.run(debug=True)