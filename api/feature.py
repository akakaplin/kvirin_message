import random
from db import DB
from features import FEATURES

def route_signal_user(user_data: dict, db: DB, pools: dict) -> str:
    user_id = 'signal_' + user_data.get('uid')

    for name in pools:
        pool = pools[name]
        ok = True
        for feature in pool.features:
            name = feature['feature']
            if name in FEATURES:
                if FEATURES[name](user_data, db) != feature['value']:
                    ok = False

        if ok:
            return random.choice(pool.bridges), user_id
    
    return None, user_id
