import sys
from flask import Flask, jsonify
from datetime import date
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api, reqparse, inputs, Resource
from marshmallow import Schema, fields

app = Flask(__name__)
db = SQLAlchemy(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///calendar.db'
api = Api(app)


class EventSchema(Schema):
    id = fields.Int()
    event = fields.Str()
    date = fields.Date()


class Event(db.Model):
    __tablename__ = 'events'
    id = db.Column(db.Integer, primary_key=True)
    event = db.Column(db.String(80), nullable=False)
    date = db.Column(db.Date, nullable=False)


db.create_all()

parser = reqparse.RequestParser()
parser.add_argument('event', type=str, help='The event name is required!', required=True)
parser.add_argument('date', type=inputs.date,
                    help='The event date with the correct format is required! The correct format is YYYY-MM-DD!',
                    required=True)


class EventResource(Resource):
    def get(self):
        schema = EventSchema(many=True)
        events = Event.query.all()

        return schema.dump(events)

    def post(self):
        args = parser.parse_args(strict=True)
        date_to_add = args['date']
        event_to_add = args['event']
        db.session.add(Event(event=event_to_add, date=date_to_add))
        db.session.commit()

        return jsonify(
            {
                "message": "The event has been added!",
                "event": event_to_add,
                "date": date_to_add.strftime('%Y-%m-%d')
            })


api.add_resource(EventResource, '/event')


@app.route('/event/today')
def today():
    schema = EventSchema(many=True)
    events = Event.query.filter(Event.date == date.today())
    print(schema.dump(events))
    return jsonify(schema.dump(events))


# do not change the way you run the program
if __name__ == '__main__':
    if len(sys.argv) > 1:
        arg_host, arg_port = sys.argv[1].split(':')
        app.run(host=arg_host, port=arg_port)
    else:
        app.run()
