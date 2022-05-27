from flask import Flask
from flask import send_file


app = Flask(__name__)




@app.route('/')
def index():
    return 'Web App with Python Flask!'

app.run(host='0.0.0.0', port=8097)