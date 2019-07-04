from flask import Flask, render_template #追加
import app.service as service

app = Flask(__name__)
input_evaluations = []


@app.route('/')
def top_page():
    return render_template('hello.html', title='Recommend Your OSHIMEN')


@app.route('/like')
def like():
    if len(input_evaluations) == 5:
        service.add_evaluation(input_evaluations, id)
    return render_template('hello.html', title='flask test')


@app.route('/start')
def start():
    id = service.add_evaluationRow()
    return render_template('watchIdols.html', title='Watch Cute and Beautiful Girls')


# おまじない
if __name__ == "__main__":
    app.run(debug=True)