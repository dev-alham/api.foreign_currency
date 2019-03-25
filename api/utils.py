import redis
import datetime

from django.conf import settings

def check_req(list_params, req_params):
    check_req = set(list_params).issubset(req_params)
    if check_req:
        return True
    return False

def validate_date(date_req):
    try:
        date_req = str(date_req)
        datetime.datetime.strptime(date_req, '%Y-%m-%d')
        return True
    except ValueError:
        return False

def normalize_req(req_data):
    try:
        req_data['from_rate'] = req_data.get('from_rate').upper()
        req_data['to_rate'] = req_data.get('to_rate').upper()
        return True
    except:
        return False

def convert_int(req_data):
    try:
        data = int(req_data)
        return data
    except ValueError:
        return False