from flask import Flask
from flask import render_template
from flask import request
from flask import redirect, url_for
import search

# creates flask app to run
app = Flask(__name__)


# specifies route for flask app to run on
@app.route('/', methods=['POST'])
def get_input_text():
    if request.method == 'POST':
        query = request.form.items()
        term = ''
        for k,v in query:
            print('received ', k, v)
            term = v
        print(term)
        return display_results(term)
    return render_template('search.html')


def display_results(queries):
    print('testing', queries)
    return render_template('results.html', keyterm=queries)
  

if __name__ == '__main__':
    # to check if app is running, go to localhost:5000/
    # on any web browser on your laptop

    # runs application on localhost
    app.run(host='0.0.0.0')
