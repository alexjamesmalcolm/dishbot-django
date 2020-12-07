from urllib3 import PoolManager
import json

http = PoolManager()


def request_current_user(token):
    r = http.request(
        "GET",
        "https://api.groupme.com/v3/users/me",
        fields={"token": token},
    )
    return json.loads(r.data.decode("utf-8"))