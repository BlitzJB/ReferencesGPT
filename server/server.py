
from flask import Flask, request, jsonify, render_template, make_response, g, redirect
from flask_cors import CORS
from funcs import research


app = Flask(__name__)
CORS(app)


@app.route('/api/research', methods=['POST'])
def api_research():
    if request.method == 'POST':
        data = request.get_json()
        return jsonify(research(data['text']))
    
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)