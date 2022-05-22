# flask_web/app.py

from flask import Flask, request, jsonify
from prometheus_flask_exporter import PrometheusMetrics

import json
from db import init_db
from config import load_config
from feature import route_signal_user

app = Flask(__name__)
metrics = PrometheusMetrics(app)

# Connect to redis
config = load_config('config.yaml')
db = init_db(config)


@app.route('/')
def handle_main():
    return 'Good Morning, Vietnam!'


## Expected request
##    {
##    proto: signal,
##    cell: +7900100001001000,
##    nickname: …,
##    uid: …,
##    }
@app.route('/bridge', methods=['GET'])
def handle_bridge_get():
    return handle_bridge_real({
        'proto': 'signal',
        'cell': '79000111000',
        'nickname': 'Test Test',
        'uid': '123',
    }, 'signal')


@app.route('/bridge', methods=['POST'])
def handle_bridge_post():
    user_data = request.get_json(silent=True) # For debugging purposes
    proto = user_data.get('proto', '') # For debugging purposes

    return handle_bridge_real(user_data, proto)


def handle_bridge_real(user_data, proto):
    if proto == 'signal':
        default_bridge, user_id = route_signal_user(user_data=user_data, db=db, pools=config)
        if default_bridge is None:
            return jsonify([]), 400

        bridge = db.get_or_set_sticky(user_id, default_bridge)
        return jsonify([bridge]), 200

    return jsonify([]), 400

@app.route('/report', methods=['POST'])
def handle_report():
    content = request.get_json(silent=True)
    state = bool(content.get('state', False))
    bridge = content.get('bridge', '')

    if len(bridge) == 0:
        return 'Failed', 400

    if state:
        db.bridge_karma_up(bridge)
        return 'Promoted'
    else:
        db.bridge_karma_up(bridge)
        return 'Punished'


if __name__ == '__main__':
    db.reset_on_startup()
    app.run(debug=True, host='0.0.0.0', port=3000)