import sys
import datetime
from flask import Flask, jsonify
from flask_restful import Api, reqparse, inputs, Resource


def validate_time(date_text):
    try:
        datetime.datetime.strptime(date_text, '%Y-%m-%d')
    except ValueError:
        return False
    return True


app = Flask(__name__)
api = Api(app)

parser = reqparse.RequestParser()
parser.add_argument('event', type=str, help='The event name is required!', required=True)
parser.add_argument('date', type=inputs.date,
                    help='The event date with the correct format is required! The correct format is YYYY-MM-DD!',
                    required=True)


class Event(Resource):
    def post(self):
        args = parser.parse_args(strict=True)
        date_event = args['date']
        event = args['event']
        return jsonify(
            {
                "message": "The event has been added!",
                "event": event,
                "date": date_event.strftime('%Y-%m-%d')
            })


api.add_resource(Event, '/event')

# do not change the way you run the program
if __name__ == '__main__':
    if len(sys.argv) > 1:
        arg_host, arg_port = sys.argv[1].split(':')
        app.run(host=arg_host, port=arg_port)
    else:
        app.run()
