from flask import Flask
import search

# creates flask app to run
app = Flask(__name__)


# specifies route for flask app to run on
@app.route('/')
def get():
    return 'Hello World!'


# includes name as a variable
@app.route('/hello/<name>')
def hello_name(name):
    return 'Hello '+ name + '!'


if __name__ == '__main__':
    # to check if app is running, go to localhost:5000/
    # on any web browser on your laptop

    # runs application on localhost
    app.run(host='0.0.0.0')
