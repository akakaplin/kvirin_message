
from .is_bad import check_bad
from .is_working_hours import check_working_hours

FEATURES = {
    'is_working_hours': check_working_hours,
    'is_bad': check_bad,
}