from flask import Flask, render_template, jsonify, session
import app.service as service
import glob
import os

app = Flask(__name__)
app.secret_key = 'auhgushfuwe'

input_evaluations = []


@app.route('/')
def top_page():
    return render_template('hello.html', title='Recommend Your OSHIMEN')


@app.route('/like')
def like():
    if len(input_evaluations) == 5:
        service.add_evaluation(input_evaluations, id)
    return render_template('hello.html', title='flask test')


@app.route('/watchGirls')
def start():
    id = service.add_evaluationRow()
    session['id'] = id
    return render_template('watchIdols.html', title='Watch Cute and Beautiful Girls')


@app.route('/getFirstList')
def get_first_list():
    # 初期の名前と画像配列を与える(とりあえず来栖の写真1枚)
    name = [1]
    image = ['/static/img/img1/rinchan2019070100123135.jpg']

    data = [
        {"name": name},
        {"image": image}
    ]

    return jsonify({
        'status': 'OK',
        'data': data
    })


# おまじない
if __name__ == "__main__":
    app.run(debug=True)