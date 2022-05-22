# flask_web/app.py

import os
from flask import Flask, request, jsonify
from redis import Redis
from prometheus_flask_exporter import PrometheusMetrics

from config import Pool, Config

app = Flask(__name__)
metrics = PrometheusMetrics(app)

# Connect to redis
REDIS_HOST = os.getenv('REDIS_HOST')
REDIS_PORT = os.getenv('REDIS_PORT')
REDIS_PASSWORD = os.getenv('REDIS_PASSWORD')
redis = Redis(host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PASSWORD)

@app.route('/')
def handle_main():
    return 'Good Morning, Vietnam!'


@app.route('/bridge')
def handle_bridge():
    result = ["123"]
    #TODO
    return jsonify(result)


@app.route('/report', methods=['POST'])
def handle_report():
    content = request.get_json(silent=True)
    state = bool(content.get('state', False))
    bridge = content.get('bridge', '')

    if len(bridge) == 0:
        return 'Failed', 400

    if state:
        #TODO
        return 'Promoted'
    else:
        #TODO
        return 'Punished'

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=3000)