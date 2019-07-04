from flask import Flask, render_template #追加

app = Flask(__name__)


@app.route('/')
def top_page():
    return render_template('index.html', title='Recommend Your OSHIMEN') #変更


@app.route('/like')
def test1():
    name = "test"
    return render_template('hello.html', title='flask test', name=name) #変更


# おまじない
if __name__ == "__main__":
    app.run(debug=True)