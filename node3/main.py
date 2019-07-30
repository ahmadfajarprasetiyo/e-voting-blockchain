from flask import Flask
from flask import request
import logic

app = Flask(__name__)

@app.route('/trx', methods=['POST'])
def trx():
    print("masuk")
    content = request.json
    sender_n = int(content['sender_n'])
    sender_e = int(content['sender_e'])
    sender_d = int(content['sender_d'])
    receiver_n = int(content['receiver_n'])
    receiver_e = int(content['receiver_e'])

    return logic.vote(sender_n, sender_e, sender_d, receiver_n, receiver_e):

@app.route('/get_hash', methods=['GET'])
def get_hash():
    print("Get Lastest Hash Value")

    return logic.get_lastest_hash()

if __name__ == '__main__':
    app.run(host='localhost', port=5001, debug=True)


