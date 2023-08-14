from flask import Flask, jsonify, request
from flask_cors import CORS
import os
from ai import generateText

app = Flask(__name__)
CORS(app)

@app.route('/generateText/<type>', methods=['POST'])
def generateContent(type):
    res = request.get_json()
    url = generateText(type, res.get("url"), res.get("text"))

    return jsonify(url)

if __name__ == '__main__':
    app.run(debug=True, port=os.getenv("PORT", default=5000))
