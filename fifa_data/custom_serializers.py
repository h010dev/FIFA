import json
import datetime


class DateTimeEncoder(json.JSONEncoder):

    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.isoformat()
        return json.JSONEncoder.encode(self, obj)


class DateTimeDecoder(json.JSONDecoder):

    def decode(self, obj):
        d = json.JSONDecoder.decode(self, obj)
        if isinstance(datetime.datetime.fromisoformat(d), datetime.datetime):
            return datetime.datetime.fromisoformat(d)
        return d
