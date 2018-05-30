from flask import Flask
from app.app import *

app = Flask(__name__)

# @app.route('/')
# def index():
#     return 'Deploy Success'
#
# if __name__ == '__main__':
#     app.run()