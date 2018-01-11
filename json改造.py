# -*- coding: utf-8 -*-
__author__ = 'ShengLeQi'

import json
from datetime import date
from datetime import datetime


class CustomEncoder(json.JSONEncoder):
    def default(self, field):
        print(type(field),field)
        if isinstance(field, datetime):
            return field.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(field, date):
            return field.strftime('%Y-%m-%d')
        else:
            return json.JSONEncoder.default(self, field)


dic = {
    'k1':'v1',
    'k2':123,
    'ctime':datetime.now()
}

ds = json.dumps(dic,cls=CustomEncoder)
print(ds)