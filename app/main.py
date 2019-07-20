from flask import Flask, render_template, jsonify, session, request, url_for, redirect
import werkzeug
from app import accessService
import random
import glob
import copy
import os


app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
app.secret_key = 'auhgushfuwe'
UPLOAD_FOLDER = './static/etcimg/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 10 * 1024 * 1024
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'gif'])


@app.route('/')
def top_page():
    return render_template('index.html', title='Recommend Your OSHIMEN')


@app.route('/watchGirls')
def start():
    if 'id' not in session:
        id = accessService.add_evaluationRow()
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
    member_count = len(member_list)
    data = request.get_json()
    put_eval = data['eval']
    put_name = data['name']
    eval_points = accessService.add_evaluation(put_name, put_eval, session['id'])
    if eval_points == 1:
        like_members.append(put_name)
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


@app.route('/addidol', methods=['GET', 'POST'])
def add_idol():
    if request.method == 'POST':
        img_file = request.files['img_file']
        if img_file.filename == '':
            error_message = '顔写真は必須です。'
            return render_template('addIdol.html', title='add idol', error_message=error_message)

        if img_file and allowed_file(img_file.filename):
            filename = werkzeug.utils.secure_filename(img_file.filename)
            img_url = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            img_file.save(img_url)

        name = request.form['name']
        group_name = request.form['group_name']
        twitter_id = request.form['twitter_id']
        instagram_id = request.form['instagram_id']

        check_member = [name, group_name]
        if accessService.check_member(check_member) is True:
            error_message = name + '/' + group_name + ' は既に登録されています。'
            return render_template('addIdol.html', title='add idol', error_message=error_message)

        member = [name, group_name, twitter_id, instagram_id, filename]
        succsess = accessService.add_member(member)

        return render_template('addidolcomfirm.html', img_url=img_url, name=name, group_name=group_name,
                               twitter_id=twitter_id, instagram_id=instagram_id)
    else:
        return render_template('addIdol.html', title='add idol')


def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@app.route('/addlist')
def addlist():
    return render_template('addList.html', title='addList')


@app.route('/displayaddlist')
def show_ad_list():
    add_members = accessService.get_addmember()
    data = {
        "data": add_members
    }
    return jsonify(data)


@app.route('/aprovalAddIdol/<int:id>')
def aproval_idol(id):
    accessService.aproval(id)
    return redirect('/addlist')


@app.route('/disaprovalAddIdol/<int:id>')
def disaproval_idol(id):
    accessService.disaproval(id)
    return redirect('/addlist')


# おまじない
if __name__ == "__main__":
    app.run(debug=True)