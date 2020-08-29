from flask import Flask, render_template, request, jsonify
import os
from pymongo import MongoClient

app = Flask(__name__)

client = MongoClient('localhost', 27017)
db = client.dbtest


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/list', methods=['GET'])
def showList():
    matjip = list(db.matjip.find({}, {'_id': False}))
    return jsonify({'result': 'success', 'matjip': matjip})

@app.route('/reviewlist', methods=['GET'])
def reviewList():
    review = list(db.review.find({}, {'_id': False}))
    review_pic = list(db.review_pic.find({}, {'_id': False}))
    return jsonify({'result': 'success', 'review': review, 'review_pic' : review_pic})

@app.route('/search', methods=["GET"])
def get_matjip():
    name = request.args.get('name')
    matjip = list(db.matjip.find({}, {'_id': False}))
    search = []
    for i in range(len(matjip)):
        if name in matjip[i]['title']:
            search.append(matjip[i])
    if (len(search) == 0):
        return jsonify({'result': 'fail'})
    else:
        return jsonify({'result': 'success', 'matjip': search})


@app.route('/review', methods=['POST'])
def postArticle():
    title = request.form['title']
    comment = request.form['comment']
    db.review.insert_one({
        'title': title,
        'comment': comment,
    })
    return jsonify({'result': 'success', 'msg': '저장되었습니다!'})

@app.route('/file', methods=['POST'])
def fileSave():
    file = request.files['file']
    file.save(os.path.join(os.getcwd()+"/static", file.filename))
    db.review_pic.insert_one({
        'pic': file.filename
    })
    return jsonify({'result': 'success', 'msg': '저장되었습니다!'})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
