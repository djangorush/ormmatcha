from flask import Flask
from flask import request
app = Flask(__name__)

@app.route('/hello/<int:postId>')
def hello_name(postId):
   return 'Hello %d!' % postId

@app.route('/bonjour')
def bonjour():
    print('ip address:', request.environ['REMOTE_ADDR'])
    return 'Bonjour le monde'

if __name__ == '__main__':
    app.add_url_rule('/avis', 'hellosdasda', hello_name)
    app.run()