from db import DB

WHITELIST = set(['79000000000', '79000000001'])

def check_russian(user_data: dict, db: DB) -> bool:
    return str(user_data['cell']).startswith('79')
