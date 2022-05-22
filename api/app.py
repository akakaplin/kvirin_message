# flask_web/app.py

from flask import Flask, request, jsonify
from prometheus_flask_exporter import PrometheusMetrics

from db import init_db
from config import load_config, Config
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
@app.route('/bridge')
def handle_bridge():
    user_data = request.get_json(silent=True)
    proto = user_data.get('proto', '')

    if proto == 'signal':
        result = route_signal_user(user_data, config, db)
        return jsonify(result)

    return '[]', 400


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
    db.reset_on_startup()
    app.run(debug=True, host='0.0.0.0', port=3000)