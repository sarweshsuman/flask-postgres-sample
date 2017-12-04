from flask import Flask,request
from flask_cors import CORS , cross_origin
from flask import jsonify

from python_postgres import TicketsPostgresWrapper;
import json
import sys

import logging

app = Flask(__name__)
logging.basicConfig(level=logging.DEBUG)
cors = CORS(app, resources={r'/submitNewTicket': {"origins": "*"}})

logging.getLogger('flask_cors').level = logging.DEBUG


@app.route('/')
def index():
    return "Server Is Up!"

@app.route('/submitNewTicket',methods=['POST'])

@cross_origin()
def submit_new_ticket():
    try:
     tickets_postgres_conn = TicketsPostgresWrapper();
     print("Recevied Request with data ",request.data)
     request_as_json = json.loads(request.data.decode('utf-8'))
     ticket_no = request_as_json['ticket_no']
     print("Saving ticket no {}".format(ticket_no))
     tickets_postgres_conn.insert_data(request_as_json)
     sys.stdout.flush()
     tickets_postgres_conn.close()
     return jsonify("Ticket Submitted")
    except Exception as e:
     global tickets_postgres_conn
     print("Error {}".format(e))
     sys.stdout.flush()
     return jsonify("Received Error {}, please try again".format(e))

if __name__ == '__main__':
    app.run(debug=True,host='10.0.0.6',port=3001,threaded=True)
