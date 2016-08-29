from flask import Flask
from text_processor import processor

app = Flask(__name__)

@app.route('/')
def home():
    return 'judge/ <- request POST <text>'

@app.route('/judge')
def judge():
    processor.process("Hola!")
    return '<result of processing>'
