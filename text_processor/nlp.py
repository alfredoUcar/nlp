from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return 'judge/ <- request POST <text>'

@app.route('/judge')
def judge():
    return 'result of processing'
