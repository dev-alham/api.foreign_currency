import logging
import json
from datetime import datetime, timedelta

from django.db.models import F, Count
from django.db import IntegrityError, transaction

from api.models import *
from api.serializers import *

log = logging.getLogger()

CACHE_EXPIRE_TIME_LONG = 60 * 30
CACHE_EXPIRE_TIME_SHORT = 60

def get_setting():
    q = Setting.objects.filter(
        id=1
    ).first()

    data = {
        'is_maintenance': False,
        'message': 'System maintenance'
    }

    if not q:
        data['is_maintenance'] = True
        data['message'] = "Please insert data on setting database"
        return data
    else:
        setting = SettingSerializer(q).data
        data['is_maintenance'] = setting['is_maintenance']
        return data

def add_exchange_rate_log(get_exchange_db, exchange_rate):
    try:
        with transaction.atomic():
            ExchangeRateLog.objects.create(
                exchange_rate_id=get_exchange_db.id,
                date_rate=exchange_rate.get('date'),
                rate=float(exchange_rate.get('rate'))
            )
        return True
    except IntegrityError as e:
        log.error('failed add exchange_rate_log | %s' % (e))
        return False

def add_exchange_rate(exchange_rate):
    try:
        with transaction.atomic():
            ExchangeRate.objects.update_or_create(
                from_rate=exchange_rate.get('from_rate'),
                to_rate=exchange_rate.get('to_rate'),
                on_delete=1,
                defaults={'on_delete': 0}
            )
        return True
    except IntegrityError as e:
        log.error('failed add exchange_rate| %s' % (e))
        return False


def get_exchange(from_rate, to_rate):
    exchange = ExchangeRate.objects.filter(
        from_rate=from_rate,
        to_rate=to_rate,
        on_delete=0
    ).first()

    if not exchange:
        return False
    return exchange

def get_exchange_rate_all():
    exchange_rate = ExchangeRate.objects.filter(
        on_delete=0
    ).all()
    return json.dumps(RateSerializer(exchange_rate, many=True).data)

def get_exchange_rate(exchange_rate_id):
    exchange_rate = ExchangeRate.objects.filter(
        id=exchange_rate_id
    ).first()

    if not exchange_rate:
        return False
    return exchange_rate

def delete_exchange_rate(exchange_rate):
    try:
        with transaction.atomic():
            exchange_rate.on_delete = 1
            exchange_rate.save(update_fields=["on_delete"])

        return True
    except IntegrityError as e:
        log.error('failed update coin | %s' % (e))
        return False

def get_trend_rate(limit):
    trend_exchnage_rate = ExchangeRateLog.objects.all().order_by('-date_rate')[:limit]
    return json.dumps(TrendSerializer(trend_exchnage_rate, many=True).data)

def get_rate_track(date_req):
    datetime_obj = datetime.strptime(date_req, '%Y-%m-%d')
    # end_week = datetime_obj + datetime.timedelta(7)
    exhange_log = ExchangeRateLog.objects.filter(
        date_rate=[datetime_obj, datetime_obj]
    ).all()

    return False

