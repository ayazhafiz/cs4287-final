import gzip
import ctypes

from datetime import datetime

class Request(ctypes.BigEndianStructure):
    _fields_ = [
        ("timestamp", ctypes.c_uint32),
        ("clientID", ctypes.c_uint32),
        ("objectID", ctypes.c_uint32),
        ("size", ctypes.c_uint32),
        ("method", ctypes.c_uint8),
        ("status", ctypes.c_uint8),
        ("type", ctypes.c_uint8),
        ("server", ctypes.c_uint8),
    ]

# The dataset can be fetched from Internet Traffic Archive's World Cup (1988) traffic data.
request_timestamps = []
with gzip.open("ita_public_tools/input/test_log.gz", "rb") as f:
    result = []
    request = Request()
    while f.readinto(request) == ctypes.sizeof(request):
        ts = request.timestamp
        # Note: These timestamps are actually in GMT (+0200), but that doesn't
        # matter for the purpose of the load testing.
        date = datetime.fromtimestamp(ts)
        date_formatted = date.strftime('%A %B %d. %Y %H:%M:%S')
        print(date_formatted)

        request_timestamps.append(ts)

# print(request_timestamps)
