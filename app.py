import sys

from flask import Flask, jsonify

app = Flask(__name__)


# write your code here

@app.route('/event/today')
def today_event():
    return jsonify({"data": "There are no events for today!"})


# do not change the way you run the program
if __name__ == '__main__':
    if len(sys.argv) > 1:
        arg_host, arg_port = sys.argv[1].split(':')
        app.run(host=arg_host, port=arg_port)
    else:
        app.run()
