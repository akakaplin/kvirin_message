# flask_web/app.py

import os
from flask import Flask
from redis import Redis
app = Flask(__name__)

# Connect to redis
REDIS_HOST = os.getenv('REDIS_HOST')
REDIS_PORT = os.getenv('REDIS_PORT')
REDIS_PASSWORD = os.getenv('REDIS_PASSWORD')
redis = Redis(host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PASSWORD)

@app.route('/')
def hello_world():
    return 'Good Morning, Vietnam!'

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=3000)