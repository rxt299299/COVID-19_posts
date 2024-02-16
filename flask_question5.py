from flask import Flask, jsonify
from question5 import main

# define a flask app
app = Flask(__name__)

@app.route('/quesion5/<hashtag_name>')
def get_output_result(hashtag_name):
    # call main() function from question5.py and get the result
    # example for hashtag_name='#diedsuddenly'
    output_result = main('#'+hashtag_name)
    return jsonify(output_result)

if __name__ == '__main__':
    # start flask app on 5000 port
    app.run(host='0.0.0.0', port=5000)