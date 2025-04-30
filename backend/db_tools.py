import us
import math


def state_abbreviations(state_name):
    state = us.states.lookup(state_name)
    return state.abbr if state else state_name


def to_list(list: dict, template: object):
    return [{column.key: getattr(
        saved_job, column.key) for column in template.__table__.columns
    } for saved_job in list]


def clean_nans(data):
    for job in data:
        for key, value in job.items():
            if isinstance(value, float) and math.isnan(value):
                job[key] = None
    return data