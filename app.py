from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient

app = Flask(__name__)

client = MongoClient('localhost', 27017)
db = client.dbtest

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/list', methods=['GET'])
def showList():
    matjip = list(db.matjip.find({},{'_id':False}))
    return jsonify({'result': 'success', 'matjip':matjip})

@app.route('/search', methods=["GET"])
def get_matjip():
    name = request.args.get('name')
    matjip = list(db.matjip.find({},{'_id':False}))
    search = []
    for i in range(len(matjip)):
        if name in matjip[i]['title']:
            search.append(matjip[i])

    print(search)
    if (len(search)==0):
        return jsonify({'result': 'fail'})
    else:
        return jsonify({'result': 'success', 'matjip':search})

if __name__ == '__main__':
    app.run('0.0.0.0',port=5000,debug=True)