from datetime import datetime
import pytz

def check_working_hours(user_data, db) -> bool:
    moscow_time = datetime.now(pytz.timezone('Europe/Moscow'))
    return moscow_time.hour < 18 and moscow_time.hour > 8
