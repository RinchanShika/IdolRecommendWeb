from flask import Flask, render_template, jsonify, session, request
import app.service as service
import random
import glob


app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
app.secret_key = 'auhgushfuwe'

input_evaluations = []


@app.route('/')
def top_page():
    return render_template('index.html', title='Recommend Your OSHIMEN')


@app.route('/like')
def like():
    if len(input_evaluations) == 5:
        service.add_evaluation(input_evaluations, id)
    return render_template('hello.html', title='flask test')


@app.route('/watchGirls')
def start():
    if 'id' not in session:
        id = service.add_evaluationRow()
        session['id'] = id
    return render_template('watchIdols.html', title='Watch Cute and Beautiful Girls')


@app.route('/getFirstList')
def get_first_list():
    member_folder_list = glob.glob('static/img/*')
    member_list = []
    for member_folder in member_folder_list:
        split_path = member_folder.split('\\')
        member_list.append(split_path[1])
        print(member_list)

    num = random.randint(1, len(member_list))
    name = member_list[num - 1]
    num = random.randint(1, 10)
    file_name = name + ' (' + str(num) + ').jpg'
    image = file_name
    data = {
        "name": name,
        "image": image
    }
    return jsonify({'data': data})


@app.route('/putEvaluation', methods=['POST'])
def putEvaluation():
    data = request.get_json()
    put_eval = data['eval']
    put_name = data['name']
    service.add_evaluation(put_name, put_eval, session['id'])

    member_folder_list = glob.glob('static/img/*')
    member_list = []
    for member_folder in member_folder_list:
        split_path = member_folder.split('\\')
        member_list.append(split_path[1])
        print(member_list)

    num = random.randint(1, len(member_list))
    name = member_list[num - 1]
    num = random.randint(1, 10)
    file_name = name + ' (' + str(num) + ').jpg'
    image = file_name
    data = {
        "name": name,
        "image": image
    }
    return jsonify({'data': data})


# おまじない
if __name__ == "__main__":
    app.run(debug=True)