import logging
import json

from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from rest_framework.views import APIView
from rest_framework.decorators import parser_classes
from rest_framework.parsers import JSONParser

from api import db_manager
from api.utils import check_req, normalize_req, validate_date, convert_int
from api.decorators import api_check_maintenance
from django_www.utils import resp_err, resp_success

log = logging.getLogger()

LIST_REQ = {
    "exchange_post": ["date","from_rate", "to_rate", "rate"],
    "rate_post": ["from_rate", "to_rate"]
}


class ProtectedView(View):
    decorators = [csrf_exempt, api_check_maintenance]

    @method_decorator(decorators)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

class ExchangeView(ProtectedView, APIView):
    @parser_classes((JSONParser,))
    def post(self, request, param=None):
        if param:
            return resp_err('Invalid input', 1, 417)

        req_data = request.data

        if not req_data:
            return resp_err('Invalid input', 2, 406)

        sts_req_data = check_req(LIST_REQ['exchange_post'], list(req_data.keys()))
        if not sts_req_data:
            return resp_err('Invalid input', 3, 406)

        sts_validate_date = validate_date(req_data.get('date'))
        if not sts_validate_date:
            return resp_err('Format date not valid', 4, 406)

        sts_normalize_req = normalize_req(req_data)
        if not sts_normalize_req:
            return resp_err('Invalid input', 4, 406)

        get_exchange_db = db_manager.get_exchange(req_data.get('from_rate'), req_data.get('to_rate'))
        if not get_exchange_db:
            return resp_err('Not exchange data', 5, 406)

        sts_add_exchange_db = db_manager.add_exchange_rate_log(get_exchange_db, req_data)
        if not sts_add_exchange_db:
            return resp_err('Please try again', 6, 417)

        result = {
            "message": "Create data successful",
            "from_rate": req_data.get('from_rate'),
            "to_rate": req_data.get('to_rate'),
            "rate": float(req_data.get('rate'))
        }

        return resp_success(result, 201)

class RateView(ProtectedView, APIView):

    def get(self, request, param=None):
        if param:
            return  resp_err('Invalid input', 1, 417)

        result = json.loads(db_manager.get_exchange_rate_all())
        return resp_success(result)

    def delete(self, request, param=None):
        if not param:
            return resp_err('Invalid input', 1, 417)

        exchange_rate = db_manager.get_exchange_rate(param)
        if not exchange_rate:
            return resp_err('Data already exists', 2, 417)

        sts_delete_exchange_rate = db_manager.delete_exchange_rate(exchange_rate)
        if not sts_delete_exchange_rate:
            return resp_err('Please try again', 3, 417)

        result = {
            "message": "Delete data successful",
            "from_rate": exchange_rate.from_rate,
            "to_rate": exchange_rate.to_rate
        }
        return resp_success(result)

    @parser_classes((JSONParser,))
    def post(self, request, param=None):
        if param:
            return  resp_err('Invalid input', 1, 417)

        req_data = request.data

        if not req_data:
            return resp_err('Invalid input', 2, 406)

        sts_req_data = check_req(LIST_REQ['rate_post'], list(req_data.keys()))
        if not sts_req_data:
            return resp_err('Invalid input', 3, 406)

        sts_normalize_req = normalize_req(req_data)
        if not sts_normalize_req:
            return resp_err('Invalid input', 4, 406)

        sts_get_exchange_db = db_manager.get_exchange(req_data.get('from_rate'), req_data.get('to_rate'))
        if sts_get_exchange_db:
            return resp_err('Data already exists', 5, 417)

        sts_add_exchange_rate_db = db_manager.add_exchange_rate(req_data)
        if not sts_add_exchange_rate_db:
            return resp_err('Please try again', 6, 417)

        result = {
            "message": "Create data successful",
            "from_rate": req_data.get('from_rate'),
            "to_rate": req_data.get('to_rate')
        }

        return resp_success(result, 201)

class DetailRateView(ProtectedView, APIView):
    def get(self, request, category=None, param=None):
        # for trend
        if category == 'trend':
            if not param:
                return resp_err('Invalid input', 1, 417)

            param_int = convert_int(param)
            if not param_int:
                return resp_err('Invalid input', 2, 417)

            result = json.loads(db_manager.get_trend_rate(param_int))

            return resp_success(result)

        #for date
        elif category == 'date':
            sts_validate_data = validate_date(param)
            if not sts_validate_data:
                return resp_err('Invalid input', 1, 417)

            data = db_manager.get_rate_track(param)

            return resp_success(data)








