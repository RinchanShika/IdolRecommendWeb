from flask import Flask, render_template, jsonify, session, request
import app as a
import random
import glob
import copy


app1 = Flask(__name__)
app1.config['JSON_AS_ASCII'] = False
app1.secret_key = 'auhgushfuwe'
like_members = []


@app1.route('/')
def top_page():
    return render_template('index.html', title='Recommend Your OSHIMEN')


@app1.route('/watchGirls')
def start():
    if 'id' not in session:
        id = a.service.add_evaluationRow()
        session['id'] = id
    return render_template('watchIdols.html', title='Watch Cute and Beautiful Girls')


@app1.route('/getFirstList')
def get_first_list():
    like_members = []
    member_folder_list = glob.glob('static/img/*')
    member_list = []
    for member_folder in member_folder_list:
        split_path = member_folder.split('\\')
        member_list.append(split_path[1])

    num = random.randint(1, len(member_list))
    name = member_list[num - 1]
    # num = random.randint(1, 10)
    # file_name = name + ' (' + str(num) + ').jpg'
    file_name = name + ' (1).jpg'
    image = file_name
    data = {
        "name": name,
        "image": image
    }
    return jsonify({'data': data})


@app1.route('/putEvaluation', methods=['POST'])
def putEvaluation():
    data = request.get_json()
    put_eval = data['eval']
    put_name = data['name']
    a.service.add_evaluation(put_name, put_eval, session['id'])
    if put_eval == 1:
        like_members.append(put_name)

    member_folder_list = glob.glob('static/img/*')
    member_list = []
    for member_folder in member_folder_list:
        split_path = member_folder.split('\\')
        member_list.append(split_path[1])

    num = random.randint(1, len(member_list))
    name = member_list[num - 1]
    # num = random.randint(1, 10)
    # file_name = name + ' (' + str(1) + ').jpg'
    file_name = name + ' (1).jpg'
    image = file_name
    data = {
        "name": name,
        "image": image
    }
    return jsonify({'data': data})


@app1.route('/endEvaluation')
def endEvaluation():
    return render_template('likelist.html', title='Your OSHIMEN List')


@app1.route('/displaylikelist')
def display_like_list():
    like_list = copy.copy(like_members)
    data = {
        "like_list": like_list,
    }
    like_members.clear()
    return jsonify({'data': data})


# おまじない
if __name__ == "__main__":
    app1.run(debug=True)