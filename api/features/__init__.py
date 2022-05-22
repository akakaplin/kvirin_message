
from .is_known import check_known
from .is_russian import check_russian
from .is_working_hours import check_working_hours

FEATURES = {
    'is_working_hours': check_working_hours,
    'is_known': check_known,
    'is_russian': check_russian,
}