from flask import Flask, render_template, jsonify, session, request
import app.service as service
import random


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
    # print('呼ばれたよ～')
    # # 初期の名前と画像配列を与える(とりあえず来栖の写真1枚)
    # names = ['来栖りん', '吉井美優', '大門果琳', '森みはる', '江嶋綾恵梨']
    # images = []
    # for name in names:
    name = '来栖りん'
    num = random.randint(1, 10)
    file_name = name + ' (' + str(num) + ').jpg'
    # file_path = '../static/img/' + file_name
    # images.append(file_name)
    image = file_name
    data = {
            "name": name,
            "image": image
        }
    return jsonify({'data': data})


@app.route('/putEvaluation', methods=['POST'])
def puptEvaluation():
    data = request.get_json()
    print(data)
    print(session['id'])

    name = '来栖りん'
    num = random.randint(1, 10)
    file_name = name + ' (' + str(num) + ').jpg'
    # file_path = '../static/img/' + file_name
    # images.append(file_name)
    image = file_name
    data = {
        "name": name,
        "image": image
    }

    return jsonify({'data': data})


# おまじない
if __name__ == "__main__":
    app.run(debug=True)