from db import DB

WHITELIST = ['79000000000', '79000000001']

def check_known(user_data: dict, db: DB) -> bool:
    if user_data['cell'] in WHITELIST:
        return True
    return False